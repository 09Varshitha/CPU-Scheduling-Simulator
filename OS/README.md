# Intelligent CPU Scheduler Simulator

This project implements a visual CPU scheduling algorithm simulator that demonstrates various scheduling algorithms including:
- First Come First Serve (FCFS)
- Shortest Job First (SJF)
- Round Robin (RR)
- Priority Scheduling

## Features
- Interactive GUI for process input
- Real-time Gantt chart visualization
- Performance metrics calculation
- Support for multiple scheduling algorithms
- Visual comparison of different algorithms

## Requirements
- Python 3.8+
- Required packages listed in requirements.txt

## Setup
1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the simulator:
   ```
   python main.py
   ```

## Usage
1. Launch the application
2. Add processes with their details:
   - Process ID
   - Arrival Time
   - Burst Time
   - Priority (for Priority Scheduling)
3. Select the desired scheduling algorithm
4. Click "Simulate" to view the results

## Performance Metrics
The simulator calculates and displays:
- Average Waiting Time
- Average Turnaround Time
- CPU Utilization
- Gantt Chart visualization 