import asyncio
from fastapi import FastAPI
from bot import start_bot

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "ok", "service": "telegram-bot"}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_bot())
