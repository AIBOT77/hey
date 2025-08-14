from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class TrafficData(BaseModel):
    timestamp: datetime
    location: str
    vehicle_count: int
    average_speed: float
    congestion_level: float

class AirQualityData(BaseModel):
    timestamp: datetime
    location: str
    pm25: float
    pm10: float
    ozone: float
    aqi: int

class EnergyData(BaseModel):
    timestamp: datetime
    consumption: float
    renewable_percentage: float
    grid_efficiency: float

class CityMetrics(BaseModel):
    timestamp: datetime
    traffic: dict
    air_quality: dict
    energy: dict
    population: dict

class PredictionResponse(BaseModel):
    predictions: List[dict]
    model_accuracy: float
    generated_at: datetime