from sqlmodel import StaticPool, create_engine

from .config import get_settings

settings = get_settings()

if settings.db_engine in ["sqlite", "sqlite+aiosqlite"]:
    DATABASE_URL = f"{settings.db_engine}:///:memory:"
    db_kwargs = {"connect_args": {"check_same_thread": False}}
else:
    DATABASE_URL = (
        f"{settings.db_engine}://"
        f"{settings.db_user}:{settings.db_password}@"
        f"{settings.db_host}/{settings.db_name}"
    )
    db_kwargs = {}

engine = create_engine(DATABASE_URL, echo=True, poolclass=StaticPool, **db_kwargs)
