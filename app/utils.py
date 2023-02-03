class Day():
    def __init__(self, date: str, available_status: bool or None, day_of_the_week: str):
        self.date = date
        self.available_status = available_status
        self.day_of_the_week = day_of_the_week