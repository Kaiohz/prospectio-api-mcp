from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class JSearchParametersDTO(BaseModel):
    """
    Data Transfer Object representing the parameters of a JSearch API request.

    Attributes:
        query (Optional[str]): The search query string.
        page (Optional[int]): The current page number.
        num_pages (Optional[int]): The total number of pages.
        date_posted (Optional[str]): The date the job was posted.
        country (Optional[str]): The country for the search.
        language (Optional[str]): The language for the search.
    """
    query: Optional[str] = None
    page: Optional[int] = None
    num_pages: Optional[int] = None
    date_posted: Optional[str] = None
    country: Optional[str] = None
    language: Optional[str] = None

class JSearchResponseDTO(BaseModel):
    """
    Data Transfer Object representing the response from the JSearch API.

    Attributes:
        status (Optional[str]): The status of the response.
        request_id (Optional[str]): The unique request identifier.
        parameters (Optional[JSearchParametersDTO]): The parameters used for the request.
        data (Optional[List[Dict[str, Any]]]): The list of data items returned by the API.
    """
    status: Optional[str] = None
    request_id: Optional[str] = None
    parameters: Optional[JSearchParametersDTO] = None
    data: Optional[List[Dict[str, Any]]] = None
