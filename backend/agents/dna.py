from langchain_core.messages import HumanMessage
from backend.utils.error_handler import safe_execute

def _dna_logic(state):
    dna = state.get("dna_profile", {
        "interests": [],
        "travel_style": "balanced",
        "budget_style": "mid_range",
        "trust_score": 0.0,
        "past_keywords": []
    })
    
    last_msg = state["messages"][-1].get("content", "").lower()
    
    if any(word in last_msg for word in ["beach", "relax", "peace"]):
        dna["interests"].append("beach")
        dna["travel_style"] = "relaxed"
    if any(word in last_msg for word in ["adventure", "trek", "hike"]):
        dna["interests"].append("adventure")
        dna["travel_style"] = "adventurous"
    if any(word in last_msg for word in ["budget", "cheap"]):
        dna["budget_style"] = "budget"
    if any(word in last_msg for word in ["luxury", "premium"]):
        dna["budget_style"] = "luxury"
    
    dna["trust_score"] = min(1.0, dna["trust_score"] + 0.1)
    dna["past_keywords"].append(last_msg[:60])
    
    return {
        "dna_profile": dna,
        "next": "router"
    }

def dna_learner_node(state):
    return safe_execute(_dna_logic, state, "DNA Learner")
