"""Test consumer for validating Kafka producer."""
import json
import os
from kafka import KafkaConsumer
from src.logger.logger import SparkModelLogger


def main():
    """Simple consumer to test the stock data stream."""
    logger = SparkModelLogger.get_logger("StockConsumer")

    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    topic = os.getenv("KAFKA_TOPIC", "stock-data")

    logger.info(f"Connecting to Kafka at {bootstrap_servers}")
    logger.info(f"Subscribing to topic: {topic}")

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='stock-consumer-test',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        key_deserializer=lambda x: x.decode('utf-8') if x else None,
    )

    logger.info("Consumer ready. Waiting for messages...")

    try:
        message_count = 0
        for message in consumer:
            message_count += 1
            stock_data = message.value

            logger.info(
                f"[{message_count}] {stock_data['symbol']}: "
                f"${stock_data['price']:.2f} | "
                f"Vol: {stock_data['volume']:,} | "
                f"Time: {stock_data['timestamp']}"
            )

            if message_count % 10 == 0:
                logger.info(f"Processed {message_count} messages")

    except KeyboardInterrupt:
        logger.info("Shutting down consumer...")
    finally:
        consumer.close()
        logger.info("Consumer closed")


if __name__ == "__main__":
    main()

