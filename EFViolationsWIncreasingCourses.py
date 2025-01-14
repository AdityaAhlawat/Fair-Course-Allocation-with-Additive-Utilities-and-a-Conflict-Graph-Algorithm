import numpy as np
import matplotlib.pyplot as plt
from classes.create_data import Data
from implementations.algorithmForEF1_CC_Plus import EF1_CC_Plus_Allocation_Algorithm
from implementations.algorithmForEFX_Bounded_Charity import EFX_Allocation_With_Bounded_Charity
from implementations.Greedy_Round_Robin import Greedy_Round_Robin
from implementations.checker import is_ef

# Initialize parameters
num_courses = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]  # Number of courses
fixed_students = 40  # Fixed number of students
num_iterations = 10  # Number of iterations for averaging

# Arrays to store EF violations
all_ef_violations_efx = np.zeros((num_iterations, len(num_courses)))
all_ef_violations_ef1 = np.zeros((num_iterations, len(num_courses)))
all_ef_violations_greedy = np.zeros((num_iterations, len(num_courses)))

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

        # Calculate EF violations for Greedy Round Robin
        allocation_greedy = Greedy_Round_Robin(students, courses)
        _, ef_violation_count_greedy = is_ef(allocation_greedy, students)
        all_ef_violations_greedy[iteration, i] = ef_violation_count_greedy

        print(f"{num_course} courses completed for iteration {iteration + 1}")

# Calculate means and standard deviations, ensuring no negative values
mean_ef_violations_efx = np.maximum(0, np.mean(all_ef_violations_efx, axis=0))
mean_ef_violations_ef1 = np.maximum(0, np.mean(all_ef_violations_ef1, axis=0))
mean_ef_violations_greedy = np.maximum(0, np.mean(all_ef_violations_greedy, axis=0))

std_ef_violations_efx = np.maximum(0, np.std(all_ef_violations_efx, axis=0, ddof=1))
std_ef_violations_ef1 = np.maximum(0, np.std(all_ef_violations_ef1, axis=0, ddof=1))
std_ef_violations_greedy = np.maximum(0, np.std(all_ef_violations_greedy, axis=0, ddof=1))

# Plot EF violations comparison with averages and standard deviations
plt.figure(figsize=(10, 6))

# Plot EGGI with error bars
plt.errorbar(
    num_courses,
    mean_ef_violations_ef1,
    yerr=std_ef_violations_ef1,
    fmt='x-',
    capsize=5,
    label="EGGI"
)

# Plot CKMS with error bars
plt.errorbar(
    num_courses,
    mean_ef_violations_efx,
    yerr=std_ef_violations_efx,
    fmt='o-',
    capsize=5,
    label="CKMS"
)

# Plot GRR with error bars
plt.errorbar(
    num_courses,
    mean_ef_violations_greedy,
    yerr=std_ef_violations_greedy,
    fmt='s-',
    capsize=5,
    label="GRR"
)

# Add plot title and labels
plt.title("Average EF Violations among Students (40 Students)")
plt.xlabel("Number of Courses")
plt.ylabel("Number of Violations")

# Set x-axis ticks and labels to either 50, 100, 150, ... or 50, 150, 250, ...
plt.xticks(ticks=num_courses, labels=num_courses)
plt.legend()
plt.grid(False)
plt.show()

