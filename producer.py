import os
import random
import time
import json
import logging
from kafka import KafkaProducer
from kafka.errors import KafkaError
from kafka.admin import KafkaAdminClient, NewTopic

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration from environment variables
KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "stock_topic")
RETRY_BACKOFF_MS = int(os.environ.get("RETRY_BACKOFF_MS", 1000))
MAX_RETRIES = int(os.environ.get("MAX_RETRIES", 3))
DEAD_LETTER_TOPIC = os.environ.get("DEAD_LETTER_TOPIC", "stock_topic_dlq")
SECURITY_PROTOCOL = os.environ.get("SECURITY_PROTOCOL", "SASL_PLAINTEXT")
SASL_MECHANISM = os.environ.get("SASL_MECHANISM", "SCRAM-SHA-512")
SASL_PLAIN_USERNAME = os.environ.get("SASL_PLAIN_USERNAME", "")
SASL_PLAIN_PASSWORD = os.environ.get("SASL_PLAIN_PASSWORD", "")

# List of 20 company symbols
COMPANY_SYMBOLS = [
    "AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "FB", "NVDA", "JPM", "V", "UNH",
    "HD", "PG", "MA", "BAC", "DIS", "CMCSA", "PYPL", "ADBE", "NFLX", "KO"
]

# Function to create topic
def create_kafka_topic(topic_name, num_partitions=1, replication_factor=1):
    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            client_id='stock_producer',
            security_protocol=SECURITY_PROTOCOL,
            sasl_mechanism=SASL_MECHANISM,
            sasl_plain_username=SASL_PLAIN_USERNAME,
            sasl_plain_password=SASL_PLAIN_PASSWORD
        )
        topic = NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
        admin_client.create_topics([topic])
        logging.info(f"Topic {topic_name} created successfully.")
    except Exception as e:
        logging.warning(f"Could not create topic {topic_name}: {e}")
    finally:
        if 'admin_client' in locals():
            admin_client.close()

# Create the topic
create_kafka_topic(KAFKA_TOPIC)
create_kafka_topic(DEAD_LETTER_TOPIC)

# Kafka producer configuration
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    api_version=(0, 10, 1),  # Specify Kafka version
    security_protocol=SECURITY_PROTOCOL,
    sasl_mechanism=SASL_MECHANISM,
    sasl_plain_username=SASL_PLAIN_USERNAME,
    sasl_plain_password=SASL_PLAIN_PASSWORD,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    retries=MAX_RETRIES,
    retry_backoff_ms=RETRY_BACKOFF_MS,
    #linger_ms=5, # Reduced linger time
)

def send_message(topic, message, retry_count=0):
    try:
        producer.send(topic, message).get()  # Get result to force synchronous sending
        logging.info(f"Message sent successfully: {message}")
    except KafkaError as e:
        logging.error(f"Failed to send message: {e}")
        if retry_count < MAX_RETRIES:
            time.sleep(RETRY_BACKOFF_MS / 1000)
            logging.info(f"Retrying message (attempt {retry_count + 1})...")
            send_message(topic, message, retry_count + 1)
        else:
            logging.error(f"Max retries reached. Sending to dead-letter topic: {DEAD_LETTER_TOPIC}")
            send_message(DEAD_LETTER_TOPIC, message)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    while True:
        # Select a random company symbol
        symbol = random.choice(COMPANY_SYMBOLS)

        # Generate random price
        price = round(random.uniform(100, 200), 2)

        # Get current timestamp
        timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

        # Create stock data
        stock_data = {
            'symbol': symbol,
            'price': price,
            'timestamp': timestamp
        }

        # Send the stock data to Kafka
        send_message(KAFKA_TOPIC, stock_data)

        # Wait for a short period before sending the next message
        time.sleep(1)  # Send every 1 second

    # Optional: Flush the producer to ensure all messages are sent
    # producer.flush()
    # producer.close() # Close producer after sending -  removed as it's a continuous producer now
