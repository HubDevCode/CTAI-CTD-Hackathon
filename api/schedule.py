from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime, timedelta

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        # Enable CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        try:
            # Generate project schedule data
            start_date = datetime(2024, 1, 1)
            
            schedule_data = {
                "project_info": {
                    "name": "Data Center Construction Project",
                    "location": "Maharashtra, India",
                    "start_date": start_date.isoformat(),
                    "estimated_duration_days": 346
                },
                "phases": [
                    {
                        "phase": "Project Initiation & Planning",
                        "start_date": start_date.isoformat(),
                        "duration_days": 45,
                        "tasks": [
                            {"name": "Project Charter & Feasibility", "duration": 10},
                            {"name": "Site Survey & Geotechnical", "duration": 15},
                            {"name": "Detailed Design & Engineering", "duration": 30},
                            {"name": "Permits & Approvals", "duration": 20}
                        ]
                    },
                    {
                        "phase": "Procurement & Contracting",
                        "start_date": (start_date + timedelta(days=45)).isoformat(),
                        "duration_days": 35,
                        "tasks": [
                            {"name": "Vendor Selection & Contracting", "duration": 15},
                            {"name": "Material Orders & Delivery Schedule", "duration": 20},
                            {"name": "Equipment Procurement", "duration": 25}
                        ]
                    },
                    {
                        "phase": "Construction",
                        "start_date": (start_date + timedelta(days=80)).isoformat(),
                        "duration_days": 240,
                        "tasks": [
                            {"name": "Site Preparation", "duration": 30},
                            {"name": "Foundation Work", "duration": 45},
                            {"name": "Structural Work", "duration": 90},
                            {"name": "MEP Installation", "duration": 75}
                        ]
                    },
                    {
                        "phase": "Testing & Commissioning",
                        "start_date": (start_date + timedelta(days=320)).isoformat(),
                        "duration_days": 26,
                        "tasks": [
                            {"name": "System Integration Testing", "duration": 15},
                            {"name": "Performance Testing", "duration": 10},
                            {"name": "Final Inspections", "duration": 8},
                            {"name": "Documentation & Handover", "duration": 5}
                        ]
                    }
                ],
                "milestones": [
                    {
                        "name": "Project Kickoff",
                        "date": start_date.isoformat(),
                        "type": "start"
                    },
                    {
                        "name": "Design Completion",
                        "date": (start_date + timedelta(days=75)).isoformat(),
                        "type": "major"
                    },
                    {
                        "name": "Procurement Complete",
                        "date": (start_date + timedelta(days=120)).isoformat(),
                        "type": "major"
                    },
                    {
                        "name": "Foundation Complete",
                        "date": (start_date + timedelta(days=155)).isoformat(),
                        "type": "construction"
                    },
                    {
                        "name": "Structure Complete",
                        "date": (start_date + timedelta(days=245)).isoformat(),
                        "type": "construction"
                    },
                    {
                        "name": "MEP Complete",
                        "date": (start_date + timedelta(days=320)).isoformat(),
                        "type": "major"
                    },
                    {
                        "name": "Project Completion",
                        "date": (start_date + timedelta(days=346)).isoformat(),
                        "type": "end"
                    }
                ],
                "procurement_timeline": [
                    {
                        "material": "Steel Reinforcement Bars",
                        "order_date": (start_date + timedelta(days=60)).isoformat(),
                        "delivery_date": (start_date + timedelta(days=74)).isoformat(),
                        "required_for": "Foundation Work",
                        "lead_time_days": 14
                    },
                    {
                        "material": "Concrete Mix",
                        "order_date": (start_date + timedelta(days=103)).isoformat(),
                        "delivery_date": (start_date + timedelta(days=110)).isoformat(),
                        "required_for": "Foundation & Structure",
                        "lead_time_days": 7
                    },
                    {
                        "material": "HVAC Equipment",
                        "order_date": (start_date + timedelta(days=45)).isoformat(),
                        "delivery_date": (start_date + timedelta(days=80)).isoformat(),
                        "required_for": "MEP Installation",
                        "lead_time_days": 35
                    },
                    {
                        "material": "Electrical Cables",
                        "order_date": (start_date + timedelta(days=180)).isoformat(),
                        "delivery_date": (start_date + timedelta(days=201)).isoformat(),
                        "required_for": "Electrical Infrastructure",
                        "lead_time_days": 21
                    }
                ]
            }
            
            self.wfile.write(json.dumps(schedule_data).encode())
            
        except Exception as e:
            error_response = {
                'error': str(e),
                'message': 'Error generating schedule data'
            }
            self.wfile.write(json.dumps(error_response).encode())