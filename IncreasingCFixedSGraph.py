import time
import numpy as np
import matplotlib.pyplot as plt
from classes.create_data import Data
from implementations.algorithmForEF1_CC_Plus import EF1_CC_Plus_Allocation_Algorithm
from implementations.algorithmForEFX_Bounded_Charity import EFX_Allocation_With_Bounded_Charity
from implementations.Greedy_Round_Robin import Greedy_Round_Robin

# Initialize parameters
num_courses = range(50, 210, 10)  # Courses from 50 to 160, increment by 10
fixed_students = 40
num_iterations = 10

# Arrays to store runtimes
all_runtimes_efx_courses = np.zeros((num_iterations, len(num_courses)))
all_runtimes_ef1_courses = np.zeros((num_iterations, len(num_courses)))
all_runtimes_greedy_courses = np.zeros((num_iterations, len(num_courses)))

# Run experiments
for iteration in range(num_iterations):
    print(f"Iteration {iteration + 1}/{num_iterations}")
    for i, courses_count in enumerate(num_courses):
        data = Data(courses_count, fixed_students, total_school_time=30, reproducible=False)
        students = data.get_students()
        courses = data.get_courses()

        # Measure runtime for Bhaskar's Algorithm
        print(f"Running Bhaskar's Algorithm for {courses_count} courses")
        start_time = time.time()
        _ = EFX_Allocation_With_Bounded_Charity(students, courses)
        efx_runtime = time.time() - start_time
        all_runtimes_efx_courses[iteration, i] = efx_runtime

        # Measure runtime for EF1_CC_Plus Algorithm
        print(f"Running EF1_CC_Plus Algorithm for {courses_count} courses")
        start_time = time.time()
        _ = EF1_CC_Plus_Allocation_Algorithm(students, courses)
        ef1_runtime = time.time() - start_time
        all_runtimes_ef1_courses[iteration, i] = ef1_runtime

        # Measure runtime for Greedy Round Robin
        print(f"Running Greedy Round Robin for {courses_count} courses")
        start_time = time.time()
        _ = Greedy_Round_Robin(students, courses)
        greedy_runtime = time.time() - start_time
        all_runtimes_greedy_courses[iteration, i] = greedy_runtime

# Calculate means and standard deviations
mean_runtimes_efx_courses = np.mean(all_runtimes_efx_courses, axis=0)
mean_runtimes_ef1_courses = np.mean(all_runtimes_ef1_courses, axis=0)
mean_runtimes_greedy_courses = np.mean(all_runtimes_greedy_courses, axis=0)
std_runtimes_efx_courses = np.std(all_runtimes_efx_courses, axis=0, ddof=1)
std_runtimes_ef1_courses = np.std(all_runtimes_ef1_courses, axis=0, ddof=1)
std_runtimes_greedy_courses = np.std(all_runtimes_greedy_courses, axis=0, ddof=1)


# Plot runtime comparison with error bars
plt.figure(figsize=(10, 6))

# Plot EGGI (Our Algorithm) with error bars
plt.errorbar(
    num_courses, 
    mean_runtimes_ef1_courses, 
    yerr=std_runtimes_ef1_courses, 
    fmt='x-', 
    capsize=5, 
    label="EGGI"
)

# Plot CKMS (Bhaskar's Algorithm) with error bars
plt.errorbar(
    num_courses, 
    mean_runtimes_efx_courses, 
    yerr=std_runtimes_efx_courses, 
    fmt='o-', 
    capsize=5, 
    label="CKMS"
)

# Plot GRR (Greedy Round Robin) with error bars
plt.errorbar(
    num_courses, 
    mean_runtimes_greedy_courses, 
    yerr=std_runtimes_greedy_courses, 
    fmt='s-', 
    capsize=5, 
    label="GRR"
)

# Add plot title and labels
plt.title("Average Runtime Comparison (40 Students)")
plt.xlabel("Number of Courses")
plt.ylabel("Runtime (seconds)")
plt.xticks(ticks=num_courses, labels=num_courses)  # Set x-axis ticks and labels explicitly
plt.legend()
plt.grid(False)
plt.show()

num_courses = list(num_courses)
