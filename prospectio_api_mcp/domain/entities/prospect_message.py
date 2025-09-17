from pydantic import BaseModel, Field

class ProspectMessage(BaseModel):
    """Response model for prospecting message generation."""

    subject : str = Field(..., description="Generated subject line for the prospecting message")
    message: str = Field(..., description="Generated prospecting message")
