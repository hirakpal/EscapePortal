from langchain_core.messages import HumanMessage
from backend.utils.error_handler import safe_execute
from backend.utils.circuit_breaker import circuit_breaker
import random

def _monitor_logic(state):
    if random.random() < 0.3:
        return {
            "messages": [HumanMessage(content="⚠️ Monitoring Alert: Minor delay detected.")],
            "next": "router"
        }
    return {
        "messages": [HumanMessage(content="✅ All clear!")],
        "next": "router"
    }

def monitor_node(state):
    def wrapped():
        return _monitor_logic(state)
    return safe_execute(circuit_breaker.call(wrapped), state, "Monitor")
