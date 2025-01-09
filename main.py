from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from api import router
from db import tables


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(tables.Base.metadata.create_all)
app = FastAPI()

app.include_router(router)

app.mount('/static', StaticFiles(directory='static'), 'static')

origins = [
    'http://127.0.0.1:8000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def root():
    return FileResponse('templates/index.html')