import time
import numpy as np
import matplotlib.pyplot as plt
from classes.create_data import Data
from implementations.algorithmForEF1_CC_Plus import EF1_CC_Plus_Allocation_Algorithm
from implementations.algorithmForEFX_Bounded_Charity import EFX_Allocation_With_Bounded_Charity
from implementations.algorithmForEFX_Bounded_Charity_U1 import EFX_Allocation_With_Bounded_Charity_U1
from implementations.envy_graph_elimination import Envy_Graph_Elimination

# Initialize parameters
num_courses = range(50, 210, 10)  # Courses from 50 to 160, increment by 10
fixed_students = 40
num_iterations = 10

# Arrays to store runtimes
all_runtimes_efx_courses = np.zeros((num_iterations, len(num_courses)))
all_runtimes_ef1_courses = np.zeros((num_iterations, len(num_courses)))
all_runtimes_envy_graph_courses = np.zeros((num_iterations, len(num_courses)))
all_runtimes_u1_courses = np.zeros((num_iterations, len(num_courses)))

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

        # Measure runtime for Envy Graph Elimination
        print(f"Running Envy Graph Elimination for {courses_count} courses")
        start_time = time.time()
        _ = Envy_Graph_Elimination(students, courses)
        envy_graph_runtime = time.time() - start_time
        all_runtimes_envy_graph_courses[iteration, i] = envy_graph_runtime

        # Measure runtime for U1 Algorithm
        print(f"Running U1 Algorithm for {courses_count} courses")
        start_time = time.time()
        _ = EFX_Allocation_With_Bounded_Charity_U1(students, courses)
        u1_runtime = time.time() - start_time
        all_runtimes_u1_courses[iteration, i] = u1_runtime

# Calculate means and standard deviations
mean_runtimes_efx_courses = np.mean(all_runtimes_efx_courses, axis=0)
mean_runtimes_ef1_courses = np.mean(all_runtimes_ef1_courses, axis=0)
mean_runtimes_envy_graph_courses = np.mean(all_runtimes_envy_graph_courses, axis=0)
mean_runtimes_u1_courses = np.mean(all_runtimes_u1_courses, axis=0)
std_runtimes_efx_courses = np.std(all_runtimes_efx_courses, axis=0, ddof=1)
std_runtimes_ef1_courses = np.std(all_runtimes_ef1_courses, axis=0, ddof=1)
std_runtimes_envy_graph_courses = np.std(all_runtimes_envy_graph_courses, axis=0, ddof=1)
std_runtimes_u1_courses = np.std(all_runtimes_u1_courses, axis=0, ddof=1)

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

# Plot EGE (Envy Graph Elimination) with error bars
plt.errorbar(
    num_courses, 
    mean_runtimes_envy_graph_courses, 
    yerr=std_runtimes_envy_graph_courses, 
    fmt='s-', 
    capsize=5, 
    label="EGE"
)

# Plot U1 with error bars
plt.errorbar(
    num_courses, 
    mean_runtimes_u1_courses, 
    yerr=std_runtimes_u1_courses, 
    fmt='^-', 
    capsize=5, 
    label="U1"
)

# Add plot title and labels with larger font sizes
plt.title("Average Runtime Comparison (40 Students)", fontsize=20)  # Increased title size
plt.xlabel("Number of Courses", fontsize=18)  # Increased x-axis label size
plt.ylabel("Runtime (seconds)", fontsize=18)  # Increased y-axis label size

# Set x-axis ticks and labels with adjusted font size
plt.xticks(ticks=num_courses, labels=num_courses, fontsize=12)  # Adjust tick size
plt.yticks(fontsize=12)  # Adjust y-tick size

# Update legend font size
plt.legend(fontsize=17)  # Increased legend size
plt.grid(False)
plt.show()
