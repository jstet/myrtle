from fastapi import FastAPI
import uvicorn
from myrtle.dino import brachiosaurus
from myrtle.generate import generate
from myrtle.helpers import download_model
from fastapi.responses import PlainTextResponse

app = FastAPI()

model = "jstet/myrtle"


@app.get("/", response_class=PlainTextResponse)
async def root():
    return brachiosaurus(generate(model, "The truth"))


def start():
    """Launched with `poetry run start` at root level"""
    download_model(model)
    uvicorn.run("myrtle.main:app", host="0.0.0.0", port=8000, reload=True)
