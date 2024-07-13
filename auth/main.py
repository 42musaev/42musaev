from contextlib import asynccontextmanager

from api import router as api_v1_router
from db.db_helper import Base
from db.db_helper import sessionmanager
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with sessionmanager.get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
        await conn.run_sync(Base.metadata.drop_all)


app = FastAPI(lifespan=lifespan)
app.include_router(api_v1_router)
