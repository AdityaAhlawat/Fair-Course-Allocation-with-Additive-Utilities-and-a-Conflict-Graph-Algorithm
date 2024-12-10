import time
import numpy as np
import matplotlib.pyplot as plt
from classes.create_data import Data
from implementations.algorithmForEF1_CC_Plus import EF1_CC_Plus_Allocation_Algorithm
from implementations.algorithmForEFX_Bounded_Charity import EFX_Allocation_With_Bounded_Charity

# Initialize parameters
num_courses = range(50, 170, 10)  # Courses from 50 to 160, increment by 10
fixed_students = 40
num_iterations = 5

# Arrays to store runtimes
all_runtimes_efx_courses = np.zeros((num_iterations, len(num_courses)))
all_runtimes_ef1_courses = np.zeros((num_iterations, len(num_courses)))

# Run experiments
for iteration in range(num_iterations):
    print(f"Iteration {iteration + 1}/{num_iterations}")
    for i, courses_count in enumerate(num_courses):
        data = Data(courses_count, fixed_students, total_school_time=30, reproducible=False)
        students = data.get_students()
        courses = data.get_courses()
        print(f"Doing Bhaskar's Algorithm for {courses_count} courses")
        # Measure runtime for Bhaskar's Algorithm
        start_time = time.time()
        _ = EFX_Allocation_With_Bounded_Charity(students, courses)
        efx_runtime = time.time() - start_time
        all_runtimes_efx_courses[iteration, i] = efx_runtime
        print(f"Doing EF1_CC_Plus Algorithm for {courses_count} courses")
        # Measure runtime for EF1_CC_Plus_Allocation_Algorithm
        start_time = time.time()
        _ = EF1_CC_Plus_Allocation_Algorithm(students, courses)
        ef1_runtime = time.time() - start_time
        all_runtimes_ef1_courses[iteration, i] = ef1_runtime

# Calculate means and standard deviations
mean_runtimes_efx_courses = np.mean(all_runtimes_efx_courses, axis=0)
mean_runtimes_ef1_courses = np.mean(all_runtimes_ef1_courses, axis=0)
std_runtimes_efx_courses = np.std(all_runtimes_efx_courses, axis=0, ddof=1)
std_runtimes_ef1_courses = np.std(all_runtimes_ef1_courses, axis=0, ddof=1)

# Plot runtime comparison without error bars
plt.figure(figsize=(10, 6))
plt.plot(num_courses, mean_runtimes_efx_courses, 'o-', label="Average Runtime (Bhaskar's Algorithm)")
plt.plot(num_courses, mean_runtimes_ef1_courses, 'x-', label="Average Runtime (Our Algorithm)")
plt.title("Average Runtime Comparison (Fixed Students)")
plt.xlabel("Number of Courses")
plt.ylabel("Runtime (seconds)")
plt.legend()
plt.grid(True)
plt.show()

# Print standard deviations for both algorithms
for i, courses_count in enumerate(num_courses):
    print(f"Courses: {courses_count}")
    print(f"  Bhaskar's Algorithm - Std Dev: {std_runtimes_efx_courses[i]:.4f}")
    print(f"  Our Algorithm - Std Dev: {std_runtimes_ef1_courses[i]:.4f}")
