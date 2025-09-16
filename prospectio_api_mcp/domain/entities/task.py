from pydantic import BaseModel

class Task(BaseModel):
    """Domain entity representing a background task."""
    task_id: str
    message: str
    status: str