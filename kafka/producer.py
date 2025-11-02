"""Example usage of the stock Kafka producer."""
import os
from src.kafka import StockKafkaProducer, KafkaConfig


def example_basic_usage():
    """Basic usage example with context manager."""
    # Create configuration
    config = KafkaConfig(
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
        topic="stock-data",
        client_id="example-producer",
    )

    # Define stocks to track
    symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA"]

    # Use context manager for automatic cleanup
    with StockKafkaProducer(config, symbols) as producer:
        # Stream 5 data points per second
        producer.start_streaming(interval=0.2, batch_size=5)


def example_manual_control():
    """Example with manual control over producer."""
    config = KafkaConfig(
        bootstrap_servers="localhost:9092",
        topic="stock-data",
    )

    producer = StockKafkaProducer(config, symbols=["AAPL", "TSLA"])

    try:
        producer.connect()

        # Generate and send a single batch
        batch = producer.data_generator.generate_batch(10)
        producer.send_batch(batch)

        print(f"Sent {len(batch)} messages successfully!")

    finally:
        producer.stop()


if __name__ == "__main__":
    # Run the basic example
    example_basic_usage()

