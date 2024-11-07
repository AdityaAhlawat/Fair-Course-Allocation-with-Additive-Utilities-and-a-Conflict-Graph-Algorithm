def is_ef(allocation, students):
    ef_false_count = 0
    for student in students:
        if student.student_id == 'charity':
            continue
        own_courses_MWIS = MWIS(student, allocation[student.student_id])
        own_utility = sum(student.get_valuation_function().get(course.course_id, 0) for course in own_courses_MWIS)
        for other_student in students:
            if student != other_student:
                # Use MWIS to determine if the student would envy the other's allocation
                other_allocation = allocation[other_student.student_id]
                mwis_allocation = MWIS(student, other_allocation)
                other_utility = sum(student.valuation_function.get(course.course_id, 0) for course in mwis_allocation)
                if other_utility > own_utility:
                    ef_false_count += 1
                    #print(f"Student {student.student_id} envies Student {other_student.student_id} under EF condition. Student {student.student_id} values their own bundle at {own_utility} and the envied bundle at {other_utility}")
    if ef_false_count == 0:
        return True, ef_false_count
    else:
        return False, ef_false_count

def is_ef1(allocation, students):
    ef1_false_count = 0
    for student in students:
        if student.student_id == 'charity':
            continue
        own_courses_MWIS = MWIS(student, allocation[student.student_id])
        own_utility = sum(student.get_valuation_function().get(course.course_id, 0) for course in own_courses_MWIS)
        for other_student in students:
            if student != other_student:
                other_allocation = allocation[other_student.student_id]
                if len(other_allocation) > 0:
                    mwis_allocation = MWIS(student, other_allocation)
                    max_utility_item = max(mwis_allocation, key=lambda course: student.valuation_function.get(course.course_id, 0))
                    other_allocation_without_max = [course for course in mwis_allocation if course != max_utility_item]
                    other_utility = sum(student.valuation_function.get(course.course_id, 0) for course in other_allocation_without_max)
                    if other_utility > own_utility:
                        ef1_false_count += 1
                        print(f"Student {student.student_id} envies Student {other_student.student_id} under EF1 condition after removing course {max_utility_item.course_id}. Student {student.student_id} values their own bundle at {own_utility} and the envied bundle (after removing the highest-valued item) at {other_utility}")
    if ef1_false_count == 0:
        return True, ef1_false_count
    else:
        return False, ef1_false_count

def is_efx(allocation, students):
    efx_false_count = 0
    for student in students:
        if student.student_id == 'charity':
            continue
        own_courses_MWIS = MWIS(student, allocation[student.student_id])
        own_utility = sum(student.get_valuation_function().get(course.course_id, 0) for course in own_courses_MWIS)
        for other_student in students:
            if student != other_student:
                other_allocation = allocation[other_student.student_id]
                if len(other_allocation) > 0:
                    mwis_allocation = MWIS(student, other_allocation)
                    min_utility_item = min(mwis_allocation, key=lambda course: student.valuation_function.get(course.course_id, 0))
                    other_allocation_without_min = [course for course in mwis_allocation if course != min_utility_item]
                    other_utility = sum(student.valuation_function.get(course.course_id, 0) for course in other_allocation_without_min)
                    if other_utility > own_utility:
                        efx_false_count += 1
                        print(f"Student {student.student_id} envies Student {other_student.student_id} under EFX condition after removing course {min_utility_item.course_id}. Student {student.student_id} values their own bundle at {own_utility} and the envied bundle (after removing the least-valued item) at {other_utility}")
    if efx_false_count == 0:
        return True, efx_false_count
    else:
        return False, efx_false_count

def MWIS(student, courses):
    """Find the Maximum Weighted Independent Set of courses considering the student's credit cap."""
    n = len(courses)
    if n == 0:
        return []

    credit_cap = student.get_credit_cap()
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

def conflicts(course1, course2):
    return not (course1.end_time <= course2.start_time or course2.end_time <= course1.start_time)
