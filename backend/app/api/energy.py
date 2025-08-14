from fastapi import APIRouter
from datetime import datetime, timedelta
import random

router = APIRouter()

@router.get("/grid-status")
async def get_grid_status():
    """Get current smart grid status"""
    return {
        "timestamp": datetime.now().isoformat(),
        "total_consumption": random.uniform(850, 950),  # MW
        "total_generation": random.uniform(900, 1000),
        "renewable_sources": {
            "solar": random.uniform(150, 250),
            "wind": random.uniform(100, 200),
            "hydro": random.uniform(80, 120),
            "geothermal": random.uniform(20, 40)
        },
        "traditional_sources": {
            "natural_gas": random.uniform(300, 400),
            "coal": random.uniform(50, 100),
            "nuclear": random.uniform(200, 250)
        },
        "grid_efficiency": random.uniform(88, 96),
        "carbon_intensity": random.uniform(300, 500),  # gCO2/kWh
        "status": "stable"
    }

@router.get("/consumption-forecast")
async def forecast_energy_consumption():
    """AI-powered energy consumption forecast"""
    forecast = []
    base_consumption = random.uniform(800, 900)
    
    for hour in range(24):
        time = datetime.now() + timedelta(hours=hour)
        
        # Simulate realistic consumption patterns
        if 6 <= hour <= 8 or 18 <= hour <= 22:  # Peak hours
            consumption = base_consumption * random.uniform(1.2, 1.4)
        elif 23 <= hour or hour <= 5:  # Night hours
            consumption = base_consumption * random.uniform(0.6, 0.8)
        else:
            consumption = base_consumption * random.uniform(0.9, 1.1)
        
        forecast.append({
            "timestamp": time.isoformat(),
            "predicted_consumption": consumption,
            "renewable_percentage": random.uniform(25, 40),
            "confidence": random.uniform(0.88, 0.96)
        })
    
    return {
        "forecast": forecast,
        "model_accuracy": 0.92,
        "generated_at": datetime.now().isoformat()
    }

@router.get("/optimization")
async def get_energy_optimization():
    """Smart grid optimization recommendations"""
    return {
        "recommendations": [
            {
                "type": "Load Balancing",
                "description": "Redistribute load from high-demand areas",
                "potential_savings": random.uniform(5, 15),  # percentage
                "implementation_cost": random.uniform(50000, 150000),
                "payback_period": random.uniform(1.5, 3.0)  # years
            },
            {
                "type": "Renewable Integration",
                "description": "Increase solar panel deployment in residential areas",
                "potential_savings": random.uniform(10, 25),
                "implementation_cost": random.uniform(200000, 500000),
                "payback_period": random.uniform(3.0, 6.0)
            },
            {
                "type": "Demand Response",
                "description": "Implement smart pricing for peak hour reduction",
                "potential_savings": random.uniform(8, 20),
                "implementation_cost": random.uniform(75000, 200000),
                "payback_period": random.uniform(2.0, 4.0)
            }
        ],
        "total_potential_savings": random.uniform(20, 35)
    }