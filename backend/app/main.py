from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import asyncio
import json
import random
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any
import uvicorn

# Import our modules
from .api import traffic, air_quality, energy, emergency
from .core.config import settings
from .models.schemas import CityMetrics, TrafficData, AirQualityData
from .services.websocket_manager import ConnectionManager

app = FastAPI(
    title="Smart City AI Dashboard API",
    description="AI-powered real-time dashboard for smart city management",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
manager = ConnectionManager()

# Include API routers
app.include_router(traffic.router, prefix="/api/traffic", tags=["traffic"])
app.include_router(air_quality.router, prefix="/api/air-quality", tags=["air-quality"])
app.include_router(energy.router, prefix="/api/energy", tags=["energy"])
app.include_router(emergency.router, prefix="/api/emergency", tags=["emergency"])

@app.get("/")
async def root():
    return {"message": "Smart City AI Dashboard API", "version": "1.0.0"}

@app.get("/api/dashboard/overview")
async def get_dashboard_overview():
    """Get overall city metrics for the main dashboard"""
    return {
        "timestamp": datetime.now().isoformat(),
        "traffic": {
            "congestion_level": random.uniform(0.2, 0.8),
            "average_speed": random.uniform(25, 45),
            "incidents": random.randint(0, 5)
        },
        "air_quality": {
            "aqi": random.randint(50, 150),
            "pm25": random.uniform(10, 50),
            "co2": random.uniform(380, 420)
        },
        "energy": {
            "consumption": random.uniform(85, 95),
            "renewable_percentage": random.uniform(25, 35),
            "grid_efficiency": random.uniform(88, 96)
        },
        "population": {
            "current_density": random.uniform(0.6, 0.9),
            "public_transport_usage": random.uniform(0.4, 0.7)
        }
    }

@app.get("/api/predictions/traffic")
async def get_traffic_predictions():
    """Get AI-powered traffic predictions for the next 24 hours"""
    predictions = []
    base_time = datetime.now()
    
    for i in range(24):
        hour = base_time + timedelta(hours=i)
        # Simulate realistic traffic patterns
        hour_of_day = hour.hour
        if 7 <= hour_of_day <= 9 or 17 <= hour_of_day <= 19:  # Rush hours
            congestion = random.uniform(0.7, 0.95)
        elif 22 <= hour_of_day or hour_of_day <= 5:  # Night hours
            congestion = random.uniform(0.1, 0.3)
        else:
            congestion = random.uniform(0.3, 0.6)
        
        predictions.append({
            "timestamp": hour.isoformat(),
            "predicted_congestion": congestion,
            "confidence": random.uniform(0.8, 0.95)
        })
    
    return {"predictions": predictions}

@app.get("/api/analytics/city-health")
async def get_city_health_score():
    """Calculate and return overall city health score based on multiple metrics"""
    metrics = {
        "traffic_efficiency": random.uniform(0.6, 0.9),
        "air_quality_score": random.uniform(0.5, 0.8),
        "energy_sustainability": random.uniform(0.7, 0.9),
        "public_safety": random.uniform(0.8, 0.95),
        "citizen_satisfaction": random.uniform(0.6, 0.85)
    }
    
    overall_score = sum(metrics.values()) / len(metrics)
    
    return {
        "overall_score": overall_score,
        "grade": "A" if overall_score > 0.8 else "B" if overall_score > 0.6 else "C",
        "metrics": metrics,
        "recommendations": [
            "Optimize traffic light timing during rush hours",
            "Increase renewable energy sources",
            "Deploy more air quality sensors in industrial areas"
        ]
    }

@app.websocket("/ws/realtime")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time data streaming"""
    await manager.connect(websocket)
    try:
        while True:
            # Generate and send real-time data
            data = {
                "timestamp": datetime.now().isoformat(),
                "traffic": {
                    "live_count": random.randint(150, 300),
                    "average_speed": random.uniform(20, 50),
                    "congestion_points": [
                        {"lat": 40.7128 + random.uniform(-0.1, 0.1), 
                         "lng": -74.0060 + random.uniform(-0.1, 0.1),
                         "severity": random.uniform(0.1, 1.0)}
                        for _ in range(random.randint(3, 8))
                    ]
                },
                "air_quality": {
                    "pm25": random.uniform(15, 45),
                    "pm10": random.uniform(20, 60),
                    "ozone": random.uniform(40, 80),
                    "locations": [
                        {"lat": 40.7128 + random.uniform(-0.1, 0.1),
                         "lng": -74.0060 + random.uniform(-0.1, 0.1),
                         "aqi": random.randint(50, 120)}
                        for _ in range(5)
                    ]
                },
                "energy": {
                    "current_load": random.uniform(80, 100),
                    "renewable_generation": random.uniform(20, 40),
                    "grid_status": "stable"
                }
            }
            
            await manager.broadcast(json.dumps(data))
            await asyncio.sleep(5)  # Send updates every 5 seconds
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/api/ml/model-status")
async def get_ml_model_status():
    """Get status of all ML models"""
    return {
        "models": {
            "traffic_prediction": {
                "status": "active",
                "accuracy": 0.89,
                "last_trained": "2024-01-15T10:30:00Z"
            },
            "air_quality_forecast": {
                "status": "active", 
                "accuracy": 0.85,
                "last_trained": "2024-01-14T15:45:00Z"
            },
            "energy_optimization": {
                "status": "active",
                "accuracy": 0.92,
                "last_trained": "2024-01-16T08:20:00Z"
            }
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)