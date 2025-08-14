import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import pickle
import os

class AirQualityPredictor:
    def __init__(self):
        self.model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def generate_synthetic_data(self, days=365):
        """Generate synthetic air quality data for training"""
        data = []
        start_date = datetime.now() - timedelta(days=days)
        
        for i in range(days):
            date = start_date + timedelta(days=i)
            month = date.month
            day_of_week = date.weekday()
            
            # Base AQI influenced by seasonal patterns
            base_aqi = 70
            
            # Seasonal effects
            if month in [12, 1, 2]:  # Winter - worse air quality
                base_aqi += 20
            elif month in [6, 7, 8]:  # Summer - better air quality
                base_aqi -= 10
                
            # Weekend effect (less traffic)
            if day_of_week >= 5:
                base_aqi -= 5
                
            # Weather simulation (simplified)
            wind_speed = np.random.uniform(5, 25)  # km/h
            humidity = np.random.uniform(30, 80)  # %
            temperature = np.random.uniform(-10, 35)  # Celsius
            
            # Wind reduces pollution
            wind_factor = max(0.5, 1 - (wind_speed - 5) / 40)
            base_aqi *= wind_factor
            
            # Add noise
            noise = np.random.normal(0, 15)
            aqi = max(20, min(200, base_aqi + noise))
            
            # Generate individual pollutants based on AQI
            pm25 = max(5, aqi * 0.3 + np.random.normal(0, 5))
            pm10 = max(10, pm25 * 1.5 + np.random.normal(0, 8))
            ozone = max(20, aqi * 0.4 + np.random.normal(0, 10))
            
            data.append({
                'month': month,
                'day_of_week': day_of_week,
                'wind_speed': wind_speed,
                'humidity': humidity,
                'temperature': temperature,
                'is_weekend': 1 if day_of_week >= 5 else 0,
                'aqi': aqi,
                'pm25': pm25,
                'pm10': pm10,
                'ozone': ozone
            })
        
        return pd.DataFrame(data)
    
    def train(self):
        """Train the air quality prediction model"""
        # Generate training data
        df = self.generate_synthetic_data()
        
        # Prepare features for AQI prediction
        features = ['month', 'day_of_week', 'wind_speed', 'humidity', 'temperature', 'is_weekend']
        X = df[features]
        y = df['aqi']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        print("Air quality prediction model trained successfully!")
        
    def predict_aqi(self, month, day_of_week, wind_speed, humidity, temperature):
        """Predict AQI for given conditions"""
        if not self.is_trained:
            self.train()
            
        is_weekend = 1 if day_of_week >= 5 else 0
        
        features = np.array([[month, day_of_week, wind_speed, humidity, temperature, is_weekend]])
        features_scaled = self.scaler.transform(features)
        
        prediction = self.model.predict(features_scaled)[0]
        return max(20, min(200, prediction))
    
    def predict_7_days(self):
        """Predict air quality for next 7 days"""
        predictions = []
        base_date = datetime.now()
        
        for i in range(7):
            future_date = base_date + timedelta(days=i)
            
            # Simulate weather conditions
            wind_speed = np.random.uniform(8, 20)
            humidity = np.random.uniform(40, 70)
            temperature = np.random.uniform(15, 25)
            
            predicted_aqi = self.predict_aqi(
                future_date.month,
                future_date.weekday(),
                wind_speed,
                humidity,
                temperature
            )
            
            # Determine health category
            if predicted_aqi <= 50:
                health_category = "Good"
            elif predicted_aqi <= 100:
                health_category = "Moderate"
            elif predicted_aqi <= 150:
                health_category = "Unhealthy for Sensitive Groups"
            else:
                health_category = "Unhealthy"
            
            # Determine dominant pollutant
            dominant_pollutant = np.random.choice(["PM2.5", "PM10", "Ozone"], 
                                                p=[0.4, 0.3, 0.3])
            
            predictions.append({
                'date': future_date.date().isoformat(),
                'predicted_aqi': int(predicted_aqi),
                'health_category': health_category,
                'dominant_pollutant': dominant_pollutant,
                'confidence': np.random.uniform(0.80, 0.95)
            })
        
        return predictions
    
    def analyze_pollution_sources(self):
        """Analyze and identify pollution sources using AI"""
        # Simulate AI-powered source identification
        sources = [
            {
                'type': 'Vehicle Emissions',
                'contribution': np.random.uniform(35, 45),
                'pollutants': ['NOx', 'CO', 'PM10'],
                'location_type': 'Major Roads'
            },
            {
                'type': 'Industrial',
                'contribution': np.random.uniform(20, 30),
                'pollutants': ['SO2', 'PM2.5', 'NOx'],
                'location_type': 'Industrial Zones'
            },
            {
                'type': 'Residential Heating',
                'contribution': np.random.uniform(15, 25),
                'pollutants': ['PM2.5', 'CO'],
                'location_type': 'Residential Areas'
            },
            {
                'type': 'Construction',
                'contribution': np.random.uniform(5, 15),
                'pollutants': ['PM10', 'PM2.5'],
                'location_type': 'Construction Sites'
            }
        ]
        
        return sources
    
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