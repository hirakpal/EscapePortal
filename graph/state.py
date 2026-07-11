from typing import TypedDict, Annotated, List, Optional
from operator import add
from datetime import datetime
from pydantic import BaseModel

class TripPreferences(BaseModel):
    destination: str
    start_date: datetime
    end_date: datetime
    budget: float
    travelers: int = 1
    interests: List[str] = []

class TripItinerary(BaseModel):
    trip_id: str
    destination: str
    days: List[dict]
    total_cost: float
    status: str = "planned"

class TripState(TypedDict):
    """Main state for the LangGraph"""
    messages: Annotated[list, add]                    # Chat history
    preferences: Optional[TripPreferences]
    itinerary: Optional[TripItinerary]
    dna_profile: dict = {}
    next: str                                         # Routing decision
