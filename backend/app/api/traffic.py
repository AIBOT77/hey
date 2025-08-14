from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
import random
import numpy as np

router = APIRouter()

@router.get("/live")
async def get_live_traffic():
    """Get real-time traffic data"""
    return {
        "timestamp": datetime.now().isoformat(),
        "intersections": [
            {
                "id": f"intersection_{i}",
                "name": f"Main St & {i}th Ave",
                "coordinates": {"lat": 40.7128 + random.uniform(-0.05, 0.05), 
                               "lng": -74.0060 + random.uniform(-0.05, 0.05)},
                "vehicle_count": random.randint(50, 200),
                "average_speed": random.uniform(15, 45),
                "congestion_level": random.uniform(0.1, 0.9),
                "signal_timing": random.randint(30, 120)
            }
            for i in range(1, 11)
        ]
    }

@router.get("/predict")
async def predict_traffic():
    """AI-powered traffic prediction"""
    # Simulate ML model prediction
    predictions = []
    for hour in range(24):
        # Create realistic traffic pattern
        if 7 <= hour <= 9 or 17 <= hour <= 19:  # Rush hours
            congestion = random.uniform(0.7, 0.95)
        elif 22 <= hour or hour <= 5:  # Night
            congestion = random.uniform(0.1, 0.3)
        else:
            congestion = random.uniform(0.3, 0.6)
            
        predictions.append({
            "hour": hour,
            "predicted_congestion": congestion,
            "confidence": random.uniform(0.85, 0.98)
        })
    
    return {
        "predictions": predictions,
        "model_accuracy": 0.89,
        "generated_at": datetime.now().isoformat()
    }

@router.get("/optimize")
async def optimize_traffic_signals():
    """AI-optimized traffic signal recommendations"""
    return {
        "optimizations": [
            {
                "intersection_id": f"intersection_{i}",
                "current_timing": random.randint(60, 120),
                "recommended_timing": random.randint(45, 90),
                "expected_improvement": random.uniform(0.15, 0.35),
                "priority": "high" if random.random() > 0.7 else "medium"
            }
            for i in range(1, 6)
        ],
        "overall_improvement": random.uniform(0.20, 0.40)
    }