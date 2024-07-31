# RAG Application
For this implementation of Retrieval-Augmented Generation we have different components
 
## Vector database
This implementation is using weaviate as a vector database to store the chunks or texts which will be used as a context to LLM. To start the database run “start_database.sh” in the vector_database folder which will start the container for the database running on your local system, pass the hugging face api key which will be used for creating embeddings.

## Ingestion
We have an ingestion pipeline, which on a high level does four things: it reads the pdf files, creates chunks using LangChain, creates embeddings using a hugging face sentence transformer model and saves the data to a vector database.

## LLM
This implementation serves the Large Language Model on a local machine using FastAPI, which can’t be an efficient way to serve the model, but to execute everything on the local system I am doing so. Run save_model.sh in the llm folder which will download the model and tokenizer from hugging hace and will save it to local, pass the model name to be used.
Run deployment.sh in the llm folder which will create a docker image for model serving and will create an endpoint using FastAPI to serve the model.

## RAG
Run start_app.sh from the rag_app folder which will create an endpoint for RAG application which will accept query for question answering. On high level RAH app does following steps
- Accept the query
- Query the vector database and get the context relevant to query
- Create prompt using template with context and query
- Pass the prompt to LLM
- Return answer


## Steps
- Create virtual environment using `python -m venv envrag`
- Activate environment using `source envrag/bin/activate`
- Run `pip install -r requirements.txt`
- Run `./start_database.sh` pass hugging face api key
- Run `./ingestion/ingestion.sh` to ingest data, pass source data path and collection name
- Run `./llm/save_model.sh` to download and save model from hugging face, pass model id
- Run `./llm/deployment.sh` to serve the model
- Run `./rag_app/start_app.sh` to start the RAG app, pass hugging face api key

## References
+ https://python.langchain.com/v0.2/docs/introduction/
+ https://weaviate.io/developers/weaviate

