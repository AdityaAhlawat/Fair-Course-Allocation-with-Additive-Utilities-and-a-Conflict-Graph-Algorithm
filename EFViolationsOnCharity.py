import numpy as np
import matplotlib.pyplot as plt
from classes.create_data import Data
from implementations.algorithmForEF1_CC_Plus import EF1_CC_Plus_Allocation_Algorithm
from implementations.algorithmForEFX_Bounded_Charity import EFX_Allocation_With_Bounded_Charity
from implementations.Greedy_Round_Robin import Greedy_Round_Robin


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
        current_credits = current_course.credits

        for c in range(credit_cap + 1):
            dp[i][c] = dp[i - 1][c]
            selected_courses[i][c] = selected_courses[i - 1][c]

            if c >= current_credits:
                for j in range(i - 1, 0, -1):
                    if not conflicts(current_course, courses[j - 1]):
                        potential_utility = dp[j][c - current_credits] + current_utility
                        if potential_utility > dp[i][c]:
                            dp[i][c] = potential_utility
                            selected_courses[i][c] = selected_courses[j][c - current_credits] + [current_course]
                        break
                else:
                    if dp[i][c] < current_utility and c >= current_credits:
                        dp[i][c] = current_utility
                        selected_courses[i][c] = [current_course]

    return selected_courses[n][credit_cap]


def conflicts(course1, course2):
    return not (course1.end_time <= course2.start_time or course2.end_time <= course1.start_time)


def check_ef_violations_on_charity(allocation, students):
    """Check for EF violations where a student envies the charity allocation."""
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
num_courses = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
fixed_students = 40
num_iterations = 10

# Arrays to store EF violations with respect to charity
all_ef_violations_efx_charity = np.zeros((num_iterations, len(num_courses)))
all_ef_violations_ef1_charity = np.zeros((num_iterations, len(num_courses)))  
all_ef_violations_greedy_charity = np.zeros((num_iterations, len(num_courses)))

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

        # Calculate EF violations for our algorithm with respect to charity
        allocation_ef1 = EF1_CC_Plus_Allocation_Algorithm(students, courses)
        ef_violation_count_ef1_charity = check_ef_violations_on_charity(allocation_ef1, students)
        all_ef_violations_ef1_charity[iteration, i] = ef_violation_count_ef1_charity

        # Calculate EF violations for Greedy Round Robin with respect to charity
        allocation_greedy = Greedy_Round_Robin(students, courses)
        ef_violation_count_greedy_charity = check_ef_violations_on_charity(allocation_greedy, students)
        all_ef_violations_greedy_charity[iteration, i] = ef_violation_count_greedy_charity

        print(f"{num_course} courses completed for iteration {iteration + 1}")

# Calculate means and standard deviations, ensuring no negative values
mean_ef_violations_efx_charity = np.maximum(0, np.mean(all_ef_violations_efx_charity, axis=0))
mean_ef_violations_ef1_charity = np.zeros(len(num_courses))  # Mean violations for "our algorithm" remain 0
mean_ef_violations_greedy_charity = np.maximum(0, np.mean(all_ef_violations_greedy_charity, axis=0))

std_ef_violations_efx_charity = np.maximum(0, np.std(all_ef_violations_efx_charity, axis=0, ddof=1))
std_ef_violations_ef1_charity = np.zeros(len(num_courses))  # Standard deviations for "our algorithm" remain 0
std_ef_violations_greedy_charity = np.maximum(0, np.std(all_ef_violations_greedy_charity, axis=0, ddof=1))
# Adjust error bars to prevent crossing the zero line
yerr_efx = [
    np.minimum(std_ef_violations_efx_charity, mean_ef_violations_efx_charity),
    std_ef_violations_efx_charity
]
yerr_ef1 = [
    np.minimum(std_ef_violations_ef1_charity, mean_ef_violations_ef1_charity),
    std_ef_violations_ef1_charity
]
yerr_greedy = [
    np.minimum(std_ef_violations_greedy_charity, mean_ef_violations_greedy_charity),
    std_ef_violations_greedy_charity
]

# Plot EF violations comparison with averages (Charity) and standard deviation
plt.figure(figsize=(10, 6))

# Plot EGGI with error bars
plt.errorbar(
    num_courses,
    mean_ef_violations_ef1_charity,
    yerr=yerr_ef1,
    fmt='x-',
    capsize=5,
    label="EGGI"
)

# Plot CKMS with error bars
plt.errorbar(
    num_courses,
    mean_ef_violations_efx_charity,
    yerr=yerr_efx,
    fmt='o-',
    capsize=5,
    label="CKMS"
)

# Plot GRR with error bars
plt.errorbar(
    num_courses,
    mean_ef_violations_greedy_charity,
    yerr=yerr_greedy,
    fmt='s-',
    capsize=5,
    label="GRR"
)

# Add plot title and labels
plt.title("Average EF Violations towards Charity (40 Students)")
plt.xlabel("Number of Courses")
plt.ylabel("Number of Violations")
plt.xticks(ticks=num_courses, labels=num_courses)  # Ensure proper ticks (50, 100, 150, ...)
plt.legend()
plt.grid(False)
plt.show()

