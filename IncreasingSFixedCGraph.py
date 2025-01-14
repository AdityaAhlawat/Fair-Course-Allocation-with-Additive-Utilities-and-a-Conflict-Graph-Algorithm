import time
import numpy as np
import matplotlib.pyplot as plt
from classes.create_data import Data
from implementations.algorithmForEF1_CC_Plus import EF1_CC_Plus_Allocation_Algorithm
from implementations.algorithmForEFX_Bounded_Charity import EFX_Allocation_With_Bounded_Charity
from implementations.Greedy_Round_Robin import Greedy_Round_Robin

# Initialize parameters
num_students = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
fixed_courses = 200
num_iterations = 10

# Arrays to store runtimes
all_runtimes_efx = np.zeros((num_iterations, len(num_students)))
all_runtimes_ef1 = np.zeros((num_iterations, len(num_students)))
all_runtimes_greedy = np.zeros((num_iterations, len(num_students)))

# Run experiments
for iteration in range(num_iterations):
    print(f"Iteration {iteration + 1}/{num_iterations}")
    for i, students_count in enumerate(num_students):
        data = Data(fixed_courses, students_count, total_school_time=30, reproducible=False)
        students = data.get_students()
        courses = data.get_courses()

        # Measure runtime for Bhaskar's Algorithm
        print(f"Running Bhaskar's Algorithm for {students_count} students")
        start_time = time.time()
        _ = EFX_Allocation_With_Bounded_Charity(students, courses)
        efx_runtime = time.time() - start_time
        all_runtimes_efx[iteration, i] = efx_runtime

        # Measure runtime for EF1_CC_Plus Algorithm
        print(f"Running EF1_CC_Plus Algorithm for {students_count} students")
        start_time = time.time()
        _ = EF1_CC_Plus_Allocation_Algorithm(students, courses)
        ef1_runtime = time.time() - start_time
        all_runtimes_ef1[iteration, i] = ef1_runtime

        # Measure runtime for Greedy Round Robin
        print(f"Running Greedy Round Robin for {students_count} students")
        start_time = time.time()
        _ = Greedy_Round_Robin(students, courses)
        greedy_runtime = time.time() - start_time
        all_runtimes_greedy[iteration, i] = greedy_runtime

# Calculate means and standard deviations
mean_runtimes_efx = np.mean(all_runtimes_efx, axis=0)
mean_runtimes_ef1 = np.mean(all_runtimes_ef1, axis=0)
mean_runtimes_greedy = np.mean(all_runtimes_greedy, axis=0)
std_runtimes_efx = np.std(all_runtimes_efx, axis=0, ddof=1)
std_runtimes_ef1 = np.std(all_runtimes_ef1, axis=0, ddof=1)
std_runtimes_greedy = np.std(all_runtimes_greedy, axis=0, ddof=1)

# Plot runtime comparison with error bars
plt.figure(figsize=(10, 6))

# Plot EGGI (Our Algorithm) with error bars
plt.errorbar(
    num_students, 
    mean_runtimes_ef1, 
    yerr=std_runtimes_ef1, 
    fmt='x-', 
    capsize=5, 
    label="EGGI"
)

# Plot CKMS (Bhaskar's Algorithm) with error bars
plt.errorbar(
    num_students, 
    mean_runtimes_efx, 
    yerr=std_runtimes_efx, 
    fmt='o-', 
    capsize=5, 
    label="CKMS"
)

# Plot GRR (Greedy Round Robin) with error bars
plt.errorbar(
    num_students, 
    mean_runtimes_greedy, 
    yerr=std_runtimes_greedy, 
    fmt='s-', 
    capsize=5, 
    label="GRR"
)

# Add plot title and labels
plt.title("Average Runtime Comparison (200 Courses)")
plt.xlabel("Number of Students")
plt.ylabel("Runtime (seconds)")

# Set x-axis ticks and labels
plt.xticks(ticks=num_students, labels=num_students)  # Choose 5, 10, 15, ... or 5, 15, 25, ... based on your preference
plt.legend()
plt.grid(False)
plt.show()

