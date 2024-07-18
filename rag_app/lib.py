import weaviate
import os
import json


def get_topk_documents(query, collection_name, k):
    """Get top k documents"""
    # define client
    client = weaviate.Client(
        url="http://localhost:8080",
        additional_headers={"X-HuggingFace-Api-Key": os.getenv("HUGGINGFACE_API_KEY")},
    )
    response = (
        client.query.get(collection_name, ["page_content"])
        .with_hybrid(query=query, alpha=0.5)
        .with_limit(int(k))
        .do()
    )
    results = response["data"]["Get"][collection_name]
    return results


def create_prompt(query, context):
    """Create prompt for LLM to use context"""
    # process context
    full_context = ""
    for cntxt in context:
        full_context += cntxt["page_content"] + "\n"

    # create prompt using context
    prompt = f"""
Use the following pieces of context to answer the question:
{full_context}
Question: {query}
Helpful Answer:
"""
    return prompt
