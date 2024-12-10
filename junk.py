def apply_u1(students, allocation, pool):
    # Find all agents who envy the pool up to any good (EFX)
    students_who_envy_pool_up_to_any_good = []
    for student in students:
        # Find the max course in the pool for the student's valuation
        for course in pool:
            pool_copy = pool.copy()
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

    #Order the pool before hand
    pool = sorted(
    pool,
    key=lambda course: sum(s.valuation_function.get(course.course_id, 0) for s in students_who_envy_pool_up_to_any_good) / len(students_who_envy_pool_up_to_any_good),
    reverse=True 
    )

    print(len(pool))
    for subset_size in range(1, len(pool)):
        print(subset_size)
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


def apply_u1(students, allocation, pool):
    # Identify students who envy the pool up to any good (EFX)
    students_who_envy_pool_up_to_any_good = []
    for student in students:
        if student_valuation(student, pool) > student_valuation(student, allocation[student.get_id()]):
            students_who_envy_pool_up_to_any_good.append(student)
            
    if not students_who_envy_pool_up_to_any_good:
        print("u1 not possible")
        return allocation, pool, None

    # Sort pool based on aggregate valuation for envious students
    pool = sorted(
        pool,
        key=lambda course: sum(
            student.valuation_function.get(course.course_id, 0) for student in students_who_envy_pool_up_to_any_good
        ),
        reverse=True
    )

    most_envious_agent = None
    minimal_envied_subset = None
    maxValueNecessary = len(pool)

    # Find the smallest subset for the first envious student
    first_student = students_who_envy_pool_up_to_any_good[0]
    current_allocation_value = student_valuation(first_student, allocation[first_student.get_id()])
    print(len(pool))
    for subset_size in range(1, len(pool) + 1):
        print(subset_size)
        for subset in combinations(pool, subset_size):
            subset_list = list(subset)  # Convert tuple to list
            if student_valuation(first_student, subset_list) > current_allocation_value:
                maxValueNecessary = subset_size
                break
        else:
            continue
        break

    # Generate subsets up to maxValueNecessary
    subsets = list(chain.from_iterable(
        combinations(pool, subset_size) for subset_size in range(1, maxValueNecessary + 1)
    ))

    # Find the minimal envied subset for any envious student
    for student in students_who_envy_pool_up_to_any_good:
        current_allocation_value = student_valuation(student, allocation[student.get_id()])
        for subset in sorted(subsets, key=lambda s: student_valuation(student, list(s))):
            subset_list = list(subset)  # Convert tuple to list
            if student_valuation(student, subset_list) > current_allocation_value:
                # Validate subset for all other students
                #if all(
                    #student_valuation(other_student, subset_list[:-1]) <= student_valuation(other_student, allocation[other_student.get_id()])
                    #for other_student in students if other_student != student
                #):
                    minimal_envied_subset = subset_list
                    most_envious_agent = student
                    break
        if minimal_envied_subset:
            break

    # If a minimal envied subset is found
    if most_envious_agent and minimal_envied_subset:
        student_id = most_envious_agent.get_id()
        new_allocation = allocation.copy()
        new_allocation[student_id] = minimal_envied_subset

        # Update the pool
        new_pool = [course for course in pool if course not in minimal_envied_subset]
        new_pool += allocation[student_id]

        return new_allocation, new_pool, most_envious_agent

    # If no agent was found who envies the pool, return the original allocation and pool
    return allocation, pool, None