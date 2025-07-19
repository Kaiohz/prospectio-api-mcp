from pydantic import BaseModel, Field


class CompatibilityScore(BaseModel):
    """Response model for compatibility score calculation."""
    
    score: int = Field(..., ge=0, le=100, description="Compatibility score from 0 to 100")
