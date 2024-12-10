import time
import matplotlib.pyplot as plt
from classes.create_data import Data
from implementations.algorithmForEF1_CC_Plus import EF1_CC_Plus_Allocation_Algorithm
from implementations.algorithmForEFX_Bounded_Charity import EFX_Allocation_With_Bounded_Charity
from implementations.checker import is_ef, is_ef1, is_efx
import csv

#Generate data instance without auto-generated data
data = Data(40, 8000, total_school_time=30, reproducible=False)

#Graph of Time for Courses as they increase and fixed students (compared between both algorithms)
students = data.get_students()
courses = data.get_courses()
start = time.time()
# Perform round robin course assignment
allocation1 = EFX_Allocation_With_Bounded_Charity(students, courses)
end = time.time()
print("Total Time Taken for Bhaskar's Paper: " + str(end - start) + " seconds")
start = time.time()
allocation2 = EF1_CC_Plus_Allocation_Algorithm(students, courses)
end = time.time()
print("Total Time Taken for our Paper: " + str(end - start) + " seconds")


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

#What is Envy Ratio?

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


print("SECOND ALGORITHM")

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
