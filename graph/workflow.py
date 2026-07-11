from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from .state import TripState

def router_node(state: TripState):
    """Decides next step based on last message"""
    if not state.get("messages"):
        return {"next": "luna_chat"}
    
    last_msg = state["messages"][-1].get("content", "").lower()
    
    if any(d in last_msg for d in ["bali", "goa", "paris", "maldives", "kerala"]):
        return {"next": "explorer"}
    elif "plan" in last_msg or "itinerary" in last_msg:
        return {"next": "planner"}
    else:
        return {"next": "luna_chat"}

def build_graph():
    workflow = StateGraph(TripState)
    
    workflow.add_node("router", router_node)
    # More nodes will be added in next steps
    
    workflow.set_entry_point("router")
    workflow.add_conditional_edges("router", lambda s: s.get("next", END))
    
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)
