from fastapi import FastAPI
import uvicorn
from myrtle.dino import brachiosaurus
from fastapi.responses import PlainTextResponse


app = FastAPI()


@app.get("/", response_class=PlainTextResponse)
async def root():
    return brachiosaurus("Hi")


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("myrtle.main:app", host="0.0.0.0", port=8000, reload=True)
