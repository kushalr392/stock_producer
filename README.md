# Stock Producer

This project simulates stock data for 20 companies and continuously produces the data to a Kafka topic.

## Prerequisites

*   Kafka cluster
*   Python 3.6+
*   Kafka Python client library (`kafka-python`)

## Installation

1.  Clone the repository.
2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Configure the following environment variables:

*   `KAFKA_BOOTSTRAP_SERVERS`: Kafka broker address (default: `localhost:9092`)
*   `KAFKA_TOPIC`: Kafka topic to produce to (default: `stock_topic`)
*   `RETRY_BACKOFF_MS`: Retry backoff in milliseconds (default: `1000`)
*   `MAX_RETRIES`: Maximum number of retries (default: `3`)
*   `DEAD_LETTER_TOPIC`: Dead-letter topic for failed messages (default: `stock_topic_dlq`)
*   `SECURITY_PROTOCOL`: Security protocol for Kafka connection (default: `SASL_PLAINTEXT`)
*   `SASL_MECHANISM`: SASL mechanism for authentication (default: `SCRAM-SHA-512`)
*   `SASL_PLAIN_USERNAME`: SASL username (if applicable)
*   `SASL_PLAIN_PASSWORD`: SASL password (if applicable)

Example `.env` file:

```
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC=stock_topic
RETRY_BACKOFF_MS=1000
MAX_RETRIES=3
DEAD_LETTER_TOPIC=stock_topic_dlq
SECURITY_PROTOCOL=SASL_PLAINTEXT
SASL_MECHANISM=SCRAM-SHA-512
SASL_PLAIN_USERNAME=your_username
SASL_PLAIN_PASSWORD=your_password
```

## Usage

1.  Set the environment variables.
2.  Run the producer:
    ```bash
    python producer.py
    ```

## Docker

You can also run the producer using Docker.

1.  Build the Docker image:
    ```bash
    docker build -t stock-producer .
    ```
2.  Run the Docker container:
    ```bash
    docker run -e KAFKA_BOOTSTRAP_SERVERS=<kafka_broker> -e KAFKA_TOPIC=<topic_name> -e SECURITY_PROTOCOL=SASL_PLAINTEXT -e SASL_MECHANISM=SCRAM-SHA-512 -e SASL_PLAIN_USERNAME=<username> -e SASL_PLAIN_PASSWORD=<password> stock-producer
    ```

Replace `<kafka_broker>`, `<topic_name>`, `<username>`, and `<password>` with your actual values.
