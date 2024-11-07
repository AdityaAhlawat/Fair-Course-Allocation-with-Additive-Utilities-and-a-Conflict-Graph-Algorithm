from collections import deque
from itertools import chain, combinations

def EFX_Allocation_With_Bounded_Charity(students, courses):
    # Initialize empty allocation and pool of unallocated goods
    allocation = {student.get_id(): [] for student in students}
    pool = courses[:]  # All courses initially in the pool
    envy_graph = {student.get_id(): [] for student in students}  # Empty envy graph

    # Main loop: Continue applying update rules while applicable
    while is_any_rule_applicable(students, allocation, pool, envy_graph):
        # Select an applicable rule (U0, U1, or U2)
        if is_u0_applicable(students, allocation, pool):
            print("U0 is being run")
            allocation, pool, affected_student = apply_u0(allocation, pool, students)
        elif is_u2_applicable(students, allocation, pool, envy_graph):
            print("U2 is being run")
            allocation, pool, affected_student = apply_u2(students, allocation, pool, envy_graph)
        elif is_u1_applicable(students, allocation, pool):
            print("U1 is being run")
            allocation, pool, affected_student = apply_u1(students, allocation, pool)
        for student in students:
            assigned_courses = allocation[student.student_id]
            utility = student.utility(allocation)
            course_details = [
                f"Course {course.course_id} (Start: {course.start_time}, End: {course.end_time})"
                for course in assigned_courses
            ]
            valuation_function_details = {
                course_id: value for course_id, value in student.valuation_function.items()
            }
            print(f"Student {student.student_id} assigned courses: {course_details}, Utility: {utility}")
        print("Next Stage")
        # Update the envy graph after applying the rule with the affected student
        if affected_student != None:
            envy_graph = update_envy_graph(envy_graph, students, allocation, affected_student)

    allocation['charity'] = pool  # Assign the remaining courses in the pool to 'charity'

    return allocation


def is_any_rule_applicable(students, allocation, pool, envy_graph):
    # Check if any of the update rules (U0, U1, U2) are applicable
    return is_u0_applicable(students, allocation, pool) or is_u1_applicable(students, allocation, pool) or is_u2_applicable(students, allocation, pool, envy_graph)

def is_u0_applicable(students, allocation, pool):
    # Check if U0 is applicable
    for course in pool:
        #We need not look at all students but only the sources of envy graph -> Optimization
        for student in students:
            if can_allocate_good(student, course, allocation, students):
                return True
    return False


def apply_u0(allocation, pool, students):
    for course in pool:
        for student in students:
            if can_allocate_good(student, course, allocation, students):
                allocation[student.get_id()].append(course)
                pool.remove(course)
                return allocation, pool, student
    return allocation, pool, None


def is_u1_applicable(students, allocation, pool):
    # Check if U1 is applicable: If any student values the pool more than their current bundle
    for student in students:
        if student_valuation(student, pool) > student_valuation(student, allocation[student.get_id()]):
            return True
    return False


def apply_u1(students, allocation, pool):
    # Find all agents who envy the pool up to any good (EFX)
    students_who_envy_pool_up_to_any_good = []
    for student in students:
        # Find the max course in the pool for the student's valuation
        max_course_in_pool = max(pool, key=lambda course: student.valuation_function.get(course.course_id, 0))
        pool_copy = pool.copy()
        pool_copy.remove(max_course_in_pool)
        
        # Check if the student envies the pool copy more than their current allocation
        if student_valuation(student, pool_copy) > student_valuation(student, allocation[student.get_id()]):
            students_who_envy_pool_up_to_any_good.append(student)
    if len(students_who_envy_pool_up_to_any_good) == 0:
        return allocation, pool, None
    # Initialize variables to find the most envious agent and the minimal envied subset
    most_envious_agent = None
    minimal_envied_subset = None

    # Determine the maximum subset size needed, default to the length of the pool
    maxValueNecessary = len(pool)

    student = students_who_envy_pool_up_to_any_good[0]
    current_allocation_value = student_valuation(student, allocation[student.get_id()])
    breakOutOfMain = False
    for subset_size in range(1, len(pool)):
        for subset in combinations(pool, subset_size):
            subset_list = list(subset)
            # Check if this subset is envied by the current student
            if student_valuation(student, subset_list) > current_allocation_value:
                maxValueNecessary = len(subset_list)
                breakOutOfMain = True
                break
        if breakOutOfMain == True:
            break
    # Generate subsets up to the determined maxValueNecessary size outside the second loop
    subsets = []
    for subset_size in range(1, maxValueNecessary + 1):
        for subset in combinations(pool, subset_size):
            subsets.append(list(subset))
    foundValues = False
    for student in students_who_envy_pool_up_to_any_good:
        current_allocation_value = student_valuation(student, allocation[student.get_id()])
        sorted_subsets = sorted(subsets, key=lambda subset: student_valuation(student, subset))
        for subset_list in sorted_subsets:
            if student_valuation(student, subset_list) > current_allocation_value:
                valid = True
                for different_student in students_who_envy_pool_up_to_any_good:
                    if different_student != student:
                        min_course_in_subset = min(subset_list, key=lambda course: different_student.valuation_function.get(course.course_id, 0))
                        subset_copy = subset_list.copy()
                        subset_copy.remove(min_course_in_subset)
                        if student_valuation(different_student, subset_copy) > student_valuation(different_student, allocation[different_student.get_id()]):
                            valid = False
                            break
                if valid == True:
                    minimal_envied_subset = subset_list
                    most_envious_agent = student
                    foundValues = True
                break
        if foundValues == True:
            break

    # If we found a most envious agent and a minimal envied subset
    if most_envious_agent is not None and minimal_envied_subset is not None:
        # Update the allocation: assign the minimal envied subset Z to the most envious agent
        student_id = most_envious_agent.get_id()
        new_allocation = allocation.copy()
        new_allocation[student_id] = minimal_envied_subset
        
        # Update the pool by moving the previous allocation of the agent back to the pool and removing Z
        new_pool = list(set(allocation[student_id] + pool) - set(minimal_envied_subset))
        
        # Return the updated allocation and pool
        return new_allocation, new_pool, most_envious_agent

    # If no agent was found who envies the pool, return the original allocation and pool
    return allocation, pool, None

def find_most_envious_student_and_inclusion_wise_minimal_envied_subset(students, allocation, x_s_i_g_i):
    # Find all agents who envy the pool up to any good (EFX)
    students_who_envy_pool_up_to_any_good = []
    print(x_s_i_g_i)
    for student in students:
        # Find the max course in the pool for the student's valuation
        max_course_in_pool = max(x_s_i_g_i, key=lambda course: student.valuation_function.get(course.course_id, 0))
        pool_copy = x_s_i_g_i.copy()
        pool_copy.remove(max_course_in_pool)
        
        # Check if the student envies the pool copy more than their current allocation
        print(student_valuation(student, pool_copy), student_valuation(student, allocation[student.get_id()]))
        if student_valuation(student, pool_copy) > student_valuation(student, allocation[student.get_id()]):
            students_who_envy_pool_up_to_any_good.append(student)
    if len(students_who_envy_pool_up_to_any_good) == 0:
        print("yes")
        return None, None
    # Initialize variables to find the most envious agent and the minimal envied subset
    most_envious_agent = None
    minimal_envied_subset = None

    # Determine the maximum subset size needed, default to the length of the pool
    maxValueNecessary = len(x_s_i_g_i)

    student = students_who_envy_pool_up_to_any_good[0]
    current_allocation_value = student_valuation(student, allocation[student.get_id()])
    breakOutOfMain = False
    for subset_size in range(1, len(x_s_i_g_i)):
        for subset in combinations(x_s_i_g_i, subset_size):
            subset_list = list(subset)
            # Check if this subset is envied by the current student
            if student_valuation(student, subset_list) > current_allocation_value:
                maxValueNecessary = len(subset_list)
                breakOutOfMain = True
                break
        if breakOutOfMain == True:
            break
    # Generate subsets up to the determined maxValueNecessary size outside the second loop
    subsets = []
    for subset_size in range(1, maxValueNecessary + 1):
        for subset in combinations(x_s_i_g_i, subset_size):
            subsets.append(list(subset))
    foundValues = False
    for student in students_who_envy_pool_up_to_any_good:
        current_allocation_value = student_valuation(student, allocation[student.get_id()])
        sorted_subsets = sorted(subsets, key=lambda subset: student_valuation(student, subset))
        for subset_list in sorted_subsets:
            if student_valuation(student, subset_list) > current_allocation_value:
                valid = True
                for different_student in students_who_envy_pool_up_to_any_good:
                    if different_student != student:
                        min_course_in_subset = min(subset_list, key=lambda course: different_student.valuation_function.get(course.course_id, 0))
                        subset_copy = subset_list.copy()
                        subset_copy.remove(min_course_in_subset)
                        if student_valuation(different_student, subset_copy) > student_valuation(different_student, allocation[different_student.get_id()]):
                            valid = False
                            break
                if valid == True:
                    minimal_envied_subset = subset_list
                    most_envious_agent = student
                    foundValues = True
                break
        if foundValues == True:
            break

    # If we found a most envious agent and a minimal envied subset
    if most_envious_agent is not None and minimal_envied_subset is not None:
        return most_envious_agent, minimal_envied_subset
    else:
        return None, None

def is_u2_applicable(students, allocation, pool, envy_graph):
    # Get the number of students
    num_students = len(students)

    # Check if Rule U0 is not applicable
    if is_u0_applicable(students, allocation, pool):
        return False 

    # Check if the pool contains at least `n` goods
    if len(pool) >= num_students:
        return True
    
    return False

def apply_u2(students, allocation, pool, envy_graph):
    # Initialize sources and cycle tracking
    sources = [student for student in students if len(envy_graph[student.get_id()]) == 0]
    distinct_goods = []
    selected_sources = []
    most_envious_agents = []
    minimal_envied_subsets = []
    cycle_detected = False
    l = 0  # Length of the cycle

    # Cycle detection and reallocation preparation
    while sources and pool and not cycle_detected:
        current_source = sources.pop(0)
        selected_sources.append(current_source)

        # Assign a distinct good to the current source
        good = pool.pop(0)
        allocation[current_source.get_id()].append(good)
        distinct_goods.append(good)

        # Use find_most_envious_student_and_inclusion_wise_minimal_envied_subset
        most_envious_agent, minimal_envied_subset = find_most_envious_student_and_inclusion_wise_minimal_envied_subset(students, allocation, allocation[current_source.get_id()])
        
        # Handle None return values to avoid errors
        if most_envious_agent is None or minimal_envied_subset is None:
            break  # Exit loop if no envious agent is found

        most_envious_agents.append(most_envious_agent)
        minimal_envied_subsets.append(minimal_envied_subset)

        # Update the envy graph
        envy_graph = update_envy_graph(envy_graph, students, allocation, current_source)

        # Detect cycle in the envy graph
        cycle = detect_single_cycle(envy_graph)
        if cycle:
            cycle_detected = True
            l = len(cycle)
            break

    # If no cycle was detected, return
    if not cycle_detected:
        return allocation, pool, None

    # Step 1: Update the pool P by excluding the required items
    updated_pool = [g for g in pool if g not in distinct_goods]
    for i in range(l):
        source_allocation = allocation[cycle[i].get_id()]
        Z_i = minimal_envied_subsets[i]
        updated_pool += [g for g in source_allocation if g not in Z_i]

    # Step 2: Reallocate goods along the cycle
    for i in range(l):
        si = cycle[i]
        ti = cycle[(i + 1) % l]

        # Step 2a: Find path in the envy graph from si to ti
        path = find_path_in_envy_graph(envy_graph, si, ti)

        # Step 2b: Shift allocations along the path
        for k in range(len(path) - 1):
            current_node = path[k]
            next_node = path[k + 1]
            allocation[current_node.get_id()] = allocation[next_node.get_id()]

    # Step 3: Assign the minimal envied subset to the final target node ti
    # Set allocation for each ti in the cycle to Z_{i-1}, and all other j to their original allocation
    for i in range(l):
        ti = cycle[(i + 1) % l]  # Final target in the path for the current segment
        allocation[ti.get_id()] = minimal_envied_subsets[i - 1]  # Set X0_ti = Z_{i-1}

    # Return the updated allocation and pool
    return allocation, updated_pool, None


def update_envy_graph(G, students, allocation, affected_student):
    # Get the student whose allocation changed
    student_id = affected_student.student_id

    # Clear only the envy relations of the affected student
    G[student_id] = []
    
    # Recompute envy relations for the affected student against all other students
    for other_student in students:
        if student_id != other_student.student_id:
            # If the other student's allocation is better in terms of utility, add an envy edge
            if sum(affected_student.valuation_function.get(c.course_id, 0) for c in allocation[other_student.student_id]) > sum(affected_student.valuation_function.get(c.course_id, 0) for c in allocation[student_id]):
                G[student_id].append(other_student.student_id)
            
            # Additionally, update the envy relations for the other student towards the affected student
            if sum(other_student.valuation_function.get(c.course_id, 0) for c in allocation[student_id]) > sum(other_student.valuation_function.get(c.course_id, 0) for c in allocation[other_student.student_id]):
                if student_id not in G[other_student.student_id]:
                    G[other_student.student_id].append(student_id)
            else:
                # If there was an envy relation before and it's no longer valid, remove it
                if student_id in G[other_student.student_id]:
                    G[other_student.student_id].remove(student_id)

    # Continuously check and resolve cycles
    while True:
        cycle = detect_single_cycle(G)  # Detect only one cycle
        if not cycle:
            break  # No cycles detected, exit loop
        
        # Resolve the detected cycle
        resolve_cycle(cycle, allocation)

        nodes_to_update = set(cycle)

        for node in G:
            for neighbor in G[node]:
                if neighbor in cycle:
                    nodes_to_update.add(node)

        for i in students:
            if i.student_id in nodes_to_update:
                G[i.student_id] = []
                for j in students:
                    if i != j and sum(i.valuation_function.get(c.course_id, 0) for c in allocation[j.student_id]) > sum(i.valuation_function.get(c.course_id, 0) for c in allocation[i.student_id]):
                        G[i.student_id].append(j.student_id)
    
    return G

def can_allocate_good(student, course, allocation, students):
    # Temporarily allocate the course to the student
    student_bundle = allocation[student.get_id()].copy()
    student_bundle.append(course)
    for other_student in students:
        if other_student != student:
            other_student_bundle = allocation[other_student.get_id()]
            #Instead of running a for loop, calculate min good of stundent_bundle and remove it. 
            for good in student_bundle:
                modified_student_bundle = student_bundle.copy()
                modified_student_bundle.remove(good)
                if student_valuation(other_student, modified_student_bundle) > student_valuation(other_student, other_student_bundle):
                    return False
    return True 

def student_valuation(student, courses):
    n = len(courses)
    if n == 0:
        return 0  # Return 0 if there are no courses
    
    credit_cap = student.get_credit_cap()
    dp = [[0] * (credit_cap + 1) for _ in range(n + 1)]  # DP table to store utility values
    
    # Sort courses by end time to use dynamic programming effectively
    courses.sort(key=lambda x: x.end_time)
    
    for i in range(1, n + 1):
        current_course = courses[i - 1]
        current_utility = student.valuation_function.get(current_course.course_id, 0)  # Utility of the current course
        current_credits = current_course.credits  # Assuming each course has a credit value

        for c in range(credit_cap + 1):
            # Option 1: Exclude the current course
            dp[i][c] = dp[i - 1][c]
            
            # Option 2: Include the current course if it doesn't conflict and fits within the credit cap
            if c >= current_credits:
                for j in range(i - 1, 0, -1):
                    if not conflicts(current_course, courses[j - 1]):  # Check for conflicts
                        potential_utility = dp[j][c - current_credits] + current_utility
                        if potential_utility > dp[i][c]:
                            dp[i][c] = potential_utility
                        break
                else:
                    # No conflicts, consider the current course independently if credit cap allows
                    if dp[i][c] < current_utility and c >= current_credits:
                        dp[i][c] = current_utility
    
    # The result is the maximum utility for the given student and courses
    return dp[n][credit_cap]

def update_pool(pool, minimal_envied_subset):
    # Update the pool after reallocation
    return [good for good in pool if good not in minimal_envied_subset]


def detect_single_cycle(envy_graph):
    visited = set()

    def dfs(node, path):
        if node in path:
            return path[path.index(node):]  # Return the cycle
        visited.add(node)
        path.append(node)
        for neighbor in envy_graph[node]:
            cycle = dfs(neighbor, path.copy())
            if cycle:
                return cycle
        return None

    for node in envy_graph:
        if node not in visited:
            cycle = dfs(node, [])
            if cycle:
                return cycle
    return None


def resolve_cycle(cycle, allocation):
    # Resolve the cycle by shifting the bundles along the cycle
    n = len(cycle)
    temp_allocation = allocation[cycle[0]]
    for i in range(n - 1):
        allocation[cycle[i]] = allocation[cycle[i + 1]]
    allocation[cycle[-1]] = temp_allocation


def update_pool_after_cycle(pool, distinct_goods, minimal_envied_subsets):
    # Remove goods used in the reallocation
    for i, Z_i in enumerate(minimal_envied_subsets):
        # Remove the goods used in the allocation
        pool = [good for good in pool if good not in distinct_goods]
        
        # Add any unallocated goods back to the pool
        unallocated_goods = set(distinct_goods[i]) - set(Z_i)
        pool.extend(unallocated_goods)
        
    return pool

def conflicts(course1, course2):
    return not (course1.end_time <= course2.start_time or course2.end_time <= course1.start_time)

def find_path_in_envy_graph(envy_graph, source, target):
    
    # Breadth-First Search (BFS) to find the shortest path
    queue = deque([(source, [source])])
    visited = set()

    while queue:
        current_node, path = queue.popleft()
        
        if current_node == target:
            return path  # Return the path if the target is found
        
        if current_node not in visited:
            visited.add(current_node)
            
            # Explore neighbors
            for neighbor in envy_graph.get(current_node, []):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

    return None  # Return None if no path exists


def find_next_source_with_no_incoming_edges(selected_sources, envy_graph):
    # Step 1: Determine nodes that have incoming edges
    nodes_with_incoming_edges = set()
    
    for target_list in envy_graph.values():
        for target in target_list:
            nodes_with_incoming_edges.add(target)
    
    # Step 2: Check for nodes that are not in the 'nodes_with_incoming_edges' set
    for agent_id in envy_graph.keys():
        if agent_id not in nodes_with_incoming_edges and agent_id not in selected_sources:
            # Found a source with no incoming edges and not previously selected
            return agent_id
    
    # If no such source is found, return None
    return None
