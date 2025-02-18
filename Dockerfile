FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Expose the port that Gunicorn will run on
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Run migrations, collectstatic, and start Gunicorn
CMD ["sh", "-c","uvicorn api:app --host 0.0.0.0 --port 8000"]
