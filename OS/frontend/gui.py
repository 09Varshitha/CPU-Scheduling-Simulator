import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from backend.process import Process
from backend.scheduler import Scheduler
from .visualizer import Visualizer

class CPUSchedulerApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("CPU Scheduler Simulator")
        self.root.geometry("1200x800")
        
        # Initialize components
        self.processes = []
        self.scheduler = Scheduler()
        self.visualizer = Visualizer()
        
        self._setup_gui()
        
    def _setup_gui(self):
        # Create main frames
        self.input_frame = ctk.CTkFrame(self.root)
        self.input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        self.display_frame = ctk.CTkFrame(self.root)
        self.display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Process input section
        self._setup_process_input()
        
        # Process list section
        self._setup_process_list()
        
        # Algorithm selection and simulation control
        self._setup_simulation_controls()
        
        # Results display area
        self._setup_results_display()
        
    def _setup_process_input(self):
        input_label = ctk.CTkLabel(self.input_frame, text="Add Process", font=("Arial", 16, "bold"))
        input_label.pack(pady=5)
        
        # Process ID
        pid_frame = ctk.CTkFrame(self.input_frame)
        pid_frame.pack(fill=tk.X, padx=5, pady=2)
        ctk.CTkLabel(pid_frame, text="Process ID:").pack(side=tk.LEFT)
        self.pid_var = tk.StringVar()
        self.pid_entry = ctk.CTkEntry(pid_frame, textvariable=self.pid_var)
        self.pid_entry.pack(side=tk.RIGHT, padx=5)
        
        # Arrival Time
        arrival_frame = ctk.CTkFrame(self.input_frame)
        arrival_frame.pack(fill=tk.X, padx=5, pady=2)
        ctk.CTkLabel(arrival_frame, text="Arrival Time:").pack(side=tk.LEFT)
        self.arrival_var = tk.StringVar()
        self.arrival_entry = ctk.CTkEntry(arrival_frame, textvariable=self.arrival_var)
        self.arrival_entry.pack(side=tk.RIGHT, padx=5)
        
        # Burst Time
        burst_frame = ctk.CTkFrame(self.input_frame)
        burst_frame.pack(fill=tk.X, padx=5, pady=2)
        ctk.CTkLabel(burst_frame, text="Burst Time:").pack(side=tk.LEFT)
        self.burst_var = tk.StringVar()
        self.burst_entry = ctk.CTkEntry(burst_frame, textvariable=self.burst_var)
        self.burst_entry.pack(side=tk.RIGHT, padx=5)
        
        # Priority
        priority_frame = ctk.CTkFrame(self.input_frame)
        priority_frame.pack(fill=tk.X, padx=5, pady=2)
        ctk.CTkLabel(priority_frame, text="Priority:").pack(side=tk.LEFT)
        self.priority_var = tk.StringVar()
        self.priority_entry = ctk.CTkEntry(priority_frame, textvariable=self.priority_var)
        self.priority_entry.pack(side=tk.RIGHT, padx=5)
        
        # Add Process Button
        add_btn = ctk.CTkButton(self.input_frame, text="Add Process", command=self._add_process)
        add_btn.pack(pady=10)
        
    def _setup_process_list(self):
        list_label = ctk.CTkLabel(self.input_frame, text="Process List", font=("Arial", 16, "bold"))
        list_label.pack(pady=5)
        
        # Create Treeview
        self.process_tree = ttk.Treeview(self.input_frame, columns=("PID", "Arrival", "Burst", "Priority"),
                                       show="headings", height=10)
        
        self.process_tree.heading("PID", text="PID")
        self.process_tree.heading("Arrival", text="Arrival Time")
        self.process_tree.heading("Burst", text="Burst Time")
        self.process_tree.heading("Priority", text="Priority")
        
        self.process_tree.pack(pady=5)
        
        # Clear Processes Button
        clear_btn = ctk.CTkButton(self.input_frame, text="Clear All", command=self._clear_processes)
        clear_btn.pack(pady=5)
        
    def _setup_simulation_controls(self):
        control_label = ctk.CTkLabel(self.input_frame, text="Simulation Control", font=("Arial", 16, "bold"))
        control_label.pack(pady=5)
        
        # Algorithm Selection
        self.algorithm_var = tk.StringVar(value="FCFS")
        algorithms = ["FCFS", "SJF", "Round Robin", "Priority"]
        
        for alg in algorithms:
            radio_btn = ctk.CTkRadioButton(self.input_frame, text=alg, variable=self.algorithm_var, value=alg)
            radio_btn.pack(pady=2)
            
        # Time Quantum input for Round Robin
        quantum_frame = ctk.CTkFrame(self.input_frame)
        quantum_frame.pack(fill=tk.X, padx=5, pady=2)
        ctk.CTkLabel(quantum_frame, text="Time Quantum:").pack(side=tk.LEFT)
        self.quantum_var = tk.StringVar(value="2")
        self.quantum_entry = ctk.CTkEntry(quantum_frame, textvariable=self.quantum_var)
        self.quantum_entry.pack(side=tk.RIGHT, padx=5)
        
        # Simulate Button
        simulate_btn = ctk.CTkButton(self.input_frame, text="Simulate", command=self._run_simulation)
        simulate_btn.pack(pady=10)
        
    def _setup_results_display(self):
        self.results_notebook = ttk.Notebook(self.display_frame)
        self.results_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Gantt Chart Tab
        self.gantt_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.gantt_frame, text="Gantt Chart")
        
        # Metrics Tab
        self.metrics_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.metrics_frame, text="Metrics")
        
    def _add_process(self):
        try:
            pid = self.pid_var.get()
            arrival_time = int(self.arrival_var.get())
            burst_time = int(self.burst_var.get())
            priority = int(self.priority_var.get())
            
            process = Process(pid, arrival_time, burst_time, priority)
            self.processes.append(process)
            
            # Add to treeview
            self.process_tree.insert("", tk.END, values=(pid, arrival_time, burst_time, priority))
            
            # Clear inputs
            self.pid_var.set("")
            self.arrival_var.set("")
            self.burst_var.set("")
            self.priority_var.set("")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values")
            
    def _clear_processes(self):
        self.processes.clear()
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
            
    def _run_simulation(self):
        if not self.processes:
            messagebox.showwarning("Warning", "Please add some processes first")
            return
            
        algorithm = self.algorithm_var.get()
        
        # Clear previous results
        for widget in self.gantt_frame.winfo_children():
            widget.destroy()
        for widget in self.metrics_frame.winfo_children():
            widget.destroy()
            
        # Run selected algorithm
        if algorithm == "FCFS":
            timeline = self.scheduler.fcfs(self.processes)
        elif algorithm == "SJF":
            timeline = self.scheduler.sjf(self.processes)
        elif algorithm == "Round Robin":
            try:
                time_quantum = int(self.quantum_var.get())
                timeline = self.scheduler.round_robin(self.processes, time_quantum)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid time quantum")
                return
        else:  # Priority
            timeline = self.scheduler.priority(self.processes)
            
        # Create and display Gantt chart
        gantt_fig = self.visualizer.create_gantt_chart(timeline, f"{algorithm} Gantt Chart")
        gantt_canvas = FigureCanvasTkAgg(gantt_fig, self.gantt_frame)
        gantt_canvas.draw()
        gantt_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Create and display metrics
        metrics_fig = self.visualizer.display_metrics(self.processes, algorithm)
        metrics_canvas = FigureCanvasTkAgg(metrics_fig, self.metrics_frame)
        metrics_canvas.draw()
        metrics_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def run(self):
        self.root.mainloop() 




