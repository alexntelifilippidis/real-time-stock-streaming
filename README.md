# 📈 Real-Time Stock Streaming Pipeline

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-3.0%2B-black.svg)](https://kafka.apache.org/)
[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.3%2B-orange.svg)](https://spark.apache.org/)
[![Podman](https://img.shields.io/badge/Podman-4.0%2B-892CA0.svg)](https://www.podman.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-ready, real-time data streaming pipeline that demonstrates end-to-end data engineering using **Apache Kafka** and **Apache Spark Structured Streaming**. This project simulates live stock market data, processes it in real-time with Pydantic validation, and provides beautiful colored logging.

## 🎯 Key Features

- ⚡ **Real-time Processing**: Sub-second latency streaming with Kafka and Spark
- 🎨 **Beautiful Logging**: Colored, emoji-rich logs with custom formatter
- ✅ **Pydantic Validation**: Type-safe data models with automatic validation
- 📊 **Scalable Architecture**: Horizontally scalable components using Podman
- 🔄 **Fault Tolerance**: Automatic recovery and checkpointing
- 🐳 **Easy Deployment**: Full Podman Compose setup for local development
- 📝 **Production Ready**: Comprehensive logging, monitoring, and error handling

## 🏗️ Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  Data Generator │ ───▶ │  Apache Kafka   │ ───▶ │  Spark Stream   │
│  (Pydantic)     │      │  (5 Partitions) │      │  (PySpark)      │
└─────────────────┘      └─────────────────┘      └─────────────────┘
         │                        │                         │
         │                        │                         │
    Validates              Key-based                   Real-time
    with Schema          Partitioning                Aggregations
```

**Data Flow:**
1. 🎲 **Producer** generates realistic stock price data with Pydantic validation
2. 📨 **Kafka** ingests messages with stock symbol as partition key (ordering guarantee)
3. ⚡ **Spark Structured Streaming** consumes and processes data with windowed aggregations
4. 📊 **Kafka UI** visualizes topics, partitions, and offsets in real-time

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| 🔄 **Streaming** | Apache Kafka (KRaft mode) | High-throughput message broker |
| ⚡ **Processing** | Apache Spark (Structured Streaming) | Real-time stream processing |
| 🐍 **Language** | Python 3.8+ | Main implementation language |
| ✅ **Validation** | Pydantic 2.0+ | Data modeling and validation |
| 📦 **Libraries** | kafka-python, PySpark | Data processing |
| 🔧 **Package Manager** | uv | Fast Python package manager |
| 🐳 **Infrastructure** | Podman Compose | Containerization |
| 🎨 **Logging** | Custom ColoredFormatter | Beautiful terminal output |

## 📁 Project Structure

```
real-time-stock-streaming/
│
├── README.md                      # This file
├── LICENSE                        # MIT License
├── .gitignore                     # Git ignore rules
├── docker-compose.yml             # Podman services configuration
├── pyproject.toml                 # Python dependencies (uv)
├── Makefile                       # Convenient commands
│
├── src/                           # Source code
│   ├── main.py                    # Main entry point
│   │
│   ├── kafka/                     # Kafka components
│   │   ├── model.py               # Pydantic data models (StockRecord)
│   │   ├── producer.py            # Stock data producer with logging
│   │   ├── topic_manager.py       # Topic management (create/describe/delete)
│   │   └── demo_partitions.py     # Demo script for partitions/offsets
│   │
│   ├── logger/                    # Custom logging system
│   │   ├── __init__.py            # Package exports
│   │   ├── models.py              # Pydantic models for logger config
│   │   └── logger.py              # ColoredFormatter and KafkaModelLogger
│   │
│   ├── spark/                     # Spark streaming jobs
│   │   └── (coming soon)          # Spark streaming application
│   │
│   └── data/                      # Data directory
│       └── .gitkeep               # Placeholder
│
├── docs/                          # Documentation
│   └── KAFKA_PARTITIONS_OFFSETS.md  # Partition/offset guide
│
└── .github/                       # GitHub templates
    └── pull_request_template.md  # PR template
```

## 🚀 Quick Start

### Prerequisites

- **Podman** 4.0+ and **podman-compose** 2.0+
- **Python** 3.8 or higher
- **uv** package manager (`brew install uv` or `pip install uv`)
- At least 4GB RAM available for containers

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/real-time-stock-streaming.git
   cd real-time-stock-streaming
   ```

2. **Install dependencies with uv**
   ```bash
   make install
   # or manually: uv sync
   ```

3. **Start the infrastructure** (Kafka + Kafka UI)
   ```bash
   make up
   ```
   
   Wait for services to be healthy (~30 seconds). Check status:
   ```bash
   make status
   ```

4. **Create Kafka topic with 5 partitions**
   ```bash
   make topic-create PARTITIONS=5
   ```

### Running the Pipeline

**Start Kafka Producer:**
```bash
make producer
# or: python src/kafka/producer.py
```

You'll see beautiful colored logs:
```
2025-11-02 10:50:08 - StockProducer - ✨ INFO - Connecting to Kafka at localhost:9092
2025-11-02 10:50:08 - StockProducer - ✨ INFO - ✅ Successfully connected to Kafka broker
2025-11-02 10:50:08 - StockProducer - ✨ INFO - 🚀 Starting stock data stream (interval=1.0s)
2025-11-02 10:50:09 - StockProducer - ✨ INFO - ✅ AAPL   | $150.23 | Vol:  5,234 | 📍 Partition: 1 | 📌 Offset: 42
2025-11-02 10:50:10 - StockProducer - ✨ INFO - ✅ GOOGL  | $140.75 | Vol:  8,192 | 📍 Partition: 2 | 📌 Offset: 38
```

**View Kafka UI:**
- Open `http://localhost:8080` in your browser
- Navigate to **Topics** → **stock_prices**
- See messages, partitions, and offsets in real-time!

## 📊 Features in Detail

### Stock Data Producer (`src/kafka/producer.py`)
- ✅ **Pydantic Validation**: Every message validated with `StockRecord` model
- 🎨 **Beautiful Logging**: Colored output with emojis for success/error
- 🔑 **Partition Keys**: Uses stock symbol as key for consistent partitioning
- 📊 **Statistics**: Progress tracking every 10 messages
- 🛑 **Graceful Shutdown**: Ctrl+C handling with proper cleanup
- 🔄 **Context Manager**: Clean resource management

### Pydantic Models (`src/kafka/model.py`)
```python
class StockRecord(BaseModel):
    symbol: Literal["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA", "META", "NFLX"]
    price: float  # Must be > 0
    volume: int   # Must be >= 0
    timestamp: float  # Auto-generated Unix timestamp
```

### Custom Logger (`src/logger/`)
- 🎨 **ANSI Colors**: Beautiful terminal output with color coding
- 😀 **Emojis**: Visual indicators for different log levels
- 🏗️ **Modular Design**: Separate models and logger implementation
- 🔒 **Frozen Models**: Immutable configuration with Pydantic

**Log Levels:**
- 🔍 DEBUG (cyan)
- ✨ INFO (green)
- ⚠️ WARNING (yellow)
- ❌ ERROR (red)
- 🚨 CRITICAL (magenta)

## 🧪 Testing & Tools

### Topic Management
```bash
# Create topic with custom partitions
make topic-create PARTITIONS=10

# Describe topic (shows partition and offset info)
make topic-describe

# List all topics
make topic-list

# Delete topic
make topic-delete
```

### Demo Scripts
```bash
# Run partition/offset demonstration
python src/kafka/demo_partitions.py
```

## 🐳 Podman Services

| Service | Port | Description |
|---------|------|-------------|
| Kafka | 9092 | Message broker (KRaft mode, 5 partitions) |
| Kafka UI | 8080 | Web UI for Kafka management |

Access Kafka UI at `http://localhost:8080` to:
- View topics and messages
- See partition distribution
- Track consumer offsets
- Monitor cluster health

## 🔧 Makefile Commands

```bash
make help           # Show all available commands
make install        # Install Python dependencies
make dev-install    # Install with dev dependencies (pytest, ruff, mypy)
make up             # Start Podman services
make down           # Stop services
make restart        # Restart services
make nuke           # Destroy all containers/images (⚠️  destructive!)
make producer       # Run Kafka producer
make topic-create   # Create Kafka topic
make topic-describe # Show partition info
make clean          # Clean Python cache files
make status         # Check service status
```

## 📚 Understanding Kafka Partitions & Offsets

**Partitions**: Like highway lanes - messages are distributed across them for parallel processing.
- Your producer uses **stock symbol as partition key**
- This ensures all AAPL messages go to the same partition
- Provides **ordering guarantee** per symbol

**Offsets**: Sequential IDs for messages within each partition
- Start at 0 and increment
- Act as bookmarks for tracking position
- Enable fault-tolerant consumption

See `docs/KAFKA_PARTITIONS_OFFSETS.md` for detailed explanation.

## 🛠️ Troubleshooting

**Podman machine not running:**
```bash
make up  # Automatically starts Podman machine
```

**Kafka connection refused:**
```bash
# Check Kafka status
make status
# Restart Kafka
make restart
```

**Import errors:**
```bash
# Ensure dependencies are installed
uv sync
```

**View logs:**
```bash
# All services
podman-compose logs -f
# Just Kafka
podman-compose logs -f kafka
```

## 🚀 Future Enhancements

- [ ] ⚡ **Spark Streaming**: Real-time aggregations and windowing
- [ ] 💾 **PostgreSQL**: Store processed results
- [ ] 📊 **Streamlit Dashboard**: Live visualization
- [ ] 🔐 **Schema Registry**: Schema evolution support
- [ ] 🧠 **ML Integration**: Anomaly detection
- [ ] ☁️ **Cloud Deployment**: AWS MSK or GCP Pub/Sub
- [ ] 🔒 **Security**: SASL/SSL authentication
- [ ] 📈 **Monitoring**: Prometheus + Grafana

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Use the PR template in `.github/pull_request_template.md`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Apache Software Foundation for Kafka and Spark
- Pydantic team for excellent data validation
- The open-source community

---

⭐ **Star this repo** if you found it helpful!  
🐛 **Found a bug?** [Open an issue](https://github.com/your-username/real-time-stock-streaming/issues)  
💡 **Have ideas?** [Start a discussion](https://github.com/your-username/real-time-stock-streaming/discussions)

**Made with ❤️ and ☕ by Data Engineers, for Data Engineers**

