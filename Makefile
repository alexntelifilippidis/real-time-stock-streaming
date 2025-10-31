.PHONY: help install dev-install clean up down restart logs producer consumer spark test format lint check all

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m # No Color

help: ## Show this help message
	@echo '$(BLUE)Real-Time Stock Streaming Pipeline$(NC)'
	@echo '$(YELLOW)Usage: make [target]$(NC)\n'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Install Python dependencies with uv
	@echo "$(BLUE)Installing dependencies...$(NC)"
	uv sync

dev-install: ## Install with dev dependencies
	@echo "$(BLUE)Installing dev dependencies...$(NC)"
	uv sync --extra dev

clean: ## Clean up Python cache files and checkpoints
	@echo "$(YELLOW)Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf checkpoints/ spark-warehouse/ metastore_db/ derby.log
	@echo "$(GREEN)Cleanup complete!$(NC)"

up: ## Start all services (Kafka, Zookeeper, PostgreSQL)
	@echo "$(BLUE)Starting services...$(NC)"
	podman-compose up -d
	@echo "$(GREEN)Services started! Waiting for healthy status...$(NC)"
	@sleep 5
	@podman-compose ps

down: ## Stop all services
	@echo "$(YELLOW)Stopping services...$(NC)"
	podman-compose down
	@echo "$(GREEN)Services stopped!$(NC)"

restart: down up ## Restart all services

logs: ## View logs from all services
	podman-compose logs -f

logs-kafka: ## View Kafka logs
	podman-compose logs -f kafka

logs-postgres: ## View PostgreSQL logs
	podman-compose logs -f postgres

status: ## Check status of all services
	@podman-compose ps

producer: ## Run the Kafka producer
	@echo "$(BLUE)Starting Kafka producer...$(NC)"
	python src/kafka/producer.py

consumer: ## Run the test consumer
	@echo "$(BLUE)Starting test consumer...$(NC)"
	python src/kafka/consumer_test.py

spark: ## Run Spark streaming job
	@echo "$(BLUE)Starting Spark streaming...$(NC)"
	spark-submit \
		--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 \
		src/spark/spark_streaming.py

test: ## Run tests
	@echo "$(BLUE)Running tests...$(NC)"
	pytest tests/ -v

format: ## Format code with ruff
	@echo "$(BLUE)Formatting code...$(NC)"
	ruff format src/

lint: ## Lint code with ruff
	@echo "$(BLUE)Linting code...$(NC)"
	ruff check src/

check: ## Type check with mypy
	@echo "$(BLUE)Type checking with mypy...$(NC)"
	mypy src/

qa: format lint check ## Run all quality checks (format, lint, type check)
	@echo "$(GREEN)All quality checks passed!$(NC)"

init-db: ## Initialize PostgreSQL database
	@echo "$(BLUE)Initializing database...$(NC)"
	podman-compose exec postgres psql -U postgres -d stocks -c "CREATE TABLE IF NOT EXISTS stock_aggregations (id SERIAL PRIMARY KEY, symbol VARCHAR(10), window_start TIMESTAMP, window_end TIMESTAMP, avg_price DECIMAL, min_price DECIMAL, max_price DECIMAL, total_volume BIGINT, num_trades INTEGER, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
	@echo "$(GREEN)Database initialized!$(NC)"

all: clean install up ## Clean, install dependencies, and start services
	@echo "$(GREEN)Setup complete! You can now run:$(NC)"
	@echo "  $(YELLOW)make producer$(NC)  - Start the producer"
	@echo "  $(YELLOW)make spark$(NC)     - Start Spark streaming"
	@echo "  $(YELLOW)make consumer$(NC)  - Test the consumer"

quickstart: all ## Complete setup and start producer + spark (in background)
	@echo "$(GREEN)Starting producer and Spark in background...$(NC)"
	@echo "Use 'make logs' to view output"

dev: dev-install up ## Setup for development
	@echo "$(GREEN)Development environment ready!$(NC)"
