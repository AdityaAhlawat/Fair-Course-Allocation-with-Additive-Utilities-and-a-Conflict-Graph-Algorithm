import numpy as np
import matplotlib.pyplot as plt
from classes.create_data import Data
from implementations.algorithmForEF1_CC_Plus import EF1_CC_Plus_Allocation_Algorithm
from implementations.algorithmForEFX_Bounded_Charity import EFX_Allocation_With_Bounded_Charity


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


# Function to check EF violations for charity
def check_ef_violations_on_charity(allocation, students):
    """
    Check for EF violations where a student envies the charity allocation.

    Parameters:
    - allocation (dict): A dictionary where keys are student IDs and values are lists of courses.
    - students (list): A list of student objects.

    Returns:
    - int: The count of EF violations with respect to charity.
    """
    ef_false_count = 0
    charity_allocation = allocation.get('charity', [])

    for student in students:
        if student.student_id == 'charity':
            continue

        own_courses_MWIS = MWIS(student, allocation.get(student.student_id, []))
        own_utility = sum(student.get_valuation_function().get(course.course_id, 0) for course in own_courses_MWIS)

        charity_courses_MWIS = MWIS(student, charity_allocation)
        charity_utility = sum(student.get_valuation_function().get(course.course_id, 0) for course in charity_courses_MWIS)

        if charity_utility > own_utility:
            ef_false_count += 1

    return ef_false_count

# Initialize parameters
num_courses = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160]  # Number of courses
fixed_students = 40  # Fixed number of students
num_iterations = 5  # Number of iterations for averaging

# Arrays to store EF violations with respect to charity
all_ef_violations_efx_charity = np.zeros((num_iterations, len(num_courses)))
all_ef_violations_ef1_charity = np.zeros((num_iterations, len(num_courses)))

# Run experiments for increasing courses
for iteration in range(num_iterations):
    print(f"Iteration {iteration + 1}/{num_iterations}")
    for i, num_course in enumerate(num_courses):
        data = Data(num_course, fixed_students, total_school_time=30, reproducible=False)

        # Generate students and courses
        students = data.get_students()
        courses = data.get_courses()

        # Calculate EF violations for Bhaskar's Algorithm with respect to charity
        allocation_efx = EFX_Allocation_With_Bounded_Charity(students, courses)
        ef_violation_count_efx_charity = check_ef_violations_on_charity(allocation_efx, students)
        all_ef_violations_efx_charity[iteration, i] = ef_violation_count_efx_charity

        # Calculate EF violations for EF1_CC_Plus_Allocation_Algorithm with respect to charity
        allocation_ef1 = EF1_CC_Plus_Allocation_Algorithm(students, courses)
        ef_violation_count_ef1_charity = check_ef_violations_on_charity(allocation_ef1, students)
        all_ef_violations_ef1_charity[iteration, i] = ef_violation_count_ef1_charity

        print(f"{num_course} courses completed for iteration {iteration + 1}")

# Calculate means and standard deviations
mean_ef_violations_efx_charity = np.mean(all_ef_violations_efx_charity, axis=0)
mean_ef_violations_ef1_charity = np.mean(all_ef_violations_ef1_charity, axis=0)
std_ef_violations_efx_charity = np.std(all_ef_violations_efx_charity, axis=0, ddof=1)
std_ef_violations_ef1_charity = np.std(all_ef_violations_ef1_charity, axis=0, ddof=1)

# Plot EF violations comparison with averages (Charity)
plt.figure(figsize=(10, 6))
plt.plot(num_courses, mean_ef_violations_efx_charity, marker='o', label="Average EF Violations to Charity (Bhaskar's Algorithm)")
plt.plot(num_courses, mean_ef_violations_ef1_charity, marker='x', label="Average EF Violations to Charity (Our Algorithm)")
plt.title("Average EF Violations to Charity as Number of Courses Increases (40 Students Fixed)")
plt.xlabel("Number of Courses")
plt.ylabel("Average Number of EF Violations to Charity")
plt.legend()
plt.grid(True)
plt.show()

# Print standard deviations for charity violations for both algorithms
for i, num_course in enumerate(num_courses):
    print(f"Courses: {num_course}")
    print(f"  Bhaskar's Algorithm to Charity - Std Dev: {std_ef_violations_efx_charity[i]:.4f}")
    print(f"  Our Algorithm to Charity - Std Dev: {std_ef_violations_ef1_charity[i]:.4f}")
