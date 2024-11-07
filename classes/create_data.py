import random
from .course import Course
from .student import Student

class Data:
    def __init__(self, num_of_courses, num_of_students, total_school_time, reproducible: bool = False, seed: int = 42):
        self.num_of_courses = num_of_courses
        self.num_of_students = num_of_students
        self.courses = []
        self.students = []
        self.total_school_time = total_school_time
        self.reproducible = reproducible
        self.seed = seed  # Store seed for consistent behavior

        # Set the seed once if reproducibility is required
        if self.reproducible:
            random.seed(self.seed)

        # Automatically generate data only if user does not provide custom data
        if self.num_of_courses > 0 and self.num_of_students > 0:
            self._generate_courses()
            self._generate_students()

    def _generate_courses(self):
        """Generate courses with reproducibility if needed."""
        if self.reproducible:
            random.seed(self.seed)  # Reset the seed for reproducibility
        for i in range(self.num_of_courses):
            course_id = i + 1
            credits = 1  # Set credits to 1 as per the paper
            seat_capacity = 1  # Set seat capacity to 1 as per the paper
            start_time = random.randint(0, self.total_school_time - 3)
            end_time = start_time + random.randint(1, 3)
            course = Course(course_id, credits, seat_capacity, start_time, end_time)
            self.courses.append(course)

    def _generate_students(self):
        """Generate students with reproducibility if needed."""
        if self.reproducible:
            random.seed(self.seed + 1)  # Use a slightly different seed for student generation to avoid correlation
        for j in range(self.num_of_students):
            student_id = j + 1
            valuation_function = {course.course_id: random.randint(1, 10) for course in self.courses}
            credit_cap = random.randint(3, 6)
            student = Student(student_id, valuation_function, credit_cap)
            self.students.append(student)

    def get_students(self):
        return self.students

    def get_courses(self):
        return self.courses
    
    def add_course(self, course_id, credits, seat_capacity, start_time, end_time):
        course = Course(course_id, credits, seat_capacity, start_time, end_time)
        self.courses.append(course)
        self.num_of_courses = len(self.courses)

    def add_student(self, student_id, valuation_function, credit_cap):
        student = Student(student_id, valuation_function, credit_cap)
        self.students.append(student)
        self.num_of_students = len(self.students)

    def display_courses(self):
        # Display the courses in a tabular format
        print("{:<10} {:<10} {:<10} {:<10}".format('Course ID', 'Credits', 'Start Time', 'End Time'))
        print("-" * 40)
        for course in self.courses:
            print("{:<10} {:<10} {:<10} {:<10}".format(course.course_id, course.credits, course.start_time, course.end_time))

        # Display the courses on a timeline
        print("\nCourse Timings:")
        timeline = [" " * self.total_school_time for _ in range(len(self.courses))]
        for i, course in enumerate(self.courses):
            timeline[i] = timeline[i][:course.start_time] + "=" * (course.end_time - course.start_time) + timeline[i][course.end_time:]
            print("Course {}: {}".format(course.course_id, timeline[i]))
