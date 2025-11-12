FROM python:3.9-slim-buster

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY producer.py .
COPY config/config.env ./config/

# Set environment variables
ENV KAFKA_BOOTSTRAP_SERVERS=$KAFKA_BOOTSTRAP_SERVERS
ENV KAFKA_TOPIC=$KAFKA_TOPIC
ENV RETRY_BACKOFF_MS=$RETRY_BACKOFF_MS
ENV MAX_RETRIES=$MAX_RETRIES
ENV DEAD_LETTER_TOPIC=$DEAD_LETTER_TOPIC
ENV SECURITY_PROTOCOL=$SECURITY_PROTOCOL
ENV SASL_MECHANISM=$SASL_MECHANISM
ENV SASL_PLAIN_USERNAME=$SASL_PLAIN_USERNAME
ENV SASL_PLAIN_PASSWORD=$SASL_PLAIN_PASSWORD

# Command to run the application
CMD ["python", "producer.py"]