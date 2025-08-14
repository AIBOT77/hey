from fastapi import APIRouter
from datetime import datetime, timedelta
import random

router = APIRouter()

@router.get("/incidents")
async def get_active_incidents():
    """Get current emergency incidents"""
    incident_types = ["Fire", "Medical Emergency", "Traffic Accident", "Gas Leak", "Power Outage"]
    
    return {
        "timestamp": datetime.now().isoformat(),
        "active_incidents": [
            {
                "id": f"INC-{random.randint(1000, 9999)}",
                "type": random.choice(incident_types),
                "severity": random.choice(["Low", "Medium", "High", "Critical"]),
                "location": {
                    "address": f"{random.randint(100, 999)} Main St",
                    "coordinates": {"lat": 40.7128 + random.uniform(-0.1, 0.1),
                                   "lng": -74.0060 + random.uniform(-0.1, 0.1)}
                },
                "reported_at": (datetime.now() - timedelta(minutes=random.randint(5, 180))).isoformat(),
                "status": random.choice(["Reported", "Dispatched", "En Route", "On Scene"]),
                "resources_assigned": random.randint(1, 4),
                "estimated_resolution": (datetime.now() + timedelta(minutes=random.randint(15, 120))).isoformat()
            }
            for _ in range(random.randint(2, 8))
        ]
    }

@router.get("/response-optimization")
async def optimize_emergency_response():
    """AI-optimized emergency response routing"""
    return {
        "optimizations": [
            {
                "incident_id": f"INC-{random.randint(1000, 9999)}",
                "current_eta": random.randint(8, 15),  # minutes
                "optimized_eta": random.randint(5, 10),
                "route_improvement": random.uniform(15, 40),  # percentage
                "recommended_units": [
                    f"Unit-{random.randint(100, 999)}" for _ in range(random.randint(1, 3))
                ]
            }
            for _ in range(random.randint(3, 6))
        ],
        "overall_response_improvement": random.uniform(20, 35)
    }

@router.get("/risk-assessment")
async def get_risk_assessment():
    """AI-powered city risk assessment"""
    return {
        "risk_zones": [
            {
                "zone_id": f"zone_{i}",
                "coordinates": {
                    "center": {"lat": 40.7128 + random.uniform(-0.1, 0.1),
                              "lng": -74.0060 + random.uniform(-0.1, 0.1)},
                    "radius": random.uniform(0.5, 2.0)  # km
                },
                "risk_level": random.choice(["Low", "Medium", "High"]),
                "risk_factors": random.sample([
                    "High traffic density", "Old infrastructure", "Industrial area",
                    "Dense population", "Limited emergency access", "Weather exposure"
                ], random.randint(2, 4)),
                "probability_score": random.uniform(0.1, 0.9),
                "impact_score": random.uniform(0.3, 0.8)
            }
            for i in range(1, 8)
        ],
        "generated_at": datetime.now().isoformat()
    }