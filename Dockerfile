FROM python:3.9-slim-buster

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY producer.py .
COPY config/config.env ./config/

# Command to run the application
CMD ["python", "producer.py"]