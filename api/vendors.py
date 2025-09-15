from http.server import BaseHTTPRequestHandler
import json
import os

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
            # Enhanced vendor database with real-world data structure
            vendor_data = {
                "Steel Reinforcement Bars": [
                    {
                        "name": "Mumbai Steel Works Pvt Ltd",
                        "location": "Mumbai, Maharashtra",
                        "contact": "+91-22-2345-6789",
                        "email": "info@mumbaisteel.com",
                        "rating": 4.5,
                        "experience_years": 15,
                        "services": ["Steel Reinforcement Bars", "TMT Bars", "Structural Steel"],
                        "price_range": "₹15,000-20,000/ton",
                        "delivery_time": "7-14 days",
                        "certifications": ["ISO 9001", "BIS Certification"]
                    },
                    {
                        "name": "Pune Iron & Steel Co.",
                        "location": "Pune, Maharashtra",
                        "contact": "+91-20-3456-7890",
                        "email": "sales@puneiron.com",
                        "rating": 4.2,
                        "experience_years": 12,
                        "services": ["Steel Bars", "Iron Products", "Metal Fabrication"],
                        "price_range": "₹14,500-19,500/ton",
                        "delivery_time": "5-10 days",
                        "certifications": ["ISO 9001"]
                    }
                ],
                "Concrete Mix": [
                    {
                        "name": "Maharashtra Concrete Solutions",
                        "location": "Mumbai, Maharashtra",
                        "contact": "+91-22-4567-8901",
                        "email": "info@mahaconcrete.com",
                        "rating": 4.6,
                        "experience_years": 20,
                        "services": ["Ready Mix Concrete", "Precast Concrete", "Concrete Pumping"],
                        "price_range": "₹4,500-6,000/m³",
                        "delivery_time": "Same day",
                        "certifications": ["ISO 9001", "NRMCA Certified"]
                    },
                    {
                        "name": "Pune Ready Mix Ltd",
                        "location": "Pune, Maharashtra",
                        "contact": "+91-20-5678-9012",
                        "email": "orders@punereadymix.com",
                        "rating": 4.3,
                        "experience_years": 18,
                        "services": ["Ready Mix Concrete", "Concrete Supply", "Quality Testing"],
                        "price_range": "₹4,200-5,800/m³",
                        "delivery_time": "Same day",
                        "certifications": ["ISO 9001"]
                    }
                ],
                "Electrical Cables": [
                    {
                        "name": "Maharashtra Cables & Wires",
                        "location": "Aurangabad, Maharashtra",
                        "contact": "+91-240-234-5678",
                        "email": "sales@mahacables.com",
                        "rating": 4.4,
                        "experience_years": 14,
                        "services": ["Power Cables", "Control Cables", "Fiber Optic Cables"],
                        "price_range": "₹120-180/meter",
                        "delivery_time": "3-7 days",
                        "certifications": ["ISI Mark", "CE Certified"]
                    },
                    {
                        "name": "Western India Electricals",
                        "location": "Mumbai, Maharashtra",
                        "contact": "+91-22-6789-0123",
                        "email": "info@wielectricals.com",
                        "rating": 4.1,
                        "experience_years": 16,
                        "services": ["Electrical Cables", "Switchgear", "Electrical Components"],
                        "price_range": "₹110-170/meter",
                        "delivery_time": "2-5 days",
                        "certifications": ["ISI Mark"]
                    }
                ],
                "HVAC Equipment": [
                    {
                        "name": "Cool Air Systems Maharashtra",
                        "location": "Pune, Maharashtra",
                        "contact": "+91-20-7890-1234",
                        "email": "info@coolair.com",
                        "rating": 4.5,
                        "experience_years": 22,
                        "services": ["HVAC Systems", "Air Conditioning", "Ventilation Equipment"],
                        "price_range": "₹1,20,000-2,50,000/unit",
                        "delivery_time": "15-30 days",
                        "certifications": ["ASHRAE Certified", "Energy Star"]
                    },
                    {
                        "name": "Mumbai Climate Control",
                        "location": "Mumbai, Maharashtra",
                        "contact": "+91-22-8901-2345",
                        "email": "sales@mumbaiclimate.com",
                        "rating": 4.2,
                        "experience_years": 19,
                        "services": ["HVAC Installation", "Climate Control", "Maintenance Services"],
                        "price_range": "₹1,10,000-2,40,000/unit",
                        "delivery_time": "12-25 days",
                        "certifications": ["ASHRAE Certified"]
                    }
                ]
            }
            
            # Parse query parameters for filtering
            query_string = self.path.split('?')
            filters = {}
            if len(query_string) > 1:
                params = query_string[1].split('&')
                for param in params:
                    if '=' in param:
                        key, value = param.split('=', 1)
                        filters[key] = value.replace('%20', ' ')
            
            # Filter vendors if material type is specified
            if 'material' in filters:
                material_type = filters['material']
                if material_type in vendor_data:
                    response = {material_type: vendor_data[material_type]}
                else:
                    response = {"error": f"Material type '{material_type}' not found"}
            else:
                response = vendor_data
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            error_response = {
                'error': str(e),
                'message': 'Error loading vendor database'
            }
            self.wfile.write(json.dumps(error_response).encode())