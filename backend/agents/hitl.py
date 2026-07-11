from langchain_core.messages import HumanMessage
from backend.utils.error_handler import safe_execute
from backend.utils.circuit_breaker import circuit_breaker

def _hitl_logic(state):
    if not state.get("itinerary"):
        return {
            "messages": [HumanMessage(content="No itinerary ready yet.")],
            "next": "router"
        }
    return {
        "messages": [HumanMessage(content="Proposed itinerary ready. Approve?")],
        "next": "router"
    }

def hitl_node(state):
    def wrapped():
        return _hitl_logic(state)
    return safe_execute(circuit_breaker.call(wrapped), state, "HITL")
