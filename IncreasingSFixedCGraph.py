import time
import numpy as np
import matplotlib.pyplot as plt
from classes.create_data import Data
from implementations.algorithmForEF1_CC_Plus import EF1_CC_Plus_Allocation_Algorithm
from implementations.algorithmForEFX_Bounded_Charity import EFX_Allocation_With_Bounded_Charity

# Initialize parameters
num_students = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
fixed_courses = 200
num_iterations = 5

# Arrays to store runtimes
all_runtimes_efx = np.zeros((num_iterations, len(num_students)))
all_runtimes_ef1 = np.zeros((num_iterations, len(num_students)))

# Run experiments
for iteration in range(num_iterations):
    print(f"Iteration {iteration + 1}/{num_iterations}")
    for i, students_count in enumerate(num_students):
        data = Data(fixed_courses, students_count, total_school_time=30, reproducible=False)
        students = data.get_students()
        courses = data.get_courses()
        print(f"Doing Bhaskar's Algorithm for {students_count}")
        # Measure runtime for Bhaskar's Algorithm
        start_time = time.time()
        _ = EFX_Allocation_With_Bounded_Charity(students, courses)
        efx_runtime = time.time() - start_time
        all_runtimes_efx[iteration, i] = efx_runtime
        print(f"Doing EF1_CC_Plus Algorithm for {students_count}")
        # Measure runtime for EF1_CC_Plus_Allocation_Algorithm
        start_time = time.time()
        _ = EF1_CC_Plus_Allocation_Algorithm(students, courses)
        ef1_runtime = time.time() - start_time
        all_runtimes_ef1[iteration, i] = ef1_runtime

# Calculate means and standard deviations
mean_runtimes_efx = np.mean(all_runtimes_efx, axis=0)
mean_runtimes_ef1 = np.mean(all_runtimes_ef1, axis=0)
std_runtimes_efx = np.std(all_runtimes_efx, axis=0, ddof=1)
std_runtimes_ef1 = np.std(all_runtimes_ef1, axis=0, ddof=1)

# Plot runtime comparison without error bars
plt.figure(figsize=(10, 6))
plt.plot(num_students, mean_runtimes_efx, 'o-', label="Average Runtime (Bhaskar's Algorithm)")
plt.plot(num_students, mean_runtimes_ef1, 'x-', label="Average Runtime (Our Algorithm)")
plt.title("Average Runtime Comparison (Fixed Courses)")
plt.xlabel("Number of Students")
plt.ylabel("Runtime (seconds)")
plt.legend()
plt.grid(True)
plt.show()

# Print standard deviations for both algorithms
for i, students_count in enumerate(num_students):
    print(f"Students: {students_count}")
    print(f"  Bhaskar's Algorithm - Std Dev: {std_runtimes_efx[i]:.4f}")
    print(f"  Our Algorithm - Std Dev: {std_runtimes_ef1[i]:.4f}")
