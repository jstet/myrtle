from fastapi import FastAPI
import uvicorn
from myrtle.dino import brachiosaurus
import pandas as pd
from myrtle.generate import generate
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from myrtle.helpers import download_model
from fastapi.responses import PlainTextResponse
import language_tool_python

app = FastAPI()

model_name = "jstet/myrtle"

context = {}


# Load the model during startup
@app.on_event("startup")
async def startup_event():
    # Load your model here
    download_model(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    eos_tokens = [
        int(tokenizer.convert_tokens_to_ids(".")),
        int(tokenizer.convert_tokens_to_ids("!")),
        int(tokenizer.convert_tokens_to_ids("?")),
    ]
    context["generator"] = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=60,
        no_repeat_ngram_size=3,
        repetition_penalty=1.2,
        eos_token_id=eos_tokens,
        pad_token_id=tokenizer.eos_token_id,
        top_p=0.9,
        temperature=0.6,
        top_k=50,
    )
    context["df"] = pd.read_csv("data/processed/processed_quotes.csv")
    context["gramm_checker"] = language_tool_python.LanguageTool("en-US")
    print("Model loaded")


@app.get("/", response_class=PlainTextResponse)
async def root():
    return brachiosaurus(generate(context["generator"], context["df"], context["gramm_checker"]))


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("myrtle.main:app", host="0.0.0.0", port=8000, reload=True)
