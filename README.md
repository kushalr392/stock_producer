# Stock Producer

This is a Kafka producer that sends stock data to a Kafka topic.

## Prerequisites

*   Docker
*   Docker Compose (optional)
*   Kafka cluster

## Configuration

The producer is configured using environment variables. You can set the following environment variables in the `config/config.env` file:

*   `KAFKA_BOOTSTRAP_SERVERS`: Kafka bootstrap servers (default: `localhost:9092`)
*   `KAFKA_TOPIC`: Kafka topic to send data to (default: `stock_topic`)
*   `RETRY_BACKOFF_MS`: Retry backoff in milliseconds (default: `1000`)
*   `MAX_RETRIES`: Maximum number of retries (default: `3`)
*   `DEAD_LETTER_TOPIC`: Dead-letter topic for failed messages (default: `stock_topic_dlq`)
*   `SECURITY_PROTOCOL`: Security protocol (default: `SASL_PLAINTEXT`)
*   `SASL_MECHANISM`: SASL mechanism (default: `SCRAM-SHA-512`)
*   `SASL_PLAIN_USERNAME`: SASL username
*   `SASL_PLAIN_PASSWORD`: SASL password

## Usage

1.  **Build the Docker image:**

    ```bash
    docker build -t stock-producer .
    ```

2.  **Run the producer:**

    You can run the producer using Docker directly, sourcing the environment variables from the `config/config.env` file:

    ```bash
    docker run --env-file config/config.env stock-producer
    ```

    Alternatively, you can use Docker Compose. Create a `docker-compose.yml` file:

    ```yaml
    version: "3.8"
    services:
      producer:
        image: stock-producer
        env_file:
          - ./config/config.env
    ```

    Then, run:

    ```bash
    docker-compose up
    ```

## Notes

*   Make sure the Kafka topic and dead-letter topic are created before running the producer. The producer attempts to create the topic, but it might fail if the Kafka cluster is not properly configured.
*   Replace `your_username` and `your_password` in the `config/config.env` file with your actual Kafka credentials.