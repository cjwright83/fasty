from fastapi import FastAPI

from .config import get_settings
from .routers import api_routers

settings = get_settings()

app = FastAPI(
    debug=settings.debug,
)

for api_router in api_routers:
    app.include_router(api_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
