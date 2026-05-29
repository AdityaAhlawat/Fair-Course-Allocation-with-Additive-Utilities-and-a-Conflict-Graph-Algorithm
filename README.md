This is the README file to reproduce the results in the submitted manuscript: Fair Course Allocation with Schedule Conflicts and Capacity Constraints. 

## Datasets
1. Synthetically generated datasets: The datasets were generated using the Course, Student, and Data classes (found in the Classes folder) which programmatically modeled course attributes (e.g., schedule, capacity) and student preferences (e.g., valuations, credit limits).
2. Real-world preferences: we use publicly available data from [fairpyx GitHub repository](https://github.com/ariel-research/fairpyx/blob/main/experiments/data/)


## Algorithms to compare (in the folder called `implementations`)
1. `algorithmForEF1_CC_Plus.py`: Our algorithm (EGGI)
2. `algorithmForEFX_Bounded_Charity.py`: Implementation of the algorithm in Chaudhury et al. 2021 (CKMS)
3. `envy_graph_elimination`: Implementation of a modified version of the algorithm in Lipton et al. 2004 (EGE)
4. `optimized.py`: Gurobi implementation of the optimal algorithm that maximizes the social welfare subject to the capacity, conflict, and fairness constraints in the course allocation problem. 


## For generating the results on synthetic datasets, the main files are (the graphs will appear after a few minutes. You can view progress of the graph generation from the terminal.)

1. `IncreasingCFixedSGraph.py`: Outputs a plot to compare the average runtimes considering 40 students and number of courses varying from 50 to 200. 

1. `IncreasingSFixedCGraph.py`: Outputs a plot to compare the average runtimes considering 200 courses and number of students varying from 5 to 50. 

2. `EFViolationsWIncreasingCourses.py`: Outputs a plot to compare the number of EF violations among students, when there are 40 students and number of courses varying from 50 to 200. 

3. `EFViolationsOnCharity.py`: Outputs a plot to compare the number of EF violations toward CHARITY, when there are 40 students and number of courses varying from 50 to 200. 


## For the results on real-world preference, the main files are:

1. `generate_timings.py`: Creates timings for the different courses in the dataset. The script takes course data and randomly generates start times, end times, and durations for the courses to gather the conflict information necessary for the optimizer. This file will produce the output `course_timings.json`.

2. `course_timings.json`: Defines the time slots and capacities for each course. This file uses the following structure:
```json
{
  "course_timings": {
    "course_name": {
      "start_time": int,
      "end_time": int,
      "duration": int,
      "capacity": int
    }
  }
}
```

3. SmallPublicDatasetResults.py: Outputs the runtime, social welfare, EF violations for the real-world preference dataset with 4 students and 6 courses using three algorithms --- our algorithm (EGGI), CKMS, and EGE.

4. LargePublicDatasetResults.py: Outputs the runtime, social welfare, EF violations for the real-world preference dataset with 26 students and 23 courses using three algorithms --- our algorithm (EGGI) and EGE. (EKMS is commented out since it failed to finish execution even after 2 days).

5. `optimized.py`: we use Gurobi to implement the optimal algorithm that maximizes the social welfare subject to the capacity, conflict, and fairness constraints in the course allocation problem. 

## Running the optimal solution
1. First, ensure your course timing data is properly formatted in course_timings.json

2. Generate the timings:
```bash
python generate_timings.py
```

3. Run the optimization:
```bash
python optimized.py
```

## Output of the optimal solution

The output contains
- Allocation details for each student
- Utility scores for assignments
- Number of envy-free violations
- Total runtime
- Total social welfare

## Gurobi overview and Setup
For reproducing our results, you'll need Gurobi with an academic license, which is free for university students and faculty. To get started:

1. Visit [Gurobi's academic page](www.gurobi.com/academia/academic-program-and-licenses/)
2. Register with your university email
3. Download Gurobi Optimizer
4. Request an academic license (automatic with university email)
5. Install Gurobi and its Python interface:
```bash
pip install gurobipy
```

## Troubleshooting

Common issues are usually related to Gurobi setup:
1. License problems - check that gurobi.lic is properly installed
2. Memory issues - the implementation requires at least 4GB of RAM
3. Runtime performance - can vary based on input size and system specs

For any license-related errors, verify your academic license is current and properly installed. Academic licenses need annual renewal, which can be done through the Gurobi website. Other more specific information for troubleshooting with Gurobi can be found on the [Gurobi Documentation](https://docs.gurobi.com/current/).
