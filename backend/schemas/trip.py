from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class TripPreferences(BaseModel):
    destination: str
    start_date: datetime
    end_date: datetime
    budget: float = Field(gt=0)
    travelers: int = 1
    interests: List[str] = Field(default_factory=list)
    travel_style: str = "balanced"

class ItineraryDay(BaseModel):
    date: datetime
    activities: List[Dict]
    meals: List[str] = []
    transport: str = ""

class TripItinerary(BaseModel):
    trip_id: str
    preferences: TripPreferences
    days: List[ItineraryDay]
    total_cost: float
    status: str = "planned"

class Disruption(BaseModel):
    type: str
    description: str
    impact: str
    suggested_actions: List[str]

class MonitoringUpdate(BaseModel):
    trip_id: str
    disruptions: List[Disruption] = []
    recommendations: List[str] = []
