from langchain_core.messages import HumanMessage
from backend.utils.error_handler import safe_execute
from backend.utils.circuit_breaker import circuit_breaker

def _execute_logic(state):
    itinerary = state.get("itinerary")
    if not itinerary:
        return {"messages": [HumanMessage(content="Nothing to execute yet.")], "next": "router"}
    itinerary.status = "confirmed"
    return {
        "messages": [HumanMessage(content=f"✅ Trip confirmed! Safe travels!")],
        "itinerary": itinerary,
        "next": "router"
    }

def execute_node(state):
    def wrapped():
        return _execute_logic(state)
    return safe_execute(circuit_breaker.call(wrapped), state, "Execute")
