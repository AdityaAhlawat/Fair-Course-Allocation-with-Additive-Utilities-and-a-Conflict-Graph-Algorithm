class Course:
    def __init__(self, course_id, credits, seat_capacity, start_time, end_time):
        self.course_id = course_id #Course ID to identify each Course Object.
        self.credits = credits
        self.seat_capacity = seat_capacity
        self.start_time = start_time
        self.end_time = end_time
        self.duration = end_time - start_time
        self.seat_count = 0

    def __repr__(self):
        return (f"Course(id={self.course_id}, credits={self.credits}, seat_capacity={self.seat_capacity}, "
                f"start_time={self.start_time}, end_time={self.end_time}, duration={self.duration}, "
                f"seat_count={self.seat_count})")

    def get_seat_capacity(self):
        return self.seat_capacity