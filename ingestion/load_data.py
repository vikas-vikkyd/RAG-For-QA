import weaviate
from weaviate.embedded import EmbeddedOptions
import os


def load(data, collection_name, client):
    """Module to load data"""
    with client.batch.configure(batch_size=10) as batch:
        for chunk in data:
            properties = {
                "file": chunk["file"],
                "page_number": chunk["page_number"],
                "page_content": chunk["page_content"],
            }
            # add data to collection
            batch.add_data_object(class_name=collection_name, data_object=properties)


def load_data(data, collection_name):
    """Module to load data"""

    # define client
    client = weaviate.Client(
        url="http://localhost:8080",
        additional_headers={"X-HuggingFace-Api-Key": os.getenv("HUGGINGFACE_API_KEY")},
    )
    # if collection exists add data to it
    if client.schema.exists(collection_name):
        print("Collection " + collection_name + " already exists")
        load(data, collection_name, client)
        print("data added to collection")
    else:
        collection = {
            "class": collection_name,
            "vectorizer": "text2vec-huggingface",
            "vectorIndexConfig": {"distance": "cosine"},
        }
        client.schema.create_class(collection)
        print("Collection " + collection_name + " created")
        load(data, collection_name, client)
        print("data added to collection")
