from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from .state import TripState

def router_node(state: TripState):
    """Simple router - we'll expand this"""
    last_message = state["messages"][-1]["content"].lower() if state["messages"] else ""
    
    if any(word in last_message for word in ["bali", "goa", "paris", "maldives"]):
        return {"next": "explorer"}
    elif "plan" in last_message or "itinerary" in last_message:
        return {"next": "planner"}
    else:
        return {"next": "luna_chat"}

def build_basic_graph():
    workflow = StateGraph(TripState)
    
    # Add nodes (we'll implement them one by one)
    workflow.add_node("router", router_node)
    # workflow.add_node("explorer", explorer_node)  # coming soon
    # workflow.add_node("planner", planner_node)
    # workflow.add_node("luna_chat", luna_node)
    
    workflow.set_entry_point("router")
    workflow.add_conditional_edges("router", lambda s: s["next"])
    
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)
