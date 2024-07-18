from transformers import AutoTokenizer, TFAutoModelForSeq2SeqLM
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    """load tokenizer and model on start of server"""
    global tokenizer, model
    tokenizer = AutoTokenizer.from_pretrained("/app/tokenizer", local_files_only=True)
    model = TFAutoModelForSeq2SeqLM.from_pretrained("/app/model", local_files_only=True)
    yield
    # model.clear()
    # tokenizer.clear()


app = FastAPI(title="Predict answer", lifespan=lifespan)


@app.get("/")
def home():
    return "Get your question answered by LLM"


@app.post("/predict")
def predict(prompt):
    """Generate answer for prompt"""
    inputs = tokenizer(prompt, return_tensors="tf").input_ids
    output = tokenizer.batch_decode(
        model.generate(input_ids=inputs, max_new_tokens=200), skip_special_tokens=True
    )
    return output[0]
