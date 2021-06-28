from fastapi import FastAPI

from .db import database
from .items import items_router

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(items_router)


@app.get('/')
async def read_root():
    return {'Hello': 'World'}
