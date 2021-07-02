from fastapi import FastAPI

from .config import get_settings
from .db import database_connect, database_disconnect
from .items import items_router

settings = get_settings()

app = FastAPI(
    debug=settings.debug,
    on_startup=[database_connect],
    on_shutdown=[database_disconnect],
)

app.include_router(items_router)


@app.get('/')
async def read_root():
    return {'Hello': 'World'}
