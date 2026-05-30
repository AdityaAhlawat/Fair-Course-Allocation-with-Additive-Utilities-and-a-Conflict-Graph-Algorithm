import numpy as np
import matplotlib.pyplot as plt
from classes.create_data import Data
from implementations.algorithmForEF1_CC_Plus import EF1_CC_Plus_Allocation_Algorithm
from implementations.algorithmForEFX_Bounded_Charity import EFX_Allocation_With_Bounded_Charity
from implementations.algorithmForEFX_Bounded_Charity_U1 import EFX_Allocation_With_Bounded_Charity_U1
from implementations.envy_graph_elimination import Envy_Graph_Elimination

# Initialize parameters
num_courses = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]  # Number of courses
fixed_students = 40  # Fixed number of students
num_iterations = 10  # Number of iterations for averaging


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

def is_ef(allocation, students):
    ef_false_count = 0
    for student in students:
        if student.student_id == 'charity':
            continue
        own_courses_MWIS = MWIS(student, allocation[student.student_id])
        own_utility = sum(student.get_valuation_function().get(course.course_id, 0) for course in own_courses_MWIS)
        for other_student in students:
            if student != other_student and other_student.student_id != 'charity':
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
    

# Arrays to store EF violations
all_ef_violations_efx = np.zeros((num_iterations, len(num_courses)))
all_ef_violations_ef1 = np.zeros((num_iterations, len(num_courses)))
all_ef_violations_count_envy = np.zeros((num_iterations, len(num_courses)))
all_ef_violations_u1 = np.zeros((num_iterations, len(num_courses)))

# Run experiments for increasing courses
for iteration in range(num_iterations):
    print(f"Iteration {iteration + 1}/{num_iterations}")
    for i, num_course in enumerate(num_courses):
        data = Data(num_course, fixed_students, total_school_time=30, reproducible=False)

        # Generate students and courses
        students = data.get_students()
        courses = data.get_courses()

        # Calculate EF violations for Bhaskar's Algorithm
        allocation_efx = EFX_Allocation_With_Bounded_Charity(students, courses)
        _, ef_violation_count_efx = is_ef(allocation_efx, students)
        all_ef_violations_efx[iteration, i] = ef_violation_count_efx

        # Calculate EF violations for EF1_CC_Plus_Allocation_Algorithm
        allocation_ef1 = EF1_CC_Plus_Allocation_Algorithm(students, courses)
        _, ef_violation_count_ef1 = is_ef(allocation_ef1, students)
        all_ef_violations_ef1[iteration, i] = ef_violation_count_ef1

        # Calculate EF violations for Envy Graph Elimination 
        allocation_envy_graph = Envy_Graph_Elimination(students, courses)
        _, ef_violation_count_envy_graph = is_ef(allocation_envy_graph, students)
        all_ef_violations_count_envy[iteration, i] = ef_violation_count_envy_graph

        # Calculate EF violations for U1 algorithm
        allocation_u1 = EFX_Allocation_With_Bounded_Charity_U1(students, courses)
        _, ef_violation_count_u1 = is_ef(allocation_u1, students)
        all_ef_violations_u1[iteration, i] = ef_violation_count_u1

        print(f"{num_course} courses completed for iteration {iteration + 1}")

# Calculate means and standard errors, ensuring no negative values
mean_ef_violations_efx = np.maximum(0, np.mean(all_ef_violations_efx, axis=0))
mean_ef_violations_ef1 = np.maximum(0, np.mean(all_ef_violations_ef1, axis=0))
mean_ef_violations_envy_graph = np.maximum(0, np.mean(all_ef_violations_count_envy, axis=0))
mean_ef_violations_u1 = np.maximum(0, np.mean(all_ef_violations_u1, axis=0))

stderr_ef_violations_efx = np.maximum(0, np.std(all_ef_violations_efx, axis=0, ddof=1) / np.sqrt(num_iterations))
stderr_ef_violations_ef1 = np.maximum(0, np.std(all_ef_violations_ef1, axis=0, ddof=1) / np.sqrt(num_iterations))
stderr_ef_violations_envy_graph = np.maximum(0, np.std(all_ef_violations_count_envy, axis=0, ddof=1) / np.sqrt(num_iterations))
stderr_ef_violations_u1 = np.maximum(0, np.std(all_ef_violations_u1, axis=0, ddof=1) / np.sqrt(num_iterations))

# Plot EF violations comparison with averages and standard error
plt.figure(figsize=(10, 6))

# Plot EGGI with error bars
plt.errorbar(
    num_courses,
    mean_ef_violations_ef1,
    yerr=stderr_ef_violations_ef1,
    fmt='x-',
    capsize=5,
    label="EGGI"
)

# Plot CKMS with error bars
plt.errorbar(
    num_courses,
    mean_ef_violations_efx,
    yerr=stderr_ef_violations_efx,
    fmt='o-',
    capsize=5,
    label="CKMS"
)

# Plot EGE with error bars (changed from GRR to EGE)
plt.errorbar(
    num_courses,
    mean_ef_violations_envy_graph,
    yerr=stderr_ef_violations_envy_graph,
    fmt='s-',
    capsize=5,
    label="EGE"
)

# Plot U1 with error bars
plt.errorbar(
    num_courses,
    mean_ef_violations_u1,
    yerr=stderr_ef_violations_u1,
    fmt='^-',
    capsize=5,
    label="U1"
)

# Add plot title and labels with larger font sizes
plt.title("Average EF Violations among Students (40 Students)", fontsize=20)  # Increased title size
plt.xlabel("Number of Courses", fontsize=18)  # Increased x-axis label size
plt.ylabel("Number of Violations", fontsize=18)  # Increased y-axis label size

# Set x-axis ticks and labels with adjusted font size
plt.xticks(ticks=num_courses, labels=num_courses, fontsize=12)  # Adjust tick size
plt.yticks(fontsize=12)  # Adjust y-tick size

# Update legend font size
plt.legend(fontsize=17)  # Increased legend size
plt.grid(False)
plt.show()
