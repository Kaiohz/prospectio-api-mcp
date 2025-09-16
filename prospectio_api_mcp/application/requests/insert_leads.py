from pydantic import BaseModel


class InsertLeadsRequest(BaseModel):
    """
    Request model for inserting leads.
    
    Attributes:
        source (str): The source from which to get leads.
        location (str): The country code for the location.
        job_params (list[str]): List of job titles to filter leads.
    """
    source: str
    location: str
    job_params: list[str]