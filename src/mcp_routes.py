from collections.abc import Sequence
from fastapi import APIRouter
from mcp import Tool
from pydantic import BaseModel
from typing import Any, Dict, Optional
from application.api.routes import mcp_company_jobs
from mcp.types import (
    ContentBlock,
)

import httpx
from fastapi import Response, Request
from urllib.parse import urlparse, urlunparse


mcp_router = APIRouter()

headers = {
    "accept": "application/json, text/event-stream"
}

class MCPRequest(BaseModel):
    """
    Pydantic model for MCP tool list requests.
    This model is used to retrieve the list of available tools.
    """
    jsonrpc: str = "2.0"
    id: int = 1
    method: str = "tools/list"
    params: Optional[Dict[str, Any]] = None

@mcp_router.post(
    "/mcp/sse",
    summary="Call MCP via Swagger",
)
async def call_mcp_tool(request: MCPRequest, http_request: Request) -> Response:
    """
    Call an MCP tool via FastAPI, proxying the request to the external SSE endpoint using the current host and port.

    Args:
        request (MCPRequestTool): The request containing the tool name and arguments.
        http_request (Request): The incoming HTTP request (to extract host/port).

    Returns:
        Response: The response from the external SSE endpoint.
    """
    base_url = str(http_request.base_url).rstrip('/')
    parsed = urlparse(base_url)
    sse_netloc = parsed.hostname
    if parsed.port:
        sse_netloc += f":{parsed.port}"
    sse_url = urlunparse((parsed.scheme, sse_netloc, "/prospectio/mcp/sse", '', '', ''))

    async with httpx.AsyncClient() as client:
        response = await client.post(sse_url, json=request.model_dump(), headers=headers)
        return Response(
            content=response.content,
            status_code=response.status_code,
            media_type=response.headers.get("content-type", "application/json")
        )