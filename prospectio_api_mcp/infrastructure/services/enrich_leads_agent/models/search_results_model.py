from pydantic import BaseModel


class SearchResultModel(BaseModel):
    """
    Represents a single search result with its metadata.
    """

    title: str = ""
    url: str = ""
    snippet: str = ""
