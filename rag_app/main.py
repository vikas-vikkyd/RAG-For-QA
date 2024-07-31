from lib import get_topk_documents, create_prompt
import requests
import json
from fastapi import FastAPI

app = FastAPI(title="Question Answering App")


@app.get("/")
def home():
    return "Get your question answered from ScienceBook"


@app.post("/getanswer")
def getanswer(query, collection_name="collection", k=5):
    """Main module"""
    # retrive contexts from database
    query_context = get_topk_documents(query, collection_name, k)

    # create prompt
    if query_context:
        prompt = create_prompt(query, query_context)

        # generate answer
        url = "http://localhost:90/predict"
        data = {"prompt": prompt}
        r = requests.post(url, params=data)
        return r.json()
    else:
        return "No Context Found!"
