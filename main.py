from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from database import engine
from api import router
from db import tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(tables.Base.metadata.create_all)
app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")

templates = Jinja2Templates(directory="frontend")

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("html/first_page.html", {"request": request})

app.include_router(router)