from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from .state import TripState

from backend.agents.luna import luna_chat_node
from backend.agents.explorer import explorer_node
from backend.agents.planner import planner_node
from backend.agents.dna import dna_learner_node
from backend.agents.hitl import hitl_node
from backend.agents.execute import execute_node
from backend.agents.monitor import monitor_node

from backend.utils.regex_patterns import patterns

def router_node(state: TripState):
    """Dynamic Router with Regex Patterns"""
    if not state.get("messages"):
        return {"next": "luna_chat"}
    
    last_msg = state["messages"][-1].get("content", "").lower()
    
    # Dynamic Regex Matching
    if patterns.match(last_msg, "destinations"):
        return {"next": "explorer"}
    elif patterns.match(last_msg, "planning"):
        return {"next": "planner"}
    elif patterns.match(last_msg, "monitoring"):
        return {"next": "monitor"}
    elif patterns.match(last_msg, "approval"):
        return {"next": "execute"}
    elif patterns.match(last_msg, "negative"):
        return {"next": "luna_chat"}
    
    # Safe default
    return {"next": "luna_chat"}

def build_graph():
    workflow = StateGraph(TripState)
    
    workflow.add_node("router", router_node)
    workflow.add_node("luna_chat", luna_chat_node)
    workflow.add_node("explorer", explorer_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("dna_learner", dna_learner_node)
    workflow.add_node("hitl", hitl_node)
    workflow.add_node("execute", execute_node)
    workflow.add_node("monitor", monitor_node)
    
    workflow.set_entry_point("router")
    workflow.add_conditional_edges("router", lambda s: s.get("next", END))
    
    # Return edges
    workflow.add_edge("luna_chat", "router")
    workflow.add_edge("explorer", "router")
    workflow.add_edge("planner", "hitl")
    workflow.add_edge("hitl", "execute")
    workflow.add_edge("execute", "monitor")
    workflow.add_edge("dna_learner", "router")
    
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)
