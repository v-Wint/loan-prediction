FROM python:3.10-slim
WORKDIR /app
COPY app/prediction_service/requirements.txt .
RUN apt-get update && apt-get install -y libgomp1 && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
COPY src/ ./src/
COPY model.lgbm .
COPY bins.npy .
COPY app/prediction_service/ ./app/prediction_service/
ENV PYTHONPATH=/app
CMD ["uvicorn", "app.prediction_service.main:app", "--host", "0.0.0.0", "--port", "8001"]
