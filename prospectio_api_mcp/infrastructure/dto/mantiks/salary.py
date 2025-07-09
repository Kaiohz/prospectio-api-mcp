from typing import Optional
from pydantic import BaseModel


class SalaryDTO(BaseModel):
    """
    Data Transfer Object representing the salary details for a job position.

    Attributes:
        min (Optional[int]): Minimum salary value.
        max (Optional[int]): Maximum salary value.
        type (Optional[str]): Type of salary (e.g., annual, monthly).
    """

    min: Optional[float] = None
    max: Optional[float] = None
    type: Optional[str] = None