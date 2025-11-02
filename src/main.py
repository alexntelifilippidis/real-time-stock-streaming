from src.kafka.producer import StockProducer


def main():
    import os

    # Configure from environment or use defaults
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    topic = os.getenv("KAFKA_TOPIC", "stock_prices")

    # Create and run producer
    with StockProducer(bootstrap_servers=bootstrap_servers, topic=topic) as producer:
        producer.start_streaming(interval=20.0)


if __name__ == "__main__":
    main()