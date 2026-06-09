FROM python:3.10-slim
WORKDIR /app
COPY app/web_app/requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
COPY app/web_app/ ./web_app/
COPY src/ ./src/
ENV PYTHONPATH=/app:/app/web_app
CMD ["sh", "-c", "cd /app/web_app && python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]