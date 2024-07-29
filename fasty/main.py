from fastapi import FastAPI

from .config import get_settings
from .db import lifespan
from .routers import api_routers

settings = get_settings()

app = FastAPI(
    debug=settings.debug,
    lifespan=lifespan,
)

for api_router in api_routers:
    app.include_router(api_router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
