"""Kafka producer for streaming stock data with proper logging and validation."""
import json
import random
import time
from typing import Optional

from kafka import KafkaProducer
from kafka.errors import KafkaError

from src.kafka.model import StockRecord
from src.logger.logger import KafkaModelLogger


class StockProducer:
    """Kafka producer for stock market data with Pydantic validation."""

    def __init__(
        self,
        bootstrap_servers: str = "localhost:9092",
        topic: str = "stock_prices",
        client_id: str = "stock-producer",
    ):
        """Initialize the Kafka producer.

        Args:
            bootstrap_servers: Kafka broker address
            topic: Kafka topic name
            client_id: Client identifier
        """
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.client_id = client_id
        self.logger = KafkaModelLogger.get_logger("StockProducer")
        self.producer: Optional[KafkaProducer] = None
        self._is_running = False
        self._message_count = 0

        # Stock symbols
        self.stocks = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA", "META", "NFLX"]

    def connect(self) -> None:
        """Establish connection to Kafka broker."""
        try:
            self.logger.info(f"Connecting to Kafka at {self.bootstrap_servers}")

            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                client_id=self.client_id,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                acks='all',
                retries=3,
                max_in_flight_requests_per_connection=5,
            )

            self.logger.info(f"✅ Successfully connected to Kafka broker")

        except KafkaError as e:
            self.logger.error(f"❌ Failed to connect to Kafka: {e}")
            raise

    def generate_stock_data(self) -> dict:
        """Generate random stock data.

        Returns:
            Dictionary with stock data
        """
        return {
            "symbol": random.choice(self.stocks),
            "price": round(random.uniform(100, 2000), 2),
            "volume": random.randint(100, 10000),
            "timestamp": time.time()
        }

    def send_record(self, record: StockRecord) -> None:
        """Send a validated stock record to Kafka.

        Args:
            record: Validated StockRecord instance
        """
        if not self.producer:
            raise RuntimeError("Producer not connected. Call connect() first.")

        try:
            # Send to Kafka with symbol as key (ensures same symbol goes to same partition)
            future = self.producer.send(
                self.topic,
                key=record.symbol.encode('utf-8'),  # Key determines partition
                value=record.model_dump()
            )

            # Add callbacks
            future.add_callback(self._on_send_success, record)
            future.add_errback(self._on_send_error, record)

            self._message_count += 1

        except Exception as e:
            self.logger.error(f"❌ Error sending record for {record.symbol}: {e}")

    def _on_send_success(self, metadata, record: StockRecord) -> None:
        """Callback for successful send."""
        self.logger.info(
            f"✅ {record.symbol:6s} | "
            f"${record.price:7.2f} | "
            f"Vol: {record.volume:6,d} | "
            f"📍 Partition: {metadata.partition} | "
            f"📌 Offset: {metadata.offset}"
        )

    def _on_send_error(self, exc, record: StockRecord) -> None:
        """Callback for send errors."""
        self.logger.error(f"❌ Failed to send {record.symbol}: {exc}")

    def start_streaming(self, interval: float = 20.0) -> None:
        """Start streaming stock data continuously.

        Args:
            interval: Time in seconds between messages
        """
        if not self.producer:
            self.connect()

        self._is_running = True
        self.logger.info(f"🚀 Starting stock data stream (interval={interval}s)")
        self.logger.info(f"📊 Tracking stocks: {', '.join(self.stocks)}")

        try:
            while self._is_running:
                # Generate random data
                data = self.generate_stock_data()

                # Validate using Pydantic model
                try:
                    record = StockRecord(**data)
                    self.send_record(record)
                except ValueError as e:
                    self.logger.error(f"❌ Validation error: {e}")
                    continue

                # Log stats every 10 messages
                if self._message_count % 10 == 0:
                    self.logger.info(f"📈 Total messages sent: {self._message_count}")

                # Wait before next message
                time.sleep(interval)

        except KeyboardInterrupt:
            self.logger.info("⚠️  Received interrupt signal, stopping stream...")
            self.stop()
        except Exception as e:
            self.logger.error(f"❌ Error during streaming: {e}")
            raise

    def stop(self) -> None:
        """Stop streaming and close the producer."""
        self._is_running = False

        if self.producer:
            self.logger.info("⏳ Flushing remaining messages...")
            self.producer.flush()

            self.logger.info("🛑 Closing Kafka producer...")
            self.producer.close()
            self.producer = None

            self.logger.info(
                f"✅ Producer stopped successfully. "
                f"Total messages sent: {self._message_count}"
            )

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
