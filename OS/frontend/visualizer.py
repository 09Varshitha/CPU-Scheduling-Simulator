import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple
from backend.process import Process

class Visualizer:
    def __init__(self):
        self.colors = plt.cm.Set3(np.linspace(0, 1, 12))  # Color palette for processes
        
    def create_gantt_chart(self, timeline: List[Tuple[int, str]], title: str):
        """Create a Gantt chart visualization"""
        fig, ax = plt.subplots(figsize=(12, 4))
        
        # Process the timeline data
        processes = {}
        current_time = timeline[0][0]
        
        for i in range(len(timeline)):
            start_time = timeline[i][0]
            end_time = timeline[i+1][0] if i < len(timeline)-1 else start_time + 1
            process_id = timeline[i][1]
            
            if process_id == "idle":
                color = 'lightgray'
            else:
                if process_id not in processes:
                    processes[process_id] = len(processes)
                color = self.colors[processes[process_id] % len(self.colors)]
                
            ax.barh(y=0, width=end_time-start_time, left=start_time, 
                   color=color, edgecolor='black', alpha=0.7)
            
            # Add process labels
            ax.text(start_time + (end_time-start_time)/2, 0, 
                   process_id, ha='center', va='center')
        
        # Customize the chart
        ax.set_xlabel('Time')
        ax.set_title(title)
        ax.set_yticks([])
        ax.grid(True, axis='x')
        
        return fig
    
    def display_metrics(self, processes: List[Process], algorithm_name: str):
        """Display performance metrics"""
        avg_waiting_time = sum(p.waiting_time for p in processes) / len(processes)
        avg_turnaround_time = sum(p.turnaround_time for p in processes) / len(processes)
        
        fig, ax = plt.subplots(figsize=(8, 4))
        metrics = ['Avg Waiting Time', 'Avg Turnaround Time']
        values = [avg_waiting_time, avg_turnaround_time]
        
        ax.bar(metrics, values, color=['skyblue', 'lightgreen'])
        ax.set_title(f'{algorithm_name} - Performance Metrics')
        ax.grid(True, axis='y')
        
        # Add value labels on top of bars
        for i, v in enumerate(values):
            ax.text(i, v, f'{v:.2f}', ha='center', va='bottom')
            
        return fig
    
    def compare_algorithms(self, metrics_dict: dict):
        """Compare different algorithms using bar charts"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        algorithms = list(metrics_dict.keys())
        waiting_times = [metrics_dict[alg]['avg_waiting_time'] for alg in algorithms]
        turnaround_times = [metrics_dict[alg]['avg_turnaround_time'] for alg in algorithms]
        
        # Waiting time comparison
        ax1.bar(algorithms, waiting_times, color='skyblue')
        ax1.set_title('Average Waiting Time Comparison')
        ax1.grid(True, axis='y')
        ax1.set_ylabel('Time')
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        
        # Turnaround time comparison
        ax2.bar(algorithms, turnaround_times, color='lightgreen')
        ax2.set_title('Average Turnaround Time Comparison')
        ax2.grid(True, axis='y')
        ax2.set_ylabel('Time')
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        return fig 




