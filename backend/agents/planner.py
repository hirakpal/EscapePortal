from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from schemas.trip import TripItinerary, TripPreferences
from datetime import datetime, timedelta
from backend.utils.error_handler import safe_execute
from backend.utils.circuit_breaker import circuit_breaker

def _planner_logic(state):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.7)
    prefs = state.get("preferences") or TripPreferences(
        destination="Dream Place", start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=7), budget=50000
    )
    itinerary = TripItinerary(
        trip_id="trip_demo",
        destination=prefs.destination,
        days=[{"day": i+1, "activities": ["Explore"]} for i in range(7)],
        total_cost=prefs.budget * 0.85,
        status="planned"
    )
    return {
        "messages": [HumanMessage(content="Here's your itinerary!")],
        "itinerary": itinerary,
        "next": "router"
    }

def planner_node(state):
    def wrapped():
        return _planner_logic(state)
    return safe_execute(circuit_breaker.call(wrapped), state, "Planner")
