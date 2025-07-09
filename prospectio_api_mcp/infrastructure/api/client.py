from typing import Any, Dict, Optional
import httpx


class BaseApiClient:
    """
    Generic HTTP client for consuming external lead APIs.
    Uses httpx.AsyncClient for asynchronous requests.
    """

    def __init__(
        self,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: float = 30.0,
    ) -> None:
        """
        Initialize the client with a base URL, optional headers, and a timeout.

        Args:
            base_url (str): The base URL of the API.
            headers (Optional[Dict[str, str]]): Default HTTP headers.
            timeout (float): Timeout in seconds for HTTP requests.
        """
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self._client = httpx.AsyncClient(
            base_url=self.base_url, headers=self.headers, timeout=timeout
        )

    async def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> httpx.Response:
        """
        Perform an asynchronous GET request.

        Args:
            endpoint (str): Relative path of the endpoint.
            params (Optional[Dict[str, Any]]): Optional query parameters.

        Returns:
            httpx.Response: The HTTP response object.
        """
        response = await self._client.get(endpoint, params=params)
        return response

    async def post(
        self, endpoint: str, data: Optional[Any] = None, json: Optional[Any] = None
    ) -> httpx.Response:
        """
        Perform an asynchronous POST request.

        Args:
            endpoint (str): Relative path of the endpoint.
            data (Optional[Any]): Data to send in the request body.
            json (Optional[Any]): JSON data to send in the request body.

        Returns:
            httpx.Response: The HTTP response object.
        """
        return await self._client.post(endpoint, data=data, json=json)

    async def close(self) -> None:
        """
        Properly close the HTTPX client.
        """
        await self._client.aclose()
