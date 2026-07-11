from langchain_core.messages import HumanMessage

def hitl_node(state):
    """HITL Checkpoint with error handling"""
    itinerary = state.get("itinerary")
    
    # Error Handling for Missing Itinerary
    if not itinerary:
        return {
            "messages": [HumanMessage(content="Hmm... I don't have an itinerary ready yet. Tell me more about your trip (destination, dates, budget) so I can create one! 🌴")],
            "next": "router"
        }
    
    # Normal flow
    approval_prompt = f"""
    ✨ Proposed Itinerary for **{itinerary.destination}**
    Estimated Cost: ₹{itinerary.total_cost:,.0f}
    Status: {itinerary.status}
    
    Does this look good? Reply with:
    - yes (approve)
    - no (reject)
    - modify (tell me changes)
    """
    
    return {
        "messages": [HumanMessage(content=approval_prompt)],
        "next": "router"
    }
