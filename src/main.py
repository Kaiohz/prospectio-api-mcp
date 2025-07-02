import contextlib
from fastapi import FastAPI
from infrastructure.api.routes import mcp
from infrastructure.api.routes import api_router

# Create a combined lifespan to manage both session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(mcp.session_manager.run())
        yield

app = FastAPI(title="Prospectio API", lifespan=lifespan)
REST_PATH = "/rest/v1"
MCP_PATH = "/prospectio/"

app.include_router(api_router, prefix=REST_PATH, tags=["Prospects"])
app.mount(MCP_PATH, mcp.streamable_http_app())





