from fastapi import FastAPI

from database import engine
from api import router
from db import tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(tables.Base.metadata.create_all)
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(router)