from classes.course import Course
from classes.student import Student
from classes.create_data import Data
import random
import time
import matplotlib.pyplot as plt
from classes.create_data import Data
from implementations.algorithmForEF1_CC_Plus import EF1_CC_Plus_Allocation_Algorithm
from implementations.algorithmForEFX_Bounded_Charity import EFX_Allocation_With_Bounded_Charity
from implementations.algorithmForEFX_Bounded_Charity_U1 import EFX_Allocation_With_Bounded_Charity_U1
from implementations.envy_graph_elimination import Envy_Graph_Elimination
from implementations.checker import is_ef, is_ef1, is_efx

data = {
  "valuations": {
    "s1": {"c1": 152, "c2": 86, "c3": 262, "c4": 68, "c5": 263, "c6": 169},
    "s2": {"c1": 124, "c2": 70, "c3": 98, "c4": 244, "c5": 329, "c6": 135},
    "s3": {"c1": 170, "c2": 235, "c3": 295, "c4": 91, "c5": 91, "c6": 118},
    "s4": {"c1": 158, "c2": 56, "c3": 134, "c4": 255, "c5": 192, "c6": 205}
    } ,"agent_capacities": {"s1": 23, "s2": 23, "s3": 23, "s4": 23},
  "item_capacities": {"c1": 5, "c2": 6, "c3": 2, "c4": 3, "c5": 5, "c6": 2}
}
# Create a Data instance

total_school_time = 10  # Example total time, can be adjusted
custom_data = Data(0, 0, total_school_time)

# Manually add courses with randomized start and end times
#for course_id in range(1, 7):
    #start_time = random.randint(0, total_school_time - 3)
    #end_time = start_time + random.randint(1, 3)
    #seat_capacity = {"c1": 5, "c2": 6, "c3": 2, "c4": 3, "c5": 5, "c6": 2}[f"c{course_id}"]
    #for i in range(0, seat_capacity):
        #custom_data.add_course(course_id=f"c{course_id}", credits=1, seat_capacity=1, start_time=start_time, end_time=end_time)

# Add courses with specific start and end times
for i in range(0, 5):
    custom_data.add_course(course_id="c1", credits=1, seat_capacity=1, start_time=5, end_time=8)
for i in range(0, 6):
    custom_data.add_course(course_id="c2", credits=1, seat_capacity=1, start_time=7, end_time=9)
for i in range(0, 2):
    custom_data.add_course(course_id="c3", credits=1, seat_capacity=1, start_time=6, end_time=9)
for i in range(0, 3):
    custom_data.add_course(course_id="c4", credits=1, seat_capacity=1, start_time=0, end_time=3)
for i in range(0, 5):
    custom_data.add_course(course_id="c5", credits=1, seat_capacity=1, start_time=7, end_time=10)
for i in range(0, 2):
    custom_data.add_course(course_id="c6", credits=1, seat_capacity=1, start_time=4, end_time=6)

# Manually add students based on the given data
custom_data.add_student(
    student_id="s1",
    valuation_function={"c1": 152, "c2": 86, "c3": 262, "c4": 68, "c5": 263, "c6": 169},
    credit_cap=23
)
custom_data.add_student(
    student_id="s2",
    valuation_function={"c1": 124, "c2": 70, "c3": 98, "c4": 244, "c5": 329, "c6": 135},
    credit_cap=23
)
custom_data.add_student(
    student_id="s3",
    valuation_function={"c1": 170, "c2": 235, "c3": 295, "c4": 91, "c5": 91, "c6": 118},
    credit_cap=23
)
custom_data.add_student(
    student_id="s4",
    valuation_function={"c1": 158, "c2": 56, "c3": 134, "c4": 255, "c5": 192, "c6": 205},
    credit_cap=23
)

students = custom_data.get_students()
courses = custom_data.get_courses()

start = time.time()
allocation1 = EFX_Allocation_With_Bounded_Charity(students, courses)
end = time.time()
print("Total Time Taken for CKMS: " + str(end - start) + " seconds")
start = time.time()
allocation2 = EF1_CC_Plus_Allocation_Algorithm(students, courses)
end = time.time()
print("Total Time Taken for EGGI " + str(end - start) + " seconds")
start = time.time()
allocation3 = Envy_Graph_Elimination(students, courses)
end = time.time()
print("Total Time Taken for EGE: " + str(end - start) + " seconds")
start = time.time()
allocation4 = EFX_Allocation_With_Bounded_Charity_U1(students, courses)
end = time.time()
print("Total Time Taken for U1: " + str(end - start) + " seconds")

print("CKMS ALGORITHM -----------------")
#Lets find the social welfare of our allocation:
if allocation1['charity']:
    # Only compute max if there are students and courses in the 'charity' allocation
    maxValueOfCharity = max(
        student.get_valuation_function().get(course.course_id, 0) 
        for course in allocation1['charity'] 
        for student in students
    )
else:
    maxValueOfCharity = 0 
# Check for EF, EF1, and EFX
print("Is EF:", is_ef(allocation1, students))
print("Is EF1:", is_ef1(allocation1, students)) 
print("Is EFX:", is_efx(allocation1, students))
print("Maximum Value of Charity from any Student Valuation Function:", maxValueOfCharity)

# Print the assignments and utility for each student
for student in students:
    assigned_courses = allocation1[student.student_id]
    utility = student.utility(allocation1)
    course_details = [
        f"Course {course.course_id} (Start: {course.start_time}, End: {course.end_time})"
        for course in assigned_courses
    ]
    valuation_function_details = {
        course_id: value for course_id, value in student.valuation_function.items()
    }
    
    print(f"Student {student.student_id} assigned courses: {course_details}, Utility: {utility}")


print("EGGI ALGORITHM -----------------")

#Lets find the social welfare of our allocation:

if allocation2['charity']:
    # Only compute max if there are students and courses in the 'charity' allocation
    maxValueOfCharity = max(
        student.get_valuation_function().get(course.course_id, 0) 
        for course in allocation2['charity'] 
        for student in students
    )
else:
    maxValueOfCharity = 0 


# Check for EF, EF1, and EFX
print("Is EF:", is_ef(allocation2, students))
print("Is EF1:", is_ef1(allocation2, students)) 
print("Is EFX:", is_efx(allocation2, students))
print("Maximum Value of Charity from any Student Valuation Function:", maxValueOfCharity)

#What is Envy Ratio?

# Print the assignments and utility for each student
for student in students:
    assigned_courses = allocation2[student.student_id]
    utility = student.utility(allocation2)
    course_details = [
        f"Course {course.course_id} (Start: {course.start_time}, End: {course.end_time})"
        for course in assigned_courses
    ]
    valuation_function_details = {
        course_id: value for course_id, value in student.valuation_function.items()
    }
    
    print(f"Student {student.student_id} assigned courses: {course_details}, Utility: {utility}")

print("EGE ALGORITHM -----------------")

#Lets find the social welfare of our allocation:
if allocation3['charity']:
    # Only compute max if there are students and courses in the 'charity' allocation
    maxValueOfCharity = max(
        student.get_valuation_function().get(course.course_id, 0) 
        for course in allocation3['charity'] 
        for student in students
    )
else:
    maxValueOfCharity = 0 


# Check for EF, EF1, and EFX
print("Is EF:", is_ef(allocation3, students))
print("Is EF1:", is_ef1(allocation3, students)) 
print("Is EFX:", is_efx(allocation3, students))
print("Maximum Value of Charity from any Student Valuation Function:", maxValueOfCharity)

#What is Envy Ratio?

# Print the assignments and utility for each student
for student in students:
    assigned_courses = allocation3[student.student_id]
    utility = student.utility(allocation2)
    course_details = [
        f"Course {course.course_id} (Start: {course.start_time}, End: {course.end_time})"
        for course in assigned_courses
    ]
    valuation_function_details = {
        course_id: value for course_id, value in student.valuation_function.items()
    }
    
    print(f"Student {student.student_id} assigned courses: {course_details}, Utility: {utility}")

print("U1 ALGORITHM -----------------")

#Lets find the social welfare of our allocation:
if allocation4['charity']:
    # Only compute max if there are students and courses in the 'charity' allocation
    maxValueOfCharity = max(
        student.get_valuation_function().get(course.course_id, 0) 
        for course in allocation4['charity'] 
        for student in students
    )
else:
    maxValueOfCharity = 0 


# Check for EF, EF1, and EFX
print("Is EF:", is_ef(allocation4, students))
print("Is EF1:", is_ef1(allocation4, students)) 
print("Is EFX:", is_efx(allocation4, students))
print("Maximum Value of Charity from any Student Valuation Function:", maxValueOfCharity)

#What is Envy Ratio?

# Print the assignments and utility for each student
for student in students:
    assigned_courses = allocation4[student.student_id]
    utility = student.utility(allocation4)
    course_details = [
        f"Course {course.course_id} (Start: {course.start_time}, End: {course.end_time})"
        for course in assigned_courses
    ]
    valuation_function_details = {
        course_id: value for course_id, value in student.valuation_function.items()
    }
    
    print(f"Student {student.student_id} assigned courses: {course_details}, Utility: {utility}")

