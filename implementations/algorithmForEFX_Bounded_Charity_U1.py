from collections import deque
from itertools import chain, combinations

def EFX_Allocation_With_Bounded_Charity_U1(students, courses):
    # Initialize empty allocation and pool of unallocated goods
    allocation = {student.get_id(): [] for student in students}
    pool = courses[:]  # All courses initially in the pool
    envy_graph = {student.get_id(): [] for student in students}  # Empty envy graph
    # Main loop: Continue applying update rules while applicable
    while is_u1_applicable(students, allocation, pool):
        allocation, pool, affected_student = apply_u1(students, allocation, pool)
        
        # Update the envy graph after applying the rule with the affected student
        if affected_student != None:
            envy_graph = update_envy_graph(envy_graph, students, allocation, affected_student)

    allocation['charity'] = pool  # Assign the remaining courses in the pool to 'charity'
    
    #for student in students:
        #allocation['charity'].extend(list(set(allocation[student.get_id()]) - set(MWIS(student, allocation[student.get_id()]))))

    return allocation

def is_u1_applicable(students, allocation, pool):
    # Check if U1 is applicable: If any student values the pool more than their current bundle
    for student in students:
        if student_valuation(student, pool) > student_valuation(student, allocation[student.get_id()]):
            return True
    return False


def apply_u1(students, allocation, pool):
    # Step 1: Identify an agent who envies the pool more than their own bundle
    envious_agents = [st for st in students if student_valuation(st, pool) > student_valuation(st, allocation[st.get_id()])]
    if not envious_agents:
        # No agent envies the pool, so U1 does not apply
        return allocation, pool, None

    # S = pool (the initially envied set)
    S = pool[:]
    Z = S[:]  # Start with Z = S

    # Step 2: Compute the minimal envied subset Z from S according to Algorithm 3
    # We'll do exactly one pass over all agents and all goods in Z.
    # As we remove goods, the set Z shrinks, and subsequent checks use the updated Z.
    for i_stud in students:
        X_i = allocation[i_stud.get_id()]
        v_i_Xi = student_valuation(i_stud, X_i)

        # Since we are going to remove goods from Z, iterate over a copy of Z
        for g in Z[:]:  # Use a copy to avoid modifying Z while iterating
            Z_minus_g = [x for x in Z if x != g]
            if v_i_Xi < student_valuation(i_stud, Z_minus_g):
                # Remove g immediately as per the algorithm
                Z.remove(g)

    # After the single pass, Z is an inclusion-wise minimal envied subset of S.
    if not Z:
        # If Z ends up empty, no minimal envied subset was found
        return allocation, pool, None

    # Step 3: Find an agent that envies Z more than her own bundle
    most_envious_agent = None
    for st in students:
        if student_valuation(st, Z) > student_valuation(st, allocation[st.get_id()]):
            most_envious_agent = st
            break

    if not most_envious_agent:
        # No agent envies Z, though we expected at least one
        return allocation, pool, None

    # Step 4: Reallocate Z to the most envious agent
    old_allocation_for_agent = allocation[most_envious_agent.get_id()]
    new_allocation = dict(allocation)
    new_allocation[most_envious_agent.get_id()] = Z

    # Update the pool: remove Z from pool and add the agent's old allocation back
    new_pool = [c for c in pool if c not in Z]
    new_pool += old_allocation_for_agent

    return new_allocation, new_pool, most_envious_agent

def find_most_envious_student_and_inclusion_wise_minimal_envied_subset(students, allocation, x_s_i_g_i, student_not_to_include):
    # Find all agents who envy the pool up to any good (EFX)
    students_who_envy_pool_up_to_any_good = []
    for student in students:
        if student != student_not_to_include:
            # Find the max course in the pool for the student's valuation
            for course in x_s_i_g_i:
                pool_copy = x_s_i_g_i.copy()
                pool_copy.remove(course)
                # Check if the student envies the pool copy more than their current allocation
                if student_valuation(student, pool_copy) > student_valuation(student, allocation[student.get_id()]):
                    students_who_envy_pool_up_to_any_good.append(student)
            
            # Check if the student envies the pool copy more than their current allocation
            if student_valuation(student, pool_copy) > student_valuation(student, allocation[student.get_id()]):
                students_who_envy_pool_up_to_any_good.append(student)
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

def update_envy_graph_fully(envy_graph, students, allocation):
    envy_graph.clear()
    envy_graph.update({student.get_id(): [] for student in students})

    # Recalculate envy relationships
    for student in students:
        student_id = student.get_id()
        
        # Calculate the total valuation for the student's allocation, defaulting to 0 if empty
        student_valuation = sum(
            student.valuation_function.get(course.course_id, 0) 
            for course in allocation.get(student_id, [])
        ) if allocation.get(student_id) else 0  # Default to 0 if no allocation exists

        # Check if the student envies any other student
        for other_student in students:
            other_student_id = other_student.get_id()
            if other_student_id == student_id:
                continue  # Skip self-comparison

            # Calculate the valuation for the other student's allocation, defaulting to 0 if empty
            other_student_valuation = sum(
                student.valuation_function.get(course.course_id, 0) 
                for course in allocation.get(other_student_id, [])
            ) if allocation.get(other_student_id) else 0  # Default to 0 if no allocation exists

            # If the student values the other student's bundle more, add an envy edge
            if other_student_valuation > student_valuation:
                envy_graph[student_id].append(other_student_id)

    return envy_graph

def C(envy_graph, source, students):
    reachable_nodes = set()
    queue = [source]  # Initialize queue with the source object

    while queue:
        current = queue.pop(0)  # Use the first element for BFS traversal
        current_id = current.get_id()  # Retrieve the ID of the current object

        if current_id not in reachable_nodes:
            reachable_nodes.add(current)  # Mark the current node's ID as visited

            # Enqueue neighbors as objects if they haven’t been visited
            for neighbor in envy_graph[current.get_id()]:
                if students[neighbor-1] not in reachable_nodes:
                    queue.append(students[neighbor-1])
    return reachable_nodes

def find_path_bfs(envy_graph, start, end, students):
    if start == end:
        return [start]

    queue = [(start, [start])]  # Each element is (current_node, path_to_current_node)
    visited = set([start.get_id()])  # To avoid revisiting nodes by storing IDs

    while queue:
        current, path = queue.pop(0)  # BFS traversal using the first element in queue
        current_id = current.get_id()  # Retrieve ID of the current node object

        # Explore neighbors in envy_graph
        for neighbor_id in envy_graph.get(current_id, []):
            neighbor = students[neighbor_id - 1]  # Access neighbor object by ID
            
            if neighbor == end:
                return path + [end]  # Found the path to end
            
            if neighbor.get_id() not in visited:
                visited.add(neighbor.get_id())
                queue.append((neighbor, path + [neighbor]))

    return None  # No path found


def print_envy_graph(envy_graph):
    print("Envy Graph:")
    for student, envied_students in envy_graph.items():
        if envied_students:
            print(f"Student {student} envies: {', '.join(map(str, envied_students))}")
        else:
            print(f"Student {student} envies no one.")

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
    for owned_course in student_bundle:
        if conflicts(owned_course, course):
            return False
    student_bundle.append(course)
    for other_student in students:
        if other_student != student:
            other_student_bundle = allocation[other_student.get_id()]
            #Instead of running a for loop, calculate min good of student_bundle and remove it. 
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
    
    # Handle infinity or very large credit caps
    if credit_cap == float('inf') or credit_cap > 1000:  # Set a reasonable upper bound
        credit_cap = 1000
    
    # Ensure credit_cap is a valid integer
    try:
        credit_cap = int(credit_cap)
    except (OverflowError, ValueError):
        credit_cap = 1000  # Default to a reasonable value
    
    dp = [[0] * (credit_cap + 1) for _ in range(n + 1)]
    
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

def MWIS(student, courses):
    n = len(courses)
    if n == 0:
        return []
      
    if str(student.student_id) == "charity":
        return courses

    credit_cap = student.get_credit_cap()
    
    # Handle infinity or very large credit caps
    if credit_cap == float('inf') or credit_cap > 1000:  # Set a reasonable upper bound
        credit_cap = 1000
    
    # Ensure credit_cap is a valid integer
    try:
        credit_cap = int(credit_cap)
    except (OverflowError, ValueError):
        credit_cap = 1000  # Default to a reasonable value
    
    dp = [[0] * (credit_cap + 1) for _ in range(n + 1)]
    selected_courses = [[[] for _ in range(credit_cap + 1)] for _ in range(n + 1)]
    
    # Sort courses by end time to use dynamic programming effectively
    courses.sort(key=lambda x: x.end_time)
    
    for i in range(1, n + 1):
        current_course = courses[i - 1]
        current_utility = student.valuation_function.get(current_course.course_id, 0)
        current_credits = current_course.credits  # Assuming each course has a credit value

        for c in range(credit_cap + 1):
            # Option 1: Exclude the current course
            dp[i][c] = dp[i - 1][c]
            selected_courses[i][c] = selected_courses[i - 1][c]
            
            # Option 2: Include the current course if it doesn't conflict and fits within the credit cap
            if c >= current_credits:
                for j in range(i - 1, 0, -1):
                    if not conflicts(current_course, courses[j - 1]):
                        potential_utility = dp[j][c - current_credits] + current_utility
                        if potential_utility > dp[i][c]:
                            dp[i][c] = potential_utility
                            selected_courses[i][c] = selected_courses[j][c - current_credits] + [current_course]
                        break
                else:
                    # No conflicts, consider it independently if credit cap allows
                    if dp[i][c] < current_utility and c >= current_credits:
                        dp[i][c] = current_utility
                        selected_courses[i][c] = [current_course]
    
    # The result is the best set of courses considering all possibilities within the credit cap
    return selected_courses[n][credit_cap]
