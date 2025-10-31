# 📈 Real-Time Stock Streaming Pipeline

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-3.0%2B-black.svg)](https://kafka.apache.org/)
[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.3%2B-orange.svg)](https://spark.apache.org/)
[![Docker](https://img.shields.io/badge/Podman-4.0%2B-892CA0.svg)](https://www.podman.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-ready, real-time data streaming pipeline that demonstrates end-to-end data engineering using **Apache Kafka** and **Apache Spark Structured Streaming**. This project simulates live stock market data, processes it in real-time, and provides actionable analytics.

## 🎯 Key Features

- ⚡ **Real-time Processing**: Sub-second latency streaming with Kafka and Spark
- 📊 **Scalable Architecture**: Horizontally scalable components using Podman
- 🔄 **Fault Tolerance**: Automatic recovery and checkpointing
- 📈 **Live Analytics**: Real-time aggregations and windowing operations
- 🐳 **Easy Deployment**: Full Podman Compose setup for local development
- 📝 **Production Ready**: Logging, monitoring, and error handling included

## 🏗️ Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  Data Generator │ ───▶ │  Apache Kafka   │ ───▶ │  Spark Stream   │
│  (Python)       │      │  (Topic: stock) │      │  (PySpark)      │
└─────────────────┘      └─────────────────┘      └─────────────────┘
                                                            │
                                                            ▼
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   Dashboard     │ ◀─── │   PostgreSQL    │ ◀─── │  Aggregations   │
│ (Streamlit)     │      │   (Storage)     │      │  (Processing)   │
└─────────────────┘      └─────────────────┘      └─────────────────┘
```

**Data Flow:**
1. 🎲 **Producer** generates realistic stock price data (AAPL, GOOGL, MSFT, AMZN, etc.)
2. 📨 **Kafka** ingests and buffers messages in the `stock_prices` topic
3. ⚡ **Spark Structured Streaming** consumes and processes data with windowed aggregations
4. 💾 **PostgreSQL** stores processed results for persistence
5. 📊 **Streamlit Dashboard** visualizes real-time trends and analytics

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| 🔄 **Streaming** | Apache Kafka | High-throughput message broker |
| ⚡ **Processing** | Apache Spark (Structured Streaming) | Real-time stream processing |
| 🗃️ **Storage** | PostgreSQL | Relational database for analytics |
| 🐍 **Language** | Python 3.8+ | Main implementation language |
| 📦 **Libraries** | PySpark, kafka-python, pandas | Data processing |
| 📊 **Visualization** | Streamlit | Interactive dashboards |
| 🐳 **Infrastructure** | Docker & Podman Compose | Containerization |
| 🔍 **Monitoring** | Prometheus + Grafana (planned) | Metrics and observability |

## 📁 Project Structure

```
real-time-stock-streaming/
│
├── README.md                      # This file
├── LICENSE                        # MIT License
├── .gitignore                     # Git ignore rules
├── podman-compose.yml             # Container services configuration
├── pyproject.toml               # Python dependencies
│
├── kafka/                         # Kafka producer/consumer
│   ├── producer.py               # Stock data generator
│   ├── consumer_test.py          # Test consumer for validation
│   └── config.py                 # Kafka configuration
│
├── spark/                         # Spark streaming jobs
│   ├── spark_streaming.py        # Main streaming application
│   ├── aggregations.py           # Aggregation logic
│   └── utils/
│       ├── schema.py             # Data schemas
│       └── helpers.py            # Utility functions
│
├── database/                      # Database scripts
│   ├── init.sql                  # PostgreSQL initialization
│   └── queries.sql               # Sample queries
│
├── dashboard/                     # Streamlit dashboard
│   ├── app.py                    # Main dashboard app
│   └── components/               # UI components
│
├── data/                          # Sample and test data
│   └── sample_stock_data.json    # Example data
│
├── notebooks/                     # Jupyter notebooks
│   └── exploration.ipynb         # Data exploration
│
└── tests/                         # Unit tests
    ├── test_producer.py
    └── test_streaming.py
```

## 🚀 Quick Start

### Prerequisites

- **Podman** 4.0+ and **Podman Compose** 2.0+
- **Python** 3.8 or higher
- **Git** for cloning the repository
- At least 4GB RAM available for containers

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/real-time-stock-streaming.git
   cd real-time-stock-streaming
   ```

2. **Start the infrastructure** (Kafka, Zookeeper, PostgreSQL)
   ```bash
   podman-compose up -d
   ```
   
   Wait for services to be healthy (~30 seconds):
   ```bash
   podman-compose ps
   ```

3. **Create Python virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # venv\Scripts\activate   # On Windows
   ```

4. **Install dependencies**
   ```bash
   uv sync
   ```

5. **Initialize the database**
   ```bash
   podman-compose exec postgres psql -U postgres -d stocks -f /docker-entrypoint-initdb.d/init.sql
   ```

### Running the Pipeline

**Terminal 1 - Start Kafka Producer:**
```bash
python kafka/producer.py
```

**Terminal 2 - Start Spark Streaming:**
```bash
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 \
  spark/spark_streaming.py
```

**Terminal 3 - Launch Dashboard:**
```bash
streamlit run dashboard/app.py
```

Visit `http://localhost:8501` to see real-time analytics! 📊

## 📊 Features in Detail

### Stock Data Generator
- Simulates realistic stock prices with random walks
- Configurable symbols, frequency, and volatility
- Timestamps with microsecond precision
- Volume and market cap metadata

### Stream Processing
- **Windowed Aggregations**: 1-minute, 5-minute, 15-minute windows
- **Stateful Operations**: Running averages, min/max tracking
- **Watermarking**: Handles late-arriving data
- **Checkpointing**: Fault-tolerant state management

### Analytics
- Real-time price trends
- Volume-weighted average price (VWAP)
- Price change percentages
- Moving averages (SMA, EMA)

## 🧪 Testing

Run unit tests:
```bash
pytest tests/
```

Test Kafka producer independently:
```bash
python kafka/consumer_test.py
```

## 🐳 Docker Services

| Service | Port | Description |
|---------|------|-------------|
| Zookeeper | 2181 | Kafka coordination |
| Kafka | 9092 | Message broker |
| PostgreSQL | 5432 | Database (user: `postgres`, db: `stocks`) |
| Adminer | 8080 | Database UI |

Access Adminer at `http://localhost:8080` for database management.

## 🔧 Configuration

Key configuration files:

- `kafka/config.py` - Kafka broker settings, topics
- `spark/config.py` - Spark session config, checkpoints
- `podman-compose.yml` - Infrastructure setup
- `.env` - Environment variables (create from `.env.example`)

## 📈 Monitoring & Observability

**Logs:**
```bash
# Kafka logs
podman-compose logs -f kafka

# View all services
podman-compose logs -f
```

**Metrics** (coming soon):
- Kafka message throughput
- Spark processing latency
- Consumer lag monitoring

## 🛠️ Troubleshooting

**Kafka connection refused:**
```bash
# Ensure Kafka is running
podman-compose ps kafka
# Restart if needed
podman-compose restart kafka
```

**Spark can't find packages:**
```bash
# Include Kafka package explicitly
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 spark/spark_streaming.py
```

**Database connection errors:**
```bash
# Check PostgreSQL status
podman-compose exec postgres pg_isready
```

## 🚀 Future Enhancements

- [ ] 🔐 **Schema Registry**: Integrate Confluent Schema Registry for schema evolution
- [ ] 🧠 **ML Integration**: Anomaly detection with streaming ML models
- [ ] ☁️ **Cloud Deployment**: AWS (MSK + EMR) or GCP (Pub/Sub + Dataflow)
- [ ] 📊 **Advanced Dashboards**: Grafana with Prometheus metrics
- [ ] 🔒 **Security**: SASL/SSL authentication for Kafka
- [ ] 📦 **Kubernetes**: Helm charts for K8s deployment
- [ ] 🧪 **Integration Tests**: End-to-end pipeline testing
- [ ] 📝 **Data Catalog**: Metadata management with Apache Atlas
- [ ] 🌊 **CDC Integration**: Change data capture from transactional databases

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 🙏 Acknowledgments

- Apache Software Foundation for Kafka and Spark
- The open-source community for excellent documentation
- Stock market APIs for inspiration

---

⭐ **Star this repo** if you found it helpful!  
🐛 **Found a bug?** [Open an issue](https://github.com/your-username/real-time-stock-streaming/issues)  
💡 **Have ideas?** [Start a discussion](https://github.com/your-username/real-time-stock-streaming/discussions)

