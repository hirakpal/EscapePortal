from langchain_core.messages import HumanMessage
from backend.utils.error_handler import safe_execute
import random

def _monitor_logic(state):
    """Real-time trip monitoring"""
    itinerary = state.get("itinerary")
    if not itinerary:
        return {"next": "router"}
    
    # Simulate monitoring
    if random.random() < 0.3:
        return {
            "messages": [HumanMessage(content="⚠️ Monitoring Alert: Minor flight delay detected. Suggesting alternative.")],
            "next": "router"
        }
    
    return {
        "messages": [HumanMessage(content="✅ All clear! Trip is monitoring smoothly.")],
        "next": "router"
    }

def monitor_node(state):
    return safe_execute(_monitor_logic, state, "Monitor")
