import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import pickle
import os

class TrafficPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def generate_synthetic_data(self, days=365):
        """Generate synthetic traffic data for training"""
        data = []
        start_date = datetime.now() - timedelta(days=days)
        
        for i in range(days * 24):  # Hourly data
            timestamp = start_date + timedelta(hours=i)
            hour = timestamp.hour
            day_of_week = timestamp.weekday()
            month = timestamp.month
            
            # Create realistic traffic patterns
            base_traffic = 0.5
            
            # Rush hour patterns
            if 7 <= hour <= 9 or 17 <= hour <= 19:
                base_traffic += 0.3
            elif 22 <= hour or hour <= 5:
                base_traffic -= 0.3
                
            # Weekend patterns
            if day_of_week >= 5:  # Weekend
                base_traffic -= 0.1
                
            # Seasonal patterns
            if month in [6, 7, 8]:  # Summer
                base_traffic += 0.1
                
            # Add some noise
            noise = np.random.normal(0, 0.1)
            congestion = max(0, min(1, base_traffic + noise))
            
            data.append({
                'hour': hour,
                'day_of_week': day_of_week,
                'month': month,
                'is_weekend': 1 if day_of_week >= 5 else 0,
                'is_rush_hour': 1 if (7 <= hour <= 9 or 17 <= hour <= 19) else 0,
                'congestion': congestion
            })
        
        return pd.DataFrame(data)
    
    def train(self):
        """Train the traffic prediction model"""
        # Generate training data
        df = self.generate_synthetic_data()
        
        # Prepare features
        features = ['hour', 'day_of_week', 'month', 'is_weekend', 'is_rush_hour']
        X = df[features]
        y = df['congestion']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        print("Traffic prediction model trained successfully!")
        
    def predict(self, hour, day_of_week, month):
        """Predict traffic congestion for given time"""
        if not self.is_trained:
            self.train()
            
        is_weekend = 1 if day_of_week >= 5 else 0
        is_rush_hour = 1 if (7 <= hour <= 9 or 17 <= hour <= 19) else 0
        
        features = np.array([[hour, day_of_week, month, is_weekend, is_rush_hour]])
        features_scaled = self.scaler.transform(features)
        
        prediction = self.model.predict(features_scaled)[0]
        return max(0, min(1, prediction))
    
    def predict_24h(self):
        """Predict traffic for next 24 hours"""
        predictions = []
        base_time = datetime.now()
        
        for i in range(24):
            future_time = base_time + timedelta(hours=i)
            prediction = self.predict(
                future_time.hour,
                future_time.weekday(),
                future_time.month
            )
            
            predictions.append({
                'timestamp': future_time.isoformat(),
                'predicted_congestion': prediction,
                'confidence': np.random.uniform(0.85, 0.95)  # Simulated confidence
            })
        
        return predictions
    
    def save_model(self, filepath):
        """Save trained model to file"""
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'is_trained': self.is_trained
        }
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self, filepath):
        """Load trained model from file"""
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
                self.model = model_data['model']
                self.scaler = model_data['scaler']
                self.is_trained = model_data['is_trained']