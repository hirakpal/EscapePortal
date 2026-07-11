from langchain_core.messages import HumanMessage
from backend.utils.error_handler import safe_execute

def _hitl_logic(state):
    itinerary = state.get("itinerary")
    if not itinerary:
        return {
            "messages": [HumanMessage(content="No itinerary ready yet. Tell me more details!")],
            "next": "router"
        }
    return {
        "messages": [HumanMessage(content=f"Proposed itinerary for {itinerary.destination} ready. Approve?")],
        "next": "router"
    }

def hitl_node(state):
    return safe_execute(_hitl_logic, state, "HITL")
