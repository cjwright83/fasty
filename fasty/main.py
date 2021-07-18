from fastapi import FastAPI

from .config import get_settings
from .db import database_connect, database_disconnect
from .routers import api_routers

settings = get_settings()

app = FastAPI(
    debug=settings.debug,
    on_startup=[database_connect],
    on_shutdown=[database_disconnect],
)

for api_router in api_routers:
    app.include_router(api_router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
