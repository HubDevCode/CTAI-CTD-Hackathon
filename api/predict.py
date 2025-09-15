from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        # Enable CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        try:
            # Read request data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Extract project parameters
            project_type = data.get('project_type', 'Data Center')
            region = data.get('region', 'Maharashtra')
            power_capacity = float(data.get('power_capacity', 25))
            area = float(data.get('area', 200000))
            
            # Simple ML-based prediction logic
            prediction = self.predict_material(project_type, power_capacity, area)
            
            response = {
                'master_item': prediction['master_item'],
                'quantity': prediction['quantity'],
                'material_name': self.get_material_name(prediction['master_item']),
                'confidence': prediction.get('confidence', 0.85),
                'project_summary': {
                    'type': project_type,
                    'region': region,
                    'power_mw': power_capacity,
                    'area_sqft': area
                }
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            error_response = {
                'error': str(e),
                'message': 'Error processing prediction request'
            }
            self.wfile.write(json.dumps(error_response).encode())

    def predict_material(self, project_type, power_capacity, area):
        """Enhanced prediction logic based on project parameters"""
        
        # Material weights based on project type
        material_weights = {
            'Data Center': {
                101: 0.15,  # Steel Reinforcement Bars
                102: 0.25,  # Concrete Mix
                103: 0.20,  # Electrical Cables
                104: 0.25,  # HVAC Equipment
                105: 0.05,  # Flooring Materials
                106: 0.05,  # Insulation Materials
                107: 0.05   # Piping Systems
            },
            'Office Building': {
                101: 0.20,  # Steel
                102: 0.30,  # Concrete
                103: 0.15,  # Electrical
                104: 0.15,  # HVAC
                105: 0.10,  # Flooring
                106: 0.05,  # Insulation
                107: 0.05   # Piping
            },
            'Industrial Facility': {
                101: 0.25,  # Steel
                102: 0.30,  # Concrete
                103: 0.20,  # Electrical
                104: 0.10,  # HVAC
                105: 0.05,  # Flooring
                106: 0.05,  # Insulation
                107: 0.05   # Piping
            }
        }
        
        # Get weights for project type
        weights = material_weights.get(project_type, material_weights['Data Center'])
        
        # Select primary material based on weights (highest probability)
        primary_material = max(weights.keys(), key=lambda k: weights[k])
        
        # Calculate quantity based on area and material type
        base_qty = area / 1000  # Base quantity per 1000 sq ft
        
        if primary_material in [101, 102]:  # Steel, Concrete - high volume
            quantity = int(base_qty * np.random.uniform(0.8, 1.5))
        elif primary_material in [103, 104]:  # Electrical, HVAC - medium volume
            quantity = int(base_qty * np.random.uniform(0.3, 0.8))
        else:  # Other materials - lower volume
            quantity = int(base_qty * np.random.uniform(0.1, 0.4))
        
        # Ensure minimum quantity
        quantity = max(1, quantity)
        
        # Add some variability for Data Centers based on power capacity
        if project_type == 'Data Center':
            power_factor = power_capacity / 25.0  # Normalize to 25MW baseline
            if primary_material == 104:  # HVAC for data centers
                quantity = int(quantity * power_factor * 1.2)
            elif primary_material == 103:  # Electrical for data centers
                quantity = int(quantity * power_factor * 1.1)
        
        return {
            'master_item': primary_material,
            'quantity': quantity,
            'confidence': weights[primary_material]
        }

    def get_material_name(self, master_item_no):
        """Get material name from item number"""
        materials = {
            101: 'Steel Reinforcement Bars',
            102: 'Concrete Mix',
            103: 'Electrical Cables',
            104: 'HVAC Equipment',
            105: 'Flooring Materials',
            106: 'Insulation Materials',
            107: 'Piping Systems',
            108: 'Fire Safety Equipment',
            109: 'Glass Panels',
            110: 'Roofing Materials'
        }
        return materials.get(master_item_no, f'Material {master_item_no}')