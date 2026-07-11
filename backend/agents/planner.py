from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from schemas.trip import TripItinerary, TripPreferences
from datetime import datetime, timedelta

def planner_node(state):
    """Planner Agent - Creates structured itineraries"""
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.7)
    
    prefs = state.get("preferences")
    if not prefs:
        prefs = TripPreferences(
            destination="Dream Destination",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=7),
            budget=50000,
            interests=["relaxation"]
        )
    
    prompt = f"""Create a beautiful 7-day itinerary for {prefs.destination}.
    Budget: ₹{prefs.budget}
    Interests: {prefs.interests}
    Keep it realistic and exciting."""
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    # Mock structured itinerary
    itinerary = TripItinerary(
        trip_id="trip_" + str(int(datetime.now().timestamp())),
        destination=prefs.destination,
        days=[{"day": i+1, "activities": ["Explore", "Relax"]} for i in range(7)],
        total_cost=prefs.budget * 0.85,
        status="planned"
    )
    
    return {
        "messages": [HumanMessage(content=f"Here's your personalized itinerary for {prefs.destination}!")],
        "itinerary": itinerary,
        "next": "router"
    }
