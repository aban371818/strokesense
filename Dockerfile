FROM python:3.10-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY stroke stroke
COPY strokesenseapp strokesenseapp

CMD uvicorn stroke.api_file:app --host 0.0.0.0 --port $PORT
