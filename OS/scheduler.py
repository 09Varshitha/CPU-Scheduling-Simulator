from process import Process
from typing import List, Tuple
import copy

class Scheduler:
    def __init__(self):
        self.timeline = []  # List of (time, process_id) tuples for Gantt chart
        
    def fcfs(self, processes: List[Process]) -> List[Tuple[int, str]]:
        """First Come First Serve scheduling"""
        processes = sorted(processes, key=lambda p: p.arrival_time)
        current_time = 0
        self.timeline = []
        
        for process in processes:
            process.reset()
            if current_time < process.arrival_time:
                self.timeline.append((current_time, "idle"))
                current_time = process.arrival_time
                
            process.start_time = current_time
            process.completion_time = current_time + process.burst_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            
            self.timeline.append((current_time, f"P{process.pid}"))
            current_time = process.completion_time
            
        return self.timeline
    
    def sjf(self, processes: List[Process]) -> List[Tuple[int, str]]:
        """Shortest Job First scheduling (non-preemptive)"""
        processes = copy.deepcopy(processes)
        current_time = 0
        self.timeline = []
        remaining_processes = sorted(processes, key=lambda p: p.arrival_time)
        
        while remaining_processes:
            available_processes = [p for p in remaining_processes if p.arrival_time <= current_time]
            
            if not available_processes:
                self.timeline.append((current_time, "idle"))
                current_time = min(p.arrival_time for p in remaining_processes)
                continue
                
            process = min(available_processes, key=lambda p: p.burst_time)
            process.start_time = current_time
            process.completion_time = current_time + process.burst_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            
            self.timeline.append((current_time, f"P{process.pid}"))
            current_time = process.completion_time
            remaining_processes.remove(process)
            
        return self.timeline
    
    def round_robin(self, processes: List[Process], time_quantum: int) -> List[Tuple[int, str]]:
        """Round Robin scheduling"""
        processes = copy.deepcopy(processes)
        current_time = 0
        self.timeline = []
        remaining_processes = sorted(processes, key=lambda p: p.arrival_time)
        ready_queue = []
        
        while remaining_processes or ready_queue:
            # Add newly arrived processes to ready queue
            while remaining_processes and remaining_processes[0].arrival_time <= current_time:
                ready_queue.append(remaining_processes.pop(0))
                
            if not ready_queue:
                self.timeline.append((current_time, "idle"))
                current_time = remaining_processes[0].arrival_time
                continue
                
            process = ready_queue.pop(0)
            execution_time = min(time_quantum, process.remaining_time)
            
            if process.remaining_time == process.burst_time:
                process.start_time = current_time
                
            self.timeline.append((current_time, f"P{process.pid}"))
            current_time += execution_time
            process.remaining_time -= execution_time
            
            # Add newly arrived processes that arrived during this time quantum
            while remaining_processes and remaining_processes[0].arrival_time <= current_time:
                ready_queue.append(remaining_processes.pop(0))
                
            if process.remaining_time > 0:
                ready_queue.append(process)
            else:
                process.completion_time = current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                
        return self.timeline
    
    def priority(self, processes: List[Process]) -> List[Tuple[int, str]]:
        """Priority scheduling (non-preemptive)"""
        processes = copy.deepcopy(processes)
        current_time = 0
        self.timeline = []
        remaining_processes = sorted(processes, key=lambda p: p.arrival_time)
        
        while remaining_processes:
            available_processes = [p for p in remaining_processes if p.arrival_time <= current_time]
            
            if not available_processes:
                self.timeline.append((current_time, "idle"))
                current_time = min(p.arrival_time for p in remaining_processes)
                continue
                
            # Lower priority number means higher priority
            process = min(available_processes, key=lambda p: p.priority)
            process.start_time = current_time
            process.completion_time = current_time + process.burst_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            
            self.timeline.append((current_time, f"P{process.pid}"))
            current_time = process.completion_time
            remaining_processes.remove(process)
            
        return self.timeline
    
    @staticmethod
    def calculate_metrics(processes: List[Process]) -> Tuple[float, float]:
        """Calculate average waiting time and average turnaround time"""
        avg_waiting_time = sum(p.waiting_time for p in processes) / len(processes)
        avg_turnaround_time = sum(p.turnaround_time for p in processes) / len(processes)
        return avg_waiting_time, avg_turnaround_time 




