from langchain_core.messages import HumanMessage
from backend.utils.error_handler import safe_execute

def _explorer_logic(state):
    last_msg = state["messages"][-1].get("content", "").lower()
    dest = "Dream Destination"
    for d in ["bali", "goa", "paris", "maldives", "kerala"]:
        if d in last_msg:
            dest = d.title()
            break
    cards = f"🌟 Top Escapes for {dest}:\n1. Bliss\n2. Hidden Gems\n3. Adventure\n4. Luxury\n5. Soulful"
    return {
        "messages": [HumanMessage(content=cards)],
        "next": "router"
    }

def explorer_node(state):
    return safe_execute(_explorer_logic, state, "Explorer")
