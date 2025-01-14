from classes.student import Student
from collections import deque, defaultdict

def Greedy_Round_Robin(students, courses):
    # Create a virtual charity student
    charity = Student(student_id='charity', credit_cap=float('inf'), valuation_function={})

    # Sorting courses by non-decreasing order of endtime
    courses.sort(key=lambda course: course.end_time)

    # Initialize charity and the envy graph
    D = courses[:]  # Initially, all courses are unallocated
    G = {student.student_id: [] for student in students}  # Envy graph, initially empty
    allocation = {student.student_id: [] for student in students}  # Initial allocation is empty for all students
    # Phase 1: Initial allocation based on student preferences
    for course in courses:
        # Identify students who are not envied by anyone (no incoming edges in G)
        non_envied_students = [student for student in students if all(student.student_id not in G[other.student_id] for other in students)]
        # Determine if any of the non-envied students can increase their utility by adding this course
        for student in non_envied_students:
            if len(allocation[student.student_id]) < student.get_credit_cap():
                # Calculate the Maximum Weighted Independent Set (MWIS) for this student with the new course included
                potential_allocation = allocation[student.student_id] + [course]
                A_prime = MWIS(student, potential_allocation)
                # Check if this new allocation improves the student's utility
                if sum(student.valuation_function.get(c.course_id, 0) for c in A_prime) > student.utility(allocation):
                    allocation[student.student_id] = A_prime
                    D = list(set(D).union(set(allocation[student.student_id])) - set(A_prime))  # Update charity
                    G = update_envy_graph(G, students, allocation, student)  # Update envy graph
                    break  # Move to the next course after allocation
    # Phase 3: Allocate remaining courses to charity
    students.append(charity)
    charity_allocation = [course for course in courses if course not in [c for alloc in allocation.values() for c in alloc]]
    allocation[charity.student_id] = charity_allocation
    
    return allocation

# Define the MWIS function
def MWIS(student, courses):
    if str(student.student_id) == "charity":
        return courses
    """Find the Maximum Weighted Independent Set of courses considering the student's credit cap."""
    n = len(courses)
    if n == 0:
        return []
    credit_cap = student.get_credit_cap()
    dp = [[0] * (int(credit_cap) + 1) for _ in range(n + 1)]
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

def conflicts(course1, course2):
    return not (course1.end_time <= course2.start_time or course2.end_time <= course1.start_time)

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
        
        #Rebuild the envy graph after resolving the cycle old code 
        # for i in students:
        #     G[i.student_id] = []
        # for i in students:
        #     for j in students:
        #         if i != j and sum(i.valuation_function.get(c.course_id, 0) for c in allocation[j.student_id]) > sum(i.valuation_function.get(c.course_id, 0) for c in allocation[i.student_id]):
        #             G[i.student_id].append(j.student_id)
    
    return G

def detect_single_cycle(G):
    visited = set()
    
    def dfs(node, path):
        if node in path:
            cycle_start_index = path.index(node)
            return path[cycle_start_index:]  # Return the detected cycle
        if node in visited:
            return None
        visited.add(node)
        path.append(node)
        for neighbor in G[node]:
            result = dfs(neighbor, path.copy())
            if result:
                return result  # Return the cycle if found
        path.pop()
        return None
    
    for node in G:
        if node not in visited:
            cycle = dfs(node, [])
            if cycle:
                return cycle  # Return the first detected cycle
    
    return None  # No cycle found

def resolve_cycle(cycle, allocation):
    """Resolves an envy cycle by performing a cyclic shift of allocations."""
    n = len(cycle)
    temp_allocation = allocation[cycle[0]].copy()
    
    # Perform the cyclic shift
    for i in range(n - 1):
        allocation[cycle[i]] = allocation[cycle[i + 1]]
    
    allocation[cycle[-1]] = temp_allocation

def level_ordered_topological_sort(G):
    """
    Performs a level-ordered topological sort on the envy graph G.
    Returns a list of levels, where each level is a list of students.
    """
    # Step 1: Calculate in-degrees of all nodes
    in_degree = {node: 0 for node in G}
    for node in G:
        for neighbor in G[node]:
            in_degree[neighbor] += 1

    # Step 2: Initialize the queue with nodes that have in-degree 0
    queue = deque([node for node in G if in_degree[node] == 0])
    level_dict = defaultdict(int)  # This will map each node to its level

    # Step 3: Process nodes in topological order
    while queue:
        node = queue.popleft()

        # Determine the level of the current node based on its predecessors
        max_predecessor_level = -1
        for predecessor in G:
            if node in G[predecessor]:  # If `predecessor` is an incoming neighbor
                max_predecessor_level = max(max_predecessor_level, level_dict[predecessor])

        # Assign the current node a level
        level_dict[node] = max_predecessor_level + 1

        # Process each neighbor (successor)
        for neighbor in G[node]:
            in_degree[neighbor] -= 1  # Decrease in-degree of neighbors
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Step 4: Create levels from the level_dict
    max_level = max(level_dict.values(), default=0)
    levels = [[] for _ in range(max_level + 1)]
    for node, level in level_dict.items():
        levels[level].append(node)
    return levels  # Return the list of levels