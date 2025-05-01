class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.start_time = 0
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        
    def reset(self):
        """Reset process state for new simulation"""
        self.remaining_time = self.burst_time
        self.start_time = 0
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        
    def __str__(self):
        return f"Process {self.pid} (Arrival: {self.arrival_time}, Burst: {self.burst_time}, Priority: {self.priority})" 

