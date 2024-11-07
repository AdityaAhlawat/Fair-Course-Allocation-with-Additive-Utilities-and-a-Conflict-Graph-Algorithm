class Student:
    def __init__(self, student_id, valuation_function, credit_cap):
        self.student_id = student_id  # Student ID is used just so we can uniquely identify each Student Object.
        self.valuation_function = valuation_function  # Utility should be a dictionary where keys are course_ids and values are utility values
        self.credit_cap = credit_cap

    def __repr__(self):
        return (f"Student(id={self.student_id}, valuation_function={self.valuation_function}, credit_cap={self.credit_cap})")
    
    def utility(self, allocation):
        return sum(self.valuation_function.get(course.course_id, 0) for course in allocation[self.student_id])
    
    def get_credit_cap(self):
        return self.credit_cap
    
    def get_id(self):
        return self.student_id
    
    def get_valuation_function(self):
        return self.valuation_function


