import re
import json
from pathlib import Path

class RegexPatterns:
    def __init__(self):
        self.patterns = {
            "destinations": re.compile(r"(bali|goa|paris|maldives|kerala|thailand|dubai|singapore|tokyo|new york)", re.IGNORECASE),
            "planning": re.compile(r"(plan|itinerary|schedule|trip|journey|book|travel)", re.IGNORECASE),
            "monitoring": re.compile(r"(monitor|status|check|update|alert|delay|problem)", re.IGNORECASE),
            "approval": re.compile(r"(yes|approve|confirm|ok|good)", re.IGNORECASE),
            "negative": re.compile(r"(no|reject|cancel|bad|issue)", re.IGNORECASE)
        }
    
    def load_from_file(self, filepath="patterns.json"):
        """Dynamic loading from JSON file"""
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
            for key, pattern in data.items():
                self.patterns[key] = re.compile(pattern, re.IGNORECASE)
        except:
            pass  # Keep defaults
    
    def match(self, text: str, category: str):
        """Match text against pattern"""
        if category in self.patterns:
            return bool(self.patterns[category].search(text))
        return False

# Global instance
patterns = RegexPatterns()
