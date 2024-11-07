import time

from classes.create_data import Data
from implementations.algorithmForEF1_CC_Plus import EF1_CC_Plus_Allocation_Algorithm
from implementations.checker import is_ef, is_ef1, is_efx
from implementations.algorithmForEFX_Bounded_Charity import EFX_Allocation_With_Bounded_Charity

# Generate data
data = Data(0, 0, 50, reproducible=True)
# Generate data instance without auto-generated data
#data = Data(62, 30, total_school_time=30, reproducible=True)

# Manually add courses based on the test case
data.add_course(course_id=1, credits=1, seat_capacity=1, start_time=0, end_time=1)  # Course valued at 5 for Student A
data.add_course(course_id=2, credits=1, seat_capacity=1, start_time=1, end_time=2)  # Course valued at 10 for Student A
data.add_course(course_id=3, credits=1, seat_capacity=1, start_time=2, end_time=3)  # Course valued at 16 for Student B
data.add_course(course_id=4, credits=1, seat_capacity=1, start_time=4, end_time=5) 
data.add_course(course_id=5, credits=1, seat_capacity=1, start_time=5, end_time=6) 
data.add_course(course_id=6, credits=1, seat_capacity=1, start_time=7, end_time=8) 
data.add_course(course_id=7, credits=1, seat_capacity=1, start_time=8, end_time=9) 

# # Create valuation functions and students
valuation_A = {1: 5, 2: 16, 3: 10, 4: 10, 5: 10, 6: 10, 7: 10}  # Student A values courses 1 and 2, not 3
valuation_B = {1: 5, 2: 16, 3: 10, 4: 10, 5:10, 6: 10, 7: 10}  # Student B values only course 3

# # Manually add students with their valuations
data.add_student(student_id=1, valuation_function=valuation_A, credit_cap=3)
data.add_student(student_id=2, valuation_function=valuation_B, credit_cap=3)

# Get students and courses
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


print("FIRST ALGORITHM")
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
