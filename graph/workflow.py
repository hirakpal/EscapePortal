from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from .state import TripState
from backend.agents.luna import luna_chat_node
from backend.agents.explorer import explorer_node
from backend.agents.hitl import hitl_node

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
    workflow.add_node("luna_chat", luna_chat_node)
    workflow.add_node("explorer", explorer_node)
    workflow.add_node("hitl", hitl_node)
    
    workflow.set_entry_point("router")
    workflow.add_conditional_edges("router", lambda s: s.get("next", END))

    # Return edges
    workflow.add_edge("planner", "hitl")
    workflow.add_edge("hitl", "router")
    workflow.add_edge("luna_chat", "router")
    workflow.add_edge("explorer", "router")
    
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)
