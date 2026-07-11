from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from schemas.trip import TripItinerary, TripPreferences
from datetime import datetime, timedelta
from backend.utils.error_handler import safe_execute

# Gemini Function Calling Tools
@tool
def get_weather_tool(destination: str):
    """Get weather using Gemini function calling"""
    return {"condition": "Sunny", "temp_c": 28}

@tool
def google_maps_tool(origin: str, destination: str):
    """Get directions using Gemini function calling"""
    return {"distance": "500km", "duration": "6 hours", "route": "Via Highway"}

@tool
def google_search_tool(query: str):
    """Google Search using Gemini function calling"""
    return {"results": [f"Top result for {query}"]}

def _planner_logic(state):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.7)
    llm_with_tools = llm.bind_tools([get_weather_tool, google_maps_tool, google_search_tool])
    
    prefs = state.get("preferences") or TripPreferences(
        destination="Dream Place", start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=7), budget=50000
    )
    
    prompt = f"Plan trip to {prefs.destination}. Use tools for weather, maps, search."
    
    response = llm_with_tools.invoke([HumanMessage(content=prompt)])
    
    # Handle tool calls
    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call["name"] == "get_weather_tool":
                weather = get_weather_tool.invoke(tool_call["args"])
            elif tool_call["name"] == "google_maps_tool":
                maps = google_maps_tool.invoke(tool_call["args"])
            elif tool_call["name"] == "google_search_tool":
                search = google_search_tool.invoke(tool_call["args"])
    
    itinerary = TripItinerary(
        trip_id="trip_demo",
        destination=prefs.destination,
        days=[{"day": i+1, "activities": ["Explore"]} for i in range(7)],
        total_cost=prefs.budget * 0.85,
        status="planned"
    )
    
    return {
        "messages": [HumanMessage(content="Here's your itinerary with Gemini function calling!")],
        "itinerary": itinerary,
        "next": "router"
    }

def planner_node(state):
    return safe_execute(_planner_logic, state, "Planner")
