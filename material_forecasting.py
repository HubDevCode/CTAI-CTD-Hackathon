import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import warnings
warnings.filterwarnings('ignore')

class MaterialForecastingModel:
    def __init__(self):
        self.classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.regressor = RandomForestRegressor(n_estimators=100, random_state=42)
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_columns = []
        
    def create_synthetic_dataset(self, n_samples=1000):
        """Create synthetic training dataset based on construction project parameters"""
        np.random.seed(42)
        
        # Project types and their typical materials
        project_types = ['Data Center', 'Office Building', 'Residential Complex', 'Industrial Facility', 'Healthcare']
        regions = ['Maharashtra', 'Karnataka', 'Delhi', 'Gujarat', 'Tamil Nadu']
        
        # Material categories with item numbers
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
        
        data = []
        for i in range(n_samples):
            project_type = np.random.choice(project_types)
            region = np.random.choice(regions)
            
            # Generate project parameters
            if project_type == 'Data Center':
                power_capacity = np.random.uniform(10, 50)  # MW
                area = np.random.uniform(50000, 300000)  # sq ft
                material_weights = [0.15, 0.25, 0.20, 0.15, 0.05, 0.05, 0.05, 0.05, 0.03, 0.02]
            elif project_type == 'Office Building':
                power_capacity = np.random.uniform(2, 15)
                area = np.random.uniform(20000, 150000)
                material_weights = [0.20, 0.30, 0.15, 0.10, 0.10, 0.05, 0.05, 0.03, 0.02, 0.00]
            else:
                power_capacity = np.random.uniform(1, 20)
                area = np.random.uniform(10000, 200000)
                material_weights = [0.18, 0.28, 0.12, 0.08, 0.12, 0.08, 0.06, 0.04, 0.02, 0.02]
            
            # Select material based on project type
            master_item_no = np.random.choice(list(materials.keys()), p=material_weights)
            
            # Calculate quantity based on project size and material type
            base_qty = area / 1000  # Base quantity per 1000 sq ft
            
            if master_item_no in [101, 102]:  # Steel, Concrete - high volume
                qty_shipped = int(base_qty * np.random.uniform(0.8, 1.5))
            elif master_item_no in [103, 107]:  # Cables, Piping - medium volume
                qty_shipped = int(base_qty * np.random.uniform(0.3, 0.8))
            else:  # Other materials - lower volume
                qty_shipped = int(base_qty * np.random.uniform(0.1, 0.4))
            
            qty_shipped = max(1, qty_shipped)  # Ensure minimum quantity
            
            data.append({
                'id': i + 1,
                'project_type': project_type,
                'region': region,
                'power_capacity_mw': power_capacity,
                'area_sqft': area,
                'MasterItemNo': master_item_no,
                'QtyShipped': qty_shipped
            })
        
        return pd.DataFrame(data)
    
    def prepare_features(self, df):
        """Prepare features for training"""
        feature_df = df.copy()
        
        # Encode categorical variables
        for col in ['project_type', 'region']:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                feature_df[col + '_encoded'] = self.label_encoders[col].fit_transform(feature_df[col])
            else:
                feature_df[col + '_encoded'] = self.label_encoders[col].transform(feature_df[col])
        
        # Select feature columns
        self.feature_columns = ['project_type_encoded', 'region_encoded', 'power_capacity_mw', 'area_sqft']
        X = feature_df[self.feature_columns]
        
        return X
    
    def train(self, df):
        """Train both classification and regression models"""
        X = self.prepare_features(df)
        y_class = df['MasterItemNo']
        y_reg = df['QtyShipped']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Split data
        X_train, X_test, y_class_train, y_class_test, y_reg_train, y_reg_test = train_test_split(
            X_scaled, y_class, y_reg, test_size=0.2, random_state=42
        )
        
        # Train models
        self.classifier.fit(X_train, y_class_train)
        self.regressor.fit(X_train, y_reg_train)
        
        # Evaluate models
        class_pred = self.classifier.predict(X_test)
        reg_pred = self.regressor.predict(X_test)
        
        accuracy = accuracy_score(y_class_test, class_pred)
        f1 = f1_score(y_class_test, class_pred, average='weighted')
        mae = mean_absolute_error(y_reg_test, reg_pred)
        
        # Calculate composite score
        y_reg_range = y_reg_test.max() - y_reg_test.min()
        norm_mae = mae / y_reg_range if y_reg_range > 0 else 0
        reg_score = max(0, 1 - norm_mae)
        final_score = 0.25 * accuracy + 0.25 * f1 + 0.5 * reg_score
        
        print(f"Model Performance:")
        print(f"Classification Accuracy: {accuracy:.4f}")
        print(f"Classification F1-Score: {f1:.4f}")
        print(f"Regression MAE: {mae:.4f}")
        print(f"Regression Score: {reg_score:.4f}")
        print(f"Final Composite Score: {final_score:.4f}")
        
        return {
            'accuracy': accuracy,
            'f1_score': f1,
            'mae': mae,
            'reg_score': reg_score,
            'final_score': final_score
        }
    
    def predict(self, df):
        """Make predictions on new data"""
        X = self.prepare_features(df)
        X_scaled = self.scaler.transform(X)
        
        master_item_pred = self.classifier.predict(X_scaled)
        qty_pred = self.regressor.predict(X_scaled)
        qty_pred = np.maximum(1, np.round(qty_pred).astype(int))  # Ensure positive integers
        
        return master_item_pred, qty_pred
    
    def save_model(self, filepath):
        """Save trained model"""
        model_data = {
            'classifier': self.classifier,
            'regressor': self.regressor,
            'label_encoders': self.label_encoders,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns
        }
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self, filepath):
        """Load trained model"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.classifier = model_data['classifier']
        self.regressor = model_data['regressor']
        self.label_encoders = model_data['label_encoders']
        self.scaler = model_data['scaler']
        self.feature_columns = model_data['feature_columns']

def main():
    # Initialize model
    model = MaterialForecastingModel()
    
    # Create synthetic dataset
    print("Creating synthetic dataset...")
    train_data = model.create_synthetic_dataset(n_samples=2000)
    print(f"Dataset created with {len(train_data)} samples")
    
    # Display dataset info
    print("\nDataset Info:")
    print(train_data.head())
    print(f"\nDataset shape: {train_data.shape}")
    print(f"Material distribution:\n{train_data['MasterItemNo'].value_counts().sort_index()}")
    
    # Train model
    print("\nTraining model...")
    performance = model.train(train_data)
    
    # Save model
    model.save_model('material_forecasting_model.pkl')
    print("\nModel saved as 'material_forecasting_model.pkl'")
    
    # Create test case for Data Center project
    test_data = pd.DataFrame({
        'id': [1, 2, 3, 4],
        'project_type': ['Data Center', 'Data Center', 'Data Center', 'Data Center'],
        'region': ['Maharashtra', 'Maharashtra', 'Maharashtra', 'Maharashtra'],
        'power_capacity_mw': [25, 25, 25, 25],
        'area_sqft': [200000, 200000, 200000, 200000]
    })
    
    # Make predictions
    master_items, quantities = model.predict(test_data)
    
    # Create submission file
    submission_df = pd.DataFrame({
        'id': test_data['id'],
        'MasterItemNo': master_items,
        'QtyShipped': quantities
    })
    
    submission_df.to_csv('submission.csv', index=False)
    print(f"\nSubmission file created:")
    print(submission_df)
    
    return model, train_data, performance

if __name__ == "__main__":
    model, data, perf = main()