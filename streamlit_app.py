import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Construction Material Forecasting Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .chatbot-container {
        background-color: #ffffff;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class MaterialForecastingApp:
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the trained model"""
        try:
            with open('material_forecasting_model.pkl', 'rb') as f:
                model_data = pickle.load(f)
            self.model = model_data
            return True
        except FileNotFoundError:
            st.error("Model file not found. Please train the model first.")
            return False
    
    def predict_materials(self, project_data):
        """Make material predictions"""
        if not self.model:
            return None, None
        
        # Prepare input data
        df = pd.DataFrame([project_data])
        
        # Encode categorical variables
        for col in ['project_type', 'region']:
            if col in self.model['label_encoders']:
                df[col + '_encoded'] = self.model['label_encoders'][col].transform(df[col])
        
        # Select features
        X = df[self.model['feature_columns']]
        X_scaled = self.model['scaler'].transform(X)
        
        # Make predictions
        master_item_pred = self.model['classifier'].predict(X_scaled)[0]
        qty_pred = max(1, int(self.model['regressor'].predict(X_scaled)[0]))
        
        return master_item_pred, qty_pred
    
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

def main():
    app = MaterialForecastingApp()
    
    # Header
    st.markdown('<h1 class="main-header">🏗️ Construction Material Forecasting Platform</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Material Forecasting", "Vendor Search", "Project Schedule", "Procurement Plan", "Chatbot"])
    
    if page == "Material Forecasting":
        show_forecasting_page(app)
    elif page == "Vendor Search":
        show_vendor_page()
    elif page == "Project Schedule":
        show_schedule_page()
    elif page == "Procurement Plan":
        show_procurement_page()
    elif page == "Chatbot":
        show_chatbot_page()

def show_forecasting_page(app):
    st.header("Material Demand Forecasting")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Project Parameters")
        project_type = st.selectbox("Project Type", 
                                  ['Data Center', 'Office Building', 'Residential Complex', 'Industrial Facility', 'Healthcare'])
        region = st.selectbox("Region", 
                            ['Maharashtra', 'Karnataka', 'Delhi', 'Gujarat', 'Tamil Nadu'])
        power_capacity = st.number_input("Power Capacity (MW)", min_value=1.0, max_value=100.0, value=25.0, step=0.1)
        area = st.number_input("Built-up Area (sq ft)", min_value=1000, max_value=1000000, value=200000, step=1000)
        
        if st.button("Generate Forecast", type="primary"):
            project_data = {
                'project_type': project_type,
                'region': region,
                'power_capacity_mw': power_capacity,
                'area_sqft': area
            }
            
            master_item, quantity = app.predict_materials(project_data)
            
            if master_item and quantity:
                st.session_state['forecast_result'] = {
                    'master_item': master_item,
                    'quantity': quantity,
                    'material_name': app.get_material_name(master_item),
                    'project_data': project_data
                }
    
    with col2:
        st.subheader("Forecast Results")
        if 'forecast_result' in st.session_state:
            result = st.session_state['forecast_result']
            
            st.markdown(f"""
            <div class="metric-card">
                <h3>Primary Material Required</h3>
                <p><strong>Material:</strong> {result['material_name']}</p>
                <p><strong>Item Number:</strong> {result['master_item']}</p>
                <p><strong>Quantity:</strong> {result['quantity']} units</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Create visualization
            fig = go.Figure(data=[
                go.Bar(x=['Predicted Quantity'], y=[result['quantity']], 
                      text=[f"{result['quantity']} units"], textposition='auto',
                      marker_color='lightblue')
            ])
            fig.update_layout(title=f"Material Forecast: {result['material_name']}")
            st.plotly_chart(fig, use_container_width=True)

def show_vendor_page():
    st.header("Vendor Identification")
    
    if 'forecast_result' in st.session_state:
        result = st.session_state['forecast_result']
        material_name = result['material_name']
        region = result['project_data']['region']
        
        st.write(f"Searching vendors for: **{material_name}** in **{region}**")
        
        # Simulated vendor data
        vendors = [
            {"name": "Mumbai Steel Works", "location": "Mumbai, Maharashtra", "rating": 4.5, "price_range": "₹15,000-20,000/ton"},
            {"name": "Pune Construction Supplies", "location": "Pune, Maharashtra", "rating": 4.2, "price_range": "₹14,500-19,500/ton"},
            {"name": "Nashik Materials Co.", "location": "Nashik, Maharashtra", "rating": 4.0, "price_range": "₹16,000-21,000/ton"}
        ]
        
        for vendor in vendors:
            with st.expander(f"🏢 {vendor['name']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Location:** {vendor['location']}")
                with col2:
                    st.write(f"**Rating:** ⭐ {vendor['rating']}/5")
                with col3:
                    st.write(f"**Price Range:** {vendor['price_range']}")
    else:
        st.info("Please generate a material forecast first to see relevant vendors.")

def show_schedule_page():
    st.header("Project Schedule & Timeline")
    
    # Create Gantt chart
    tasks = [
        dict(Task="Project Planning", Start='2024-01-01', Finish='2024-01-15', Resource="Planning Team"),
        dict(Task="Material Procurement", Start='2024-01-10', Finish='2024-02-10', Resource="Procurement"),
        dict(Task="Site Preparation", Start='2024-01-20', Finish='2024-02-15', Resource="Construction"),
        dict(Task="Foundation Work", Start='2024-02-16', Finish='2024-03-30', Resource="Construction"),
        dict(Task="Structural Work", Start='2024-04-01', Finish='2024-07-31', Resource="Construction"),
        dict(Task="MEP Installation", Start='2024-06-01', Finish='2024-09-30', Resource="MEP Team"),
        dict(Task="Finishing Work", Start='2024-08-01', Finish='2024-10-31', Resource="Finishing"),
        dict(Task="Testing & Commissioning", Start='2024-11-01', Finish='2024-11-30', Resource="Testing")
    ]
    
    fig = px.timeline(tasks, x_start="Start", x_end="Finish", y="Task", color="Resource")
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(title="Data Center Construction Schedule", height=500)
    st.plotly_chart(fig, use_container_width=True)

def show_procurement_page():
    st.header("Procurement Management Plan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Procurement Strategy")
        st.write("""
        **Key Procurement Phases:**
        1. **Planning Phase** (Week 1-2)
           - Material requirement analysis
           - Vendor identification and qualification
           
        2. **Sourcing Phase** (Week 3-4)
           - RFQ/RFP process
           - Vendor evaluation and selection
           
        3. **Contracting Phase** (Week 5-6)
           - Contract negotiation
           - Terms and conditions finalization
           
        4. **Execution Phase** (Week 7+)
           - Purchase order management
           - Delivery tracking and quality control
        """)
    
    with col2:
        st.subheader("Risk Mitigation")
        st.write("""
        **Identified Risks:**
        - Material price volatility
        - Supply chain disruptions
        - Quality issues
        - Delivery delays
        
        **Mitigation Strategies:**
        - Multiple vendor partnerships
        - Strategic inventory management
        - Quality assurance protocols
        - Contingency planning
        """)

def show_chatbot_page():
    st.header("AI Procurement Assistant")
    
    st.markdown("""
    <div class="chatbot-container">
        <h3>🤖 Ask me about your construction project!</h3>
        <p>I can help you with material forecasting, vendor selection, scheduling, and procurement planning.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your AI procurement assistant. How can I help you with your construction project today?"}
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about materials, vendors, or schedules..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        response = generate_chatbot_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

def generate_chatbot_response(prompt):
    """Generate chatbot response based on user input"""
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ['material', 'forecast', 'predict']):
        return """
        Based on your project parameters, I can predict the materials you'll need. 
        For a typical Data Center project (25MW, 200k sq ft), you might need:
        - Steel Reinforcement Bars: ~160 units
        - Concrete Mix: ~200 units  
        - Electrical Cables: ~80 units
        
        Would you like me to generate a detailed forecast for your specific project?
        """
    elif any(word in prompt_lower for word in ['vendor', 'supplier', 'source']):
        return """
        I can help you find qualified vendors in your region. For Maharashtra, 
        I recommend these top-rated suppliers:
        
        🏢 Mumbai Steel Works (Rating: 4.5/5)
        🏢 Pune Construction Supplies (Rating: 4.2/5)
        🏢 Nashik Materials Co. (Rating: 4.0/5)
        
        Would you like detailed information about any specific vendor?
        """
    elif any(word in prompt_lower for word in ['schedule', 'timeline', 'gantt']):
        return """
        I can help you plan your project timeline. A typical Data Center construction follows this schedule:
        
        📅 Planning: 2 weeks
        📅 Procurement: 4 weeks  
        📅 Construction: 8 months
        📅 Testing: 1 month
        
        The key is to start material procurement early to avoid delays. Would you like a detailed Gantt chart?
        """
    else:
        return """
        I'm here to help with construction material forecasting, vendor identification, 
        project scheduling, and procurement planning. You can ask me about:
        
        • Material quantity predictions
        • Vendor recommendations  
        • Project timelines
        • Procurement strategies
        
        What specific aspect would you like to explore?
        """

if __name__ == "__main__":
    main()