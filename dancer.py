class Dancer:
    def __init__(self, name):
        self.name = name
        self.dances = 1
        self.dances_done = 0
        self.time_since_last_dance = float('inf')

    def add_dance(self):
        self.dances += 1
    
    def schedule_dance(self):
        self.dances_done += 1
        self.time_since_last_dance = 0
    
    def __str__(self):
        return f"{self.name}"