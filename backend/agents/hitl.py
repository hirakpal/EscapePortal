from langchain_core.messages import HumanMessage

def hitl_node(state):
    """HITL Checkpoint - Waits for user approval"""
    itinerary = state.get("itinerary")
    if not itinerary:
        return {"next": "router"}
    
    approval_prompt = f"""
    Proposed Itinerary for {itinerary.destination}
    Total Cost: ₹{itinerary.total_cost}
    Status: {itinerary.status}
    
    Do you approve this plan? (yes/no/modify)
    """
    
    return {
        "messages": [HumanMessage(content=approval_prompt)],
        "next": "router"   # In full version, we would pause here
    }
