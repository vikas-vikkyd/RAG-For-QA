FROM python:3.9.1
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 90
COPY ./app /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "90"]