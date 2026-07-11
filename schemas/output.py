from pydantic import BaseModel, Field
from typing import List

class LunaResponse(BaseModel):
    message: str = Field(..., description="Friendly response to user")
    emotion: str = Field(..., description="happy, thinking, curious, surprised, relaxed")
    suggestions: List[str] = Field(default_factory=list)
    confidence: float = Field(..., ge=0, le=1)
