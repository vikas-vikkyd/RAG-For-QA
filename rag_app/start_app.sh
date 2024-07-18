sudo lsof -t -i tcp:8000 | xargs kill -9
 HUGGINGFACE_API_KEY=$1 fastapi run rag_app/main.py
