import json
from datetime import datetime

class TravellerDNA:
    def __init__(self):
        self.profile = {
            "interests": [],
            "travel_style": "balanced",
            "budget_style": "mid_range",
            "trust_score": 0.0,
            "past_keywords": [],
            "last_updated": datetime.now().isoformat()
        }
    
    def update(self, prompt: str):
        prompt_lower = prompt.lower()
        if any(word in prompt_lower for word in ["beach", "relax", "peace"]):
            self.profile["interests"].append("beach")
            self.profile["travel_style"] = "relaxed"
        if any(word in prompt_lower for word in ["adventure", "trek", "hike"]):
            self.profile["interests"].append("adventure")
            self.profile["travel_style"] = "adventurous"
        if any(word in prompt_lower for word in ["budget", "cheap"]):
            self.profile["budget_style"] = "budget"
        if any(word in prompt_lower for word in ["luxury", "premium"]):
            self.profile["budget_style"] = "luxury"
        
        self.profile["trust_score"] = min(1.0, self.profile["trust_score"] + 0.1)
        self.profile["past_keywords"].append(prompt_lower[:60])
        self.profile["last_updated"] = datetime.now().isoformat()
    
    def get_profile(self):
        return self.profile

# Global instance
dna = TravellerDNA()