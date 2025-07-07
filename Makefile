# Clothing Recommendation System Makefile

.PHONY: help install train test run clean docker-build docker-run docker-test web

# Default target
help:
	@echo "👕 Clothing Recommendation System"
	@echo "================================"
	@echo ""
	@echo "Available commands:"
	@echo "  install      - Install dependencies"
	@echo "  train        - Train the machine learning model"
	@echo "  test         - Run tests"
	@echo "  run          - Start the Flask API server"
	@echo "  web          - Start the web interface"
	@echo "  test-api     - Test the API endpoints"
	@echo "  clean        - Clean up generated files"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run with Docker Compose"
	@echo "  docker-test  - Test with Docker"
	@echo "  format       - Format code with black"
	@echo "  lint         - Lint code with flake8"
	@echo "  all          - Install, train, test, and run"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

# Train the model
train:
	@echo "🤖 Training the model..."
	python train_model.py

# Run tests
test:
	@echo "🧪 Running tests..."
	python -m pytest tests/ -v

# Start the API server
run:
	@echo "🚀 Starting Flask API server..."
	python app.py

# Start the web interface
web:
	@echo "🌐 Starting Web Interface..."
	python web_interface.py

# Test the API
test-api:
	@echo "🔍 Testing API endpoints..."
	python test_api.py

# Clean up generated files
clean:
	@echo "🧹 Cleaning up..."
	rm -f model.joblib
	rm -rf data/
	rm -rf logs/
	rm -rf __pycache__/
	rm -rf tests/__pycache__/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Build Docker image
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -f docker/Dockerfile -t clothing-recommender .

# Run with Docker Compose
docker-run:
	@echo "🐳 Running with Docker Compose..."
	docker-compose -f docker/docker-compose.yml up --build

# Test with Docker
docker-test:
	@echo "🐳 Testing with Docker..."
	docker-compose -f docker/docker-compose.yml up test-client

# Format code
format:
	@echo "🎨 Formatting code..."
	black . --line-length=88

# Lint code
lint:
	@echo "🔍 Linting code..."
	flake8 . --max-line-length=88 --ignore=E203,W503

# Complete setup and run
all: install train test run

# Development setup
dev-setup: install train
	@echo "✅ Development environment ready!"
	@echo "Run 'make run' to start the API server"
	@echo "Run 'make web' to start the web interface"
	@echo "Run 'make test-api' to test the API"

# Production setup
prod-setup: install train
	@echo "✅ Production environment ready!"
	@echo "Run 'make docker-run' to start with Docker" 