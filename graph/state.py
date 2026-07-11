from typing import TypedDict, Annotated, List
from operator import add
from schemas.trip import TripPreferences, TripItinerary, MonitoringUpdate

class TripState(TypedDict):
    messages: Annotated[list, add]          # Chat history
    preferences: TripPreferences | None
    itinerary: TripItinerary | None
    monitoring: MonitoringUpdate | None
    dna_update: dict | None                 # Traveller DNA signals
    next: str                               # Routing decision
