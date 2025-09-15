import pandas as pd
import json
from datetime import datetime, timedelta
import numpy as np

class ProcurementPlan:
    def __init__(self):
        self.materials_data = {}
        self.vendors_data = {}
        self.schedule_data = {}
        self.procurement_plan = {}
        
    def load_forecast_data(self):
        """Load material forecast and vendor data"""
        # Load vendor data
        try:
            with open('comprehensive_vendor_database.json', 'r') as f:
                self.vendors_data = json.load(f)
        except FileNotFoundError:
            print("Vendor database not found. Creating sample data...")
            self.create_sample_vendor_data()
        
        # Load schedule data
        try:
            with open('data_center_schedule.json', 'r') as f:
                self.schedule_data = json.load(f)
        except FileNotFoundError:
            print("Schedule data not found. Creating sample schedule...")
            self.create_sample_schedule()
    
    def create_sample_vendor_data(self):
        """Create sample vendor data if file doesn't exist"""
        self.vendors_data = {
            "Steel Reinforcement Bars": [
                {
                    "name": "Mumbai Steel Works Pvt Ltd",
                    "location": "Mumbai, Maharashtra",
                    "contact": "+91-22-2345-6789",
                    "rating": 4.5,
                    "lead_time_days": 14,
                    "price_per_unit": 15000
                }
            ],
            "Concrete Mix": [
                {
                    "name": "Maharashtra Concrete Solutions",
                    "location": "Mumbai, Maharashtra", 
                    "contact": "+91-22-4567-8901",
                    "rating": 4.6,
                    "lead_time_days": 7,
                    "price_per_unit": 5000
                }
            ],
            "HVAC Equipment": [
                {
                    "name": "Cool Air Systems Maharashtra",
                    "location": "Pune, Maharashtra",
                    "contact": "+91-20-7890-1234",
                    "rating": 4.5,
                    "lead_time_days": 35,
                    "price_per_unit": 150000
                }
            ]
        }
    
    def create_sample_schedule(self):
        """Create sample schedule data if file doesn't exist"""
        start_date = datetime(2024, 1, 1)
        self.schedule_data = {
            "project_name": "Data Center Construction",
            "tasks": [
                {
                    "id": 12,
                    "name": "Excavation & Foundation",
                    "start_date": (start_date + timedelta(days=100)).isoformat(),
                    "end_date": (start_date + timedelta(days=125)).isoformat()
                },
                {
                    "id": 19,
                    "name": "Electrical Infrastructure", 
                    "start_date": (start_date + timedelta(days=200)).isoformat(),
                    "end_date": (start_date + timedelta(days=240)).isoformat()
                },
                {
                    "id": 20,
                    "name": "HVAC System Installation",
                    "start_date": (start_date + timedelta(days=220)).isoformat(),
                    "end_date": (start_date + timedelta(days=265)).isoformat()
                }
            ]
        }
    
    def create_comprehensive_procurement_plan(self):
        """Create a comprehensive procurement management plan"""
        self.load_forecast_data()
        
        # Material requirements based on Data Center project (25MW, 200k sq ft)
        material_requirements = {
            "Steel Reinforcement Bars": {
                "quantity": 160,
                "unit": "tons",
                "estimated_cost_per_unit": 15000,
                "critical_path": True,
                "required_for_tasks": ["Excavation & Foundation", "Steel Structure Assembly"],
                "quality_standards": "IS 1786:2008, Grade Fe 500",
                "storage_requirements": "Covered warehouse, max 3 tier stacking"
            },
            "Concrete Mix": {
                "quantity": 200,
                "unit": "cubic meters",
                "estimated_cost_per_unit": 5000,
                "critical_path": True,
                "required_for_tasks": ["Foundation Work", "Superstructure"],
                "quality_standards": "IS 456:2000, M30 Grade",
                "storage_requirements": "Ready-mix on demand, no storage"
            },
            "Electrical Cables": {
                "quantity": 80,
                "unit": "kilometers",
                "estimated_cost_per_unit": 8000,
                "critical_path": False,
                "required_for_tasks": ["Electrical Infrastructure", "Power Distribution"],
                "quality_standards": "IS 694:1990, PVC insulated",
                "storage_requirements": "Dry storage, vertical reels"
            },
            "HVAC Equipment": {
                "quantity": 84,
                "unit": "units",
                "estimated_cost_per_unit": 150000,
                "critical_path": True,
                "required_for_tasks": ["HVAC System Installation"],
                "quality_standards": "ASHRAE standards, Energy Star rated",
                "storage_requirements": "Climate-controlled warehouse"
            }
        }
        
        # Create procurement strategy for each material
        procurement_strategies = {}
        
        for material, requirements in material_requirements.items():
            strategy = self.develop_material_strategy(material, requirements)
            procurement_strategies[material] = strategy
        
        # Create overall procurement plan
        self.procurement_plan = {
            "project_overview": {
                "project_name": "Data Center Construction - 25MW Facility",
                "location": "Maharashtra, India",
                "total_area": "200,000 sq ft",
                "project_duration": "12 months",
                "total_estimated_cost": sum(req["quantity"] * req["estimated_cost_per_unit"] 
                                          for req in material_requirements.values())
            },
            "material_requirements": material_requirements,
            "procurement_strategies": procurement_strategies,
            "risk_management": self.create_risk_management_plan(),
            "quality_assurance": self.create_quality_plan(),
            "timeline": self.create_procurement_timeline(material_requirements),
            "budget_breakdown": self.create_budget_breakdown(material_requirements),
            "vendor_management": self.create_vendor_management_plan()
        }
        
        return self.procurement_plan
    
    def develop_material_strategy(self, material_name, requirements):
        """Develop procurement strategy for specific material"""
        # Get vendor information
        vendors = self.vendors_data.get(material_name, [])
        
        # Select primary and backup vendors
        if vendors:
            primary_vendor = max(vendors, key=lambda x: x.get('rating', 0))
            backup_vendors = [v for v in vendors if v != primary_vendor][:2]
        else:
            primary_vendor = {"name": "TBD", "rating": 0, "lead_time_days": 30}
            backup_vendors = []
        
        strategy = {
            "sourcing_approach": "Multi-vendor with primary supplier",
            "primary_vendor": primary_vendor,
            "backup_vendors": backup_vendors,
            "procurement_method": "Competitive bidding" if len(vendors) > 2 else "Direct procurement",
            "delivery_schedule": self.calculate_delivery_schedule(material_name, requirements),
            "inventory_strategy": "Just-in-time" if not requirements["critical_path"] else "Safety stock",
            "payment_terms": "30% advance, 60% on delivery, 10% on acceptance",
            "contract_duration": "Project duration with extension option",
            "performance_metrics": [
                "On-time delivery rate >= 95%",
                "Quality acceptance rate >= 98%", 
                "Cost variance <= 5%"
            ]
        }
        
        return strategy
    
    def calculate_delivery_schedule(self, material_name, requirements):
        """Calculate optimal delivery schedule for material"""
        # Find relevant tasks from schedule
        relevant_tasks = []
        for task in self.schedule_data.get("tasks", []):
            if any(req_task in task["name"] for req_task in requirements["required_for_tasks"]):
                relevant_tasks.append(task)
        
        if not relevant_tasks:
            return {"delivery_start": "TBD", "delivery_end": "TBD"}
        
        # Calculate delivery windows
        earliest_task = min(relevant_tasks, key=lambda x: x["start_date"])
        latest_task = max(relevant_tasks, key=lambda x: x["end_date"])
        
        # Get lead time from vendor data
        vendors = self.vendors_data.get(material_name, [])
        lead_time = vendors[0].get("lead_time_days", 30) if vendors else 30
        
        delivery_start = datetime.fromisoformat(earliest_task["start_date"]) - timedelta(days=lead_time)
        delivery_end = datetime.fromisoformat(latest_task["start_date"])
        
        return {
            "delivery_start": delivery_start.strftime("%Y-%m-%d"),
            "delivery_end": delivery_end.strftime("%Y-%m-%d"),
            "lead_time_days": lead_time,
            "delivery_method": "Phased delivery" if requirements["quantity"] > 100 else "Single delivery"
        }
    
    def create_risk_management_plan(self):
        """Create comprehensive risk management plan"""
        risks = [
            {
                "risk_category": "Supply Chain",
                "risk_description": "Material price volatility",
                "probability": "High",
                "impact": "Medium",
                "mitigation_strategy": "Fixed-price contracts with price escalation clauses",
                "contingency_plan": "Alternative supplier activation"
            },
            {
                "risk_category": "Quality",
                "risk_description": "Material quality issues",
                "probability": "Medium", 
                "impact": "High",
                "mitigation_strategy": "Pre-qualified vendor list, quality inspections",
                "contingency_plan": "Rejection and re-procurement process"
            },
            {
                "risk_category": "Logistics",
                "risk_description": "Transportation delays",
                "probability": "Medium",
                "impact": "Medium",
                "mitigation_strategy": "Buffer time in delivery schedules",
                "contingency_plan": "Expedited shipping arrangements"
            },
            {
                "risk_category": "Regulatory",
                "risk_description": "Import/permit delays",
                "probability": "Low",
                "impact": "High", 
                "mitigation_strategy": "Early permit applications, compliance monitoring",
                "contingency_plan": "Legal and regulatory support engagement"
            }
        ]
        
        return {
            "risk_assessment": risks,
            "monitoring_frequency": "Weekly risk reviews",
            "escalation_matrix": {
                "Low impact": "Project Manager",
                "Medium impact": "Procurement Director", 
                "High impact": "Project Steering Committee"
            }
        }
    
    def create_quality_plan(self):
        """Create quality assurance plan"""
        return {
            "quality_standards": {
                "Steel": "IS 1786:2008, Grade Fe 500",
                "Concrete": "IS 456:2000, M30 Grade minimum",
                "Electrical": "IS 694:1990, IEC standards",
                "HVAC": "ASHRAE standards, Energy Star certification"
            },
            "inspection_procedures": [
                "Pre-delivery inspection at vendor facility",
                "Goods receipt inspection at site",
                "Installation quality checks",
                "Final acceptance testing"
            ],
            "documentation_requirements": [
                "Material certificates",
                "Test reports",
                "Calibration certificates", 
                "Compliance declarations"
            ],
            "rejection_criteria": "Non-conformance to specifications or standards"
        }
    
    def create_procurement_timeline(self, material_requirements):
        """Create detailed procurement timeline"""
        timeline_phases = [
            {
                "phase": "Planning & Specification",
                "duration_weeks": 2,
                "activities": [
                    "Material requirement finalization",
                    "Technical specification preparation",
                    "Budget approval"
                ]
            },
            {
                "phase": "Vendor Selection",
                "duration_weeks": 3,
                "activities": [
                    "RFQ preparation and issuance",
                    "Vendor evaluation and shortlisting",
                    "Contract negotiation"
                ]
            },
            {
                "phase": "Contract Award",
                "duration_weeks": 1,
                "activities": [
                    "Contract finalization",
                    "Purchase order issuance",
                    "Delivery schedule confirmation"
                ]
            },
            {
                "phase": "Execution & Monitoring",
                "duration_weeks": 20,
                "activities": [
                    "Production monitoring",
                    "Quality inspections",
                    "Delivery coordination",
                    "Invoice processing"
                ]
            }
        ]
        
        return {
            "total_timeline_weeks": 26,
            "phases": timeline_phases,
            "critical_milestones": [
                "Week 2: Specifications approved",
                "Week 5: Vendors selected",
                "Week 6: Contracts signed",
                "Week 26: All materials delivered"
            ]
        }
    
    def create_budget_breakdown(self, material_requirements):
        """Create detailed budget breakdown"""
        material_costs = {}
        total_material_cost = 0
        
        for material, req in material_requirements.items():
            cost = req["quantity"] * req["estimated_cost_per_unit"]
            material_costs[material] = {
                "quantity": req["quantity"],
                "unit_cost": req["estimated_cost_per_unit"],
                "total_cost": cost,
                "percentage": 0  # Will be calculated later
            }
            total_material_cost += cost
        
        # Calculate percentages
        for material in material_costs:
            material_costs[material]["percentage"] = round(
                (material_costs[material]["total_cost"] / total_material_cost) * 100, 2
            )
        
        # Additional costs
        logistics_cost = total_material_cost * 0.05  # 5%
        insurance_cost = total_material_cost * 0.02  # 2%
        contingency_cost = total_material_cost * 0.10  # 10%
        
        total_procurement_cost = total_material_cost + logistics_cost + insurance_cost + contingency_cost
        
        return {
            "material_costs": material_costs,
            "additional_costs": {
                "logistics": logistics_cost,
                "insurance": insurance_cost,
                "contingency": contingency_cost
            },
            "total_material_cost": total_material_cost,
            "total_procurement_cost": total_procurement_cost,
            "currency": "INR"
        }
    
    def create_vendor_management_plan(self):
        """Create vendor management plan"""
        return {
            "vendor_selection_criteria": [
                "Technical capability (30%)",
                "Financial stability (25%)",
                "Past performance (20%)",
                "Quality certification (15%)",
                "Delivery capability (10%)"
            ],
            "performance_monitoring": {
                "metrics": [
                    "On-time delivery rate",
                    "Quality acceptance rate",
                    "Cost performance",
                    "Customer service rating"
                ],
                "review_frequency": "Monthly",
                "improvement_plans": "Quarterly vendor development meetings"
            },
            "relationship_management": {
                "communication_protocol": "Weekly status calls",
                "escalation_matrix": "Defined contact hierarchy",
                "partnership_development": "Strategic vendor partnerships for future projects"
            }
        }
    
    def save_procurement_plan(self, filename="comprehensive_procurement_plan.json"):
        """Save procurement plan to JSON file"""
        if not self.procurement_plan:
            self.create_comprehensive_procurement_plan()
        
        with open(filename, 'w') as f:
            json.dump(self.procurement_plan, f, indent=2, default=str)
        
        print(f"Comprehensive procurement plan saved to: {filename}")
        return filename
    
    def export_to_excel(self, filename="procurement_plan.xlsx"):
        """Export procurement plan to Excel with multiple sheets"""
        if not self.procurement_plan:
            self.create_comprehensive_procurement_plan()
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Material Requirements sheet
            materials_df = pd.DataFrame.from_dict(
                self.procurement_plan["material_requirements"], 
                orient='index'
            )
            materials_df.to_excel(writer, sheet_name='Material_Requirements')
            
            # Budget Breakdown sheet
            budget_df = pd.DataFrame.from_dict(
                self.procurement_plan["budget_breakdown"]["material_costs"],
                orient='index'
            )
            budget_df.to_excel(writer, sheet_name='Budget_Breakdown')
            
            # Risk Management sheet
            risks_df = pd.DataFrame(self.procurement_plan["risk_management"]["risk_assessment"])
            risks_df.to_excel(writer, sheet_name='Risk_Management', index=False)
            
            # Timeline sheet
            timeline_df = pd.DataFrame(self.procurement_plan["timeline"]["phases"])
            timeline_df.to_excel(writer, sheet_name='Procurement_Timeline', index=False)
        
        print(f"Procurement plan exported to Excel: {filename}")
        return filename
    
    def print_executive_summary(self):
        """Print executive summary of procurement plan"""
        if not self.procurement_plan:
            self.create_comprehensive_procurement_plan()
        
        plan = self.procurement_plan
        
        print("\n" + "="*80)
        print("PROCUREMENT MANAGEMENT PLAN - EXECUTIVE SUMMARY")
        print("="*80)
        
        print(f"\nProject: {plan['project_overview']['project_name']}")
        print(f"Location: {plan['project_overview']['location']}")
        print(f"Total Estimated Procurement Cost: ₹{plan['budget_breakdown']['total_procurement_cost']:,.2f}")
        
        print(f"\nMATERIAL REQUIREMENTS SUMMARY:")
        print("-" * 50)
        for material, req in plan['material_requirements'].items():
            cost = req['quantity'] * req['estimated_cost_per_unit']
            print(f"• {material}: {req['quantity']} {req['unit']} (₹{cost:,.2f})")
        
        print(f"\nTOP RISKS:")
        print("-" * 30)
        high_risks = [r for r in plan['risk_management']['risk_assessment'] 
                     if r['probability'] == 'High' or r['impact'] == 'High']
        for risk in high_risks[:3]:
            print(f"• {risk['risk_description']} ({risk['probability']} probability, {risk['impact']} impact)")
        
        print(f"\nKEY MILESTONES:")
        print("-" * 30)
        for milestone in plan['timeline']['critical_milestones']:
            print(f"• {milestone}")
        
        print(f"\nVENDOR STRATEGY:")
        print("-" * 30)
        print("• Multi-vendor approach with primary and backup suppliers")
        print("• Performance-based contracts with defined KPIs")
        print("• Regular vendor performance reviews and development programs")

def main():
    # Create procurement plan
    procurement = ProcurementPlan()
    
    print("Creating comprehensive procurement management plan...")
    plan = procurement.create_comprehensive_procurement_plan()
    
    # Print executive summary
    procurement.print_executive_summary()
    
    # Save to files
    procurement.save_procurement_plan()
    procurement.export_to_excel()
    
    print(f"\n✅ Procurement plan creation completed!")
    print(f"📁 Files generated:")
    print(f"   - comprehensive_procurement_plan.json")
    print(f"   - procurement_plan.xlsx")
    
    return procurement

if __name__ == "__main__":
    procurement_manager = main()