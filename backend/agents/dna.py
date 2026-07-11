from langchain_core.messages import HumanMessage

def dna_learner_node(state):
    """DNA Learner - Builds Traveller DNA over time"""
    last_msg = state["messages"][-1].get("content", "").lower()
    
    dna = state.get("dna_profile", {
        "interests": [],
        "travel_style": "balanced",
        "budget_style": "mid_range",
        "trust_score": 0.0,
        "past_keywords": []
    })
    
    # Learn from message
    if any(word in last_msg for word in ["beach", "relax", "peace"]):
        dna["interests"].append("beach")
        dna["travel_style"] = "relaxed"
    if any(word in last_msg for word in ["adventure", "trek", "hike"]):
        dna["interests"].append("adventure")
        dna["travel_style"] = "adventurous"
    if any(word in last_msg for word in ["budget", "cheap", "affordable"]):
        dna["budget_style"] = "budget"
    if any(word in last_msg for word in ["luxury", "premium"]):
        dna["budget_style"] = "luxury"
    
    dna["trust_score"] = min(1.0, dna["trust_score"] + 0.08)
    dna["past_keywords"].append(last_msg[:50])
    
    return {
        "dna_profile": dna,
        "messages": [HumanMessage(content=f"Got it! Updating your Traveller DNA...")],
        "next": "router"
    }
