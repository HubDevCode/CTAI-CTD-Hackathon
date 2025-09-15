import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np
import json

class ProjectScheduler:
    def __init__(self, project_name="Data Center Construction"):
        self.project_name = project_name
        self.tasks = []
        self.milestones = []
        
    def create_data_center_schedule(self):
        """Create a comprehensive project schedule for Data Center construction"""
        start_date = datetime(2024, 1, 1)
        
        # Define project phases and tasks
        project_phases = [
            {
                "phase": "Project Initiation & Planning",
                "tasks": [
                    {"name": "Project Charter & Feasibility", "duration": 10, "dependencies": []},
                    {"name": "Site Survey & Geotechnical", "duration": 15, "dependencies": [0]},
                    {"name": "Detailed Design & Engineering", "duration": 30, "dependencies": [1]},
                    {"name": "Permits & Approvals", "duration": 20, "dependencies": [2]},
                    {"name": "Material Procurement Planning", "duration": 10, "dependencies": [2]}
                ]
            },
            {
                "phase": "Procurement & Contracting",
                "tasks": [
                    {"name": "Vendor Selection & Contracting", "duration": 15, "dependencies": [4]},
                    {"name": "Material Orders & Delivery Schedule", "duration": 20, "dependencies": [5]},
                    {"name": "Equipment Procurement", "duration": 25, "dependencies": [5]},
                    {"name": "Long Lead Items Ordering", "duration": 35, "dependencies": [5]}
                ]
            },
            {
                "phase": "Site Preparation",
                "tasks": [
                    {"name": "Site Clearing & Preparation", "duration": 12, "dependencies": [3]},
                    {"name": "Temporary Facilities Setup", "duration": 8, "dependencies": [9]},
                    {"name": "Access Roads & Utilities", "duration": 15, "dependencies": [9]}
                ]
            },
            {
                "phase": "Foundation & Structure",
                "tasks": [
                    {"name": "Excavation & Foundation", "duration": 25, "dependencies": [11, 6]},
                    {"name": "Concrete Work - Foundation", "duration": 20, "dependencies": [12]},
                    {"name": "Steel Structure Assembly", "duration": 30, "dependencies": [13, 6]},
                    {"name": "Concrete Work - Superstructure", "duration": 35, "dependencies": [14]}
                ]
            },
            {
                "phase": "Building Envelope",
                "tasks": [
                    {"name": "Roofing & Waterproofing", "duration": 20, "dependencies": [15]},
                    {"name": "Exterior Walls & Cladding", "duration": 25, "dependencies": [15]},
                    {"name": "Windows & Doors Installation", "duration": 15, "dependencies": [17]}
                ]
            },
            {
                "phase": "MEP Installation",
                "tasks": [
                    {"name": "Electrical Infrastructure", "duration": 40, "dependencies": [15, 7]},
                    {"name": "HVAC System Installation", "duration": 45, "dependencies": [15, 8]},
                    {"name": "Plumbing & Fire Protection", "duration": 30, "dependencies": [15]},
                    {"name": "Power Distribution & UPS", "duration": 35, "dependencies": [19]}
                ]
            },
            {
                "phase": "Interior & Finishes",
                "tasks": [
                    {"name": "Interior Partitions", "duration": 20, "dependencies": [18]},
                    {"name": "Flooring & Ceiling", "duration": 25, "dependencies": [23]},
                    {"name": "Interior Finishes", "duration": 20, "dependencies": [24]}
                ]
            },
            {
                "phase": "Testing & Commissioning",
                "tasks": [
                    {"name": "System Integration Testing", "duration": 15, "dependencies": [20, 21, 22]},
                    {"name": "Performance Testing", "duration": 10, "dependencies": [26]},
                    {"name": "Final Inspections", "duration": 8, "dependencies": [25, 27]},
                    {"name": "Documentation & Handover", "duration": 5, "dependencies": [28]}
                ]
            }
        ]
        
        # Calculate task dates
        task_id = 0
        current_date = start_date
        
        for phase in project_phases:
            for task in phase["tasks"]:
                # Calculate start date based on dependencies
                task_start = start_date
                if task["dependencies"]:
                    max_dependency_end = start_date
                    for dep_id in task["dependencies"]:
                        if dep_id < len(self.tasks):
                            dep_end = self.tasks[dep_id]["end_date"]
                            if dep_end > max_dependency_end:
                                max_dependency_end = dep_end
                    task_start = max_dependency_end + timedelta(days=1)
                
                task_end = task_start + timedelta(days=task["duration"])
                
                self.tasks.append({
                    "id": task_id,
                    "name": task["name"],
                    "phase": phase["phase"],
                    "start_date": task_start,
                    "end_date": task_end,
                    "duration": task["duration"],
                    "dependencies": task["dependencies"]
                })
                
                task_id += 1
        
        # Add milestones
        self.milestones = [
            {"name": "Project Kickoff", "date": start_date},
            {"name": "Design Completion", "date": self.tasks[2]["end_date"]},
            {"name": "Procurement Complete", "date": self.tasks[8]["end_date"]},
            {"name": "Foundation Complete", "date": self.tasks[13]["end_date"]},
            {"name": "Structure Complete", "date": self.tasks[15]["end_date"]},
            {"name": "MEP Complete", "date": self.tasks[22]["end_date"]},
            {"name": "Project Completion", "date": self.tasks[-1]["end_date"]}
        ]
        
        return self.tasks, self.milestones
    
    def create_gantt_chart(self, save_path="project_gantt_chart.png"):
        """Create a comprehensive Gantt chart"""
        if not self.tasks:
            self.create_data_center_schedule()
        
        # Create figure and axis
        fig, ax = plt.subplots(1, 1, figsize=(16, 12))
        
        # Define colors for different phases
        phase_colors = {
            "Project Initiation & Planning": "#FF6B6B",
            "Procurement & Contracting": "#4ECDC4", 
            "Site Preparation": "#45B7D1",
            "Foundation & Structure": "#96CEB4",
            "Building Envelope": "#FECA57",
            "MEP Installation": "#FF9FF3",
            "Interior & Finishes": "#54A0FF",
            "Testing & Commissioning": "#5F27CD"
        }
        
        # Plot tasks
        for i, task in enumerate(self.tasks):
            start_date = task["start_date"]
            duration = task["duration"]
            phase = task["phase"]
            
            # Create horizontal bar
            ax.barh(i, duration, left=start_date, 
                   color=phase_colors.get(phase, "#95A5A6"),
                   alpha=0.8, edgecolor='black', linewidth=0.5)
            
            # Add task name
            ax.text(start_date + timedelta(days=duration/2), i, 
                   task["name"], ha="center", va="center", 
                   fontsize=8, fontweight='bold')
        
        # Plot milestones
        for milestone in self.milestones:
            milestone_date = milestone["date"]
            ax.axvline(x=milestone_date, color='red', linestyle='--', alpha=0.7)
            ax.text(milestone_date, len(self.tasks), milestone["name"], 
                   rotation=45, ha='right', va='bottom', fontsize=9, 
                   color='red', fontweight='bold')
        
        # Customize chart
        ax.set_yticks(range(len(self.tasks)))
        ax.set_yticklabels([f"{task['phase'][:15]}..." if len(task['phase']) > 15 
                           else task['phase'] for task in self.tasks])
        ax.invert_yaxis()
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Add grid and labels
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('Timeline', fontsize=12, fontweight='bold')
        ax.set_ylabel('Project Tasks', fontsize=12, fontweight='bold')
        ax.set_title(f'{self.project_name} - Gantt Chart', 
                    fontsize=16, fontweight='bold', pad=20)
        
        # Create legend
        legend_elements = [plt.Rectangle((0,0),1,1, facecolor=color, alpha=0.8) 
                          for phase, color in phase_colors.items()]
        ax.legend(legend_elements, phase_colors.keys(), 
                 loc='upper left', bbox_to_anchor=(1.05, 1))
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"Gantt chart saved as: {save_path}")
        return fig
    
    def export_to_csv(self, filename="project_schedule.csv"):
        """Export schedule to CSV format"""
        if not self.tasks:
            self.create_data_center_schedule()
        
        schedule_data = []
        for task in self.tasks:
            schedule_data.append({
                "Task_ID": task["id"],
                "Task_Name": task["name"],
                "Phase": task["phase"],
                "Start_Date": task["start_date"].strftime("%Y-%m-%d"),
                "End_Date": task["end_date"].strftime("%Y-%m-%d"),
                "Duration_Days": task["duration"],
                "Dependencies": ",".join(map(str, task["dependencies"]))
            })
        
        df = pd.DataFrame(schedule_data)
        df.to_csv(filename, index=False)
        print(f"Schedule exported to: {filename}")
        return df
    
    def export_to_json(self, filename="project_schedule.json"):
        """Export schedule to JSON format"""
        if not self.tasks:
            self.create_data_center_schedule()
        
        # Convert datetime objects to strings for JSON serialization
        tasks_json = []
        for task in self.tasks:
            task_copy = task.copy()
            task_copy["start_date"] = task["start_date"].isoformat()
            task_copy["end_date"] = task["end_date"].isoformat()
            tasks_json.append(task_copy)
        
        milestones_json = []
        for milestone in self.milestones:
            milestone_copy = milestone.copy()
            milestone_copy["date"] = milestone["date"].isoformat()
            milestones_json.append(milestone_copy)
        
        schedule_json = {
            "project_name": self.project_name,
            "tasks": tasks_json,
            "milestones": milestones_json,
            "total_duration_days": (self.tasks[-1]["end_date"] - self.tasks[0]["start_date"]).days
        }
        
        with open(filename, 'w') as f:
            json.dump(schedule_json, f, indent=2)
        
        print(f"Schedule exported to: {filename}")
        return schedule_json
    
    def print_schedule_summary(self):
        """Print a summary of the project schedule"""
        if not self.tasks:
            self.create_data_center_schedule()
        
        print(f"\n{'='*60}")
        print(f"PROJECT SCHEDULE SUMMARY: {self.project_name}")
        print(f"{'='*60}")
        
        project_start = min(task["start_date"] for task in self.tasks)
        project_end = max(task["end_date"] for task in self.tasks)
        total_duration = (project_end - project_start).days
        
        print(f"Project Start Date: {project_start.strftime('%Y-%m-%d')}")
        print(f"Project End Date: {project_end.strftime('%Y-%m-%d')}")
        print(f"Total Duration: {total_duration} days")
        print(f"Total Tasks: {len(self.tasks)}")
        print(f"Total Milestones: {len(self.milestones)}")
        
        print(f"\nMAJOR MILESTONES:")
        print(f"{'-'*40}")
        for milestone in self.milestones:
            print(f"{milestone['date'].strftime('%Y-%m-%d')}: {milestone['name']}")
        
        print(f"\nPHASE BREAKDOWN:")
        print(f"{'-'*40}")
        phases = {}
        for task in self.tasks:
            phase = task["phase"]
            if phase not in phases:
                phases[phase] = {"tasks": 0, "duration": 0, "start": task["start_date"], "end": task["start_date"]}
            phases[phase]["tasks"] += 1
            phases[phase]["duration"] += task["duration"]
            if task["start_date"] < phases[phase]["start"]:
                phases[phase]["start"] = task["start_date"]
            if task["end_date"] > phases[phase]["end"]:
                phases[phase]["end"] = task["end_date"]
        
        for phase, info in phases.items():
            actual_duration = (info["end"] - info["start"]).days
            print(f"{phase}: {info['tasks']} tasks, {actual_duration} days")

def main():
    # Create project scheduler
    scheduler = ProjectScheduler("Data Center Construction Project")
    
    # Generate schedule
    print("Generating Data Center construction schedule...")
    tasks, milestones = scheduler.create_data_center_schedule()
    
    # Print summary
    scheduler.print_schedule_summary()
    
    # Export to different formats
    scheduler.export_to_csv("data_center_schedule.csv")
    scheduler.export_to_json("data_center_schedule.json")
    
    # Create Gantt chart
    print("\nGenerating Gantt chart...")
    scheduler.create_gantt_chart("data_center_gantt_chart.png")
    
    # Create procurement timeline integration
    print("\nCreating procurement integration timeline...")
    
    # Material procurement mapping
    material_mapping = {
        "Steel Reinforcement Bars": {"task_ids": [12, 13, 14], "lead_time": 14},
        "Concrete Mix": {"task_ids": [13, 15], "lead_time": 7},
        "Electrical Cables": {"task_ids": [19, 22], "lead_time": 21},
        "HVAC Equipment": {"task_ids": [20], "lead_time": 35}
    }
    
    procurement_schedule = []
    for material, info in material_mapping.items():
        for task_id in info["task_ids"]:
            if task_id < len(tasks):
                task = tasks[task_id]
                procurement_start = task["start_date"] - timedelta(days=info["lead_time"])
                procurement_schedule.append({
                    "Material": material,
                    "Required_For_Task": task["name"],
                    "Task_Start_Date": task["start_date"].strftime("%Y-%m-%d"),
                    "Procurement_Start_Date": procurement_start.strftime("%Y-%m-%d"),
                    "Lead_Time_Days": info["lead_time"]
                })
    
    # Save procurement timeline
    procurement_df = pd.DataFrame(procurement_schedule)
    procurement_df.to_csv("procurement_timeline.csv", index=False)
    print("Procurement timeline saved as: procurement_timeline.csv")
    
    return scheduler

if __name__ == "__main__":
    scheduler = main()