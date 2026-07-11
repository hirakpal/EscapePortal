from langchain_core.messages import HumanMessage
from backend.utils.error_handler import safe_execute

def _execute_logic(state):
    itinerary = state.get("itinerary")
    if not itinerary:
        return {"messages": [HumanMessage(content="Nothing to execute yet.")], "next": "router"}
    
    itinerary.status = "confirmed"
    
    return {
        "messages": [HumanMessage(content=f"✅ Trip to {itinerary.destination} is confirmed! Safe travels! 🌴")],
        "itinerary": itinerary,
        "next": "router"
    }

def execute_node(state):
    return safe_execute(_execute_logic, state, "Execute")
