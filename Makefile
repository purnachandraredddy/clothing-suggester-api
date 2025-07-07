# Clothing Recommendation System - Makefile
# Use 'make help' to see all available commands

.PHONY: help install train run-api run-web run-all test clean docker-build docker-run docker-stop docker-logs docker-clean

# Default target
help:
	@echo "👕 Clothing Recommendation System"
	@echo "=================================="
	@echo ""
	@echo "Available commands:"
	@echo "  install      - Install Python dependencies"
	@echo "  train        - Train the machine learning model"
	@echo "  run-api      - Start the Flask API server"
	@echo "  run-web      - Start the web interface"
	@echo "  run-all      - Start both API and web interface"
	@echo "  test         - Run all tests"
	@echo "  clean        - Clean up generated files"
	@echo ""
	@echo "Docker commands:"
	@echo "  docker-build - Build Docker images"
	@echo "  docker-run   - Run containers using docker-compose"
	@echo "  docker-stop  - Stop and remove containers"
	@echo "  docker-logs  - View container logs"
	@echo "  docker-clean - Clean up Docker resources"
	@echo ""

# Development commands
install:
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt

train:
	@echo "🤖 Training the machine learning model..."
	python train_model.py

run-api:
	@echo "🚀 Starting API server..."
	python app.py

run-web:
	@echo "🌐 Starting web interface..."
	python web_interface.py

run-all:
	@echo "🚀 Starting both API and web interface..."
	@echo "Starting API in background..."
	@python app.py &
	@sleep 3
	@echo "Starting web interface..."
	@python web_interface.py

test:
	@echo "🧪 Running tests..."
	python -m pytest tests/ -v
	python test_api.py
	python test_web_interface.py

clean:
	@echo "🧹 Cleaning up..."
	rm -rf __pycache__/
	rm -rf *.pyc
	rm -rf .pytest_cache/
	rm -rf data/*.pkl
	rm -rf data/*.joblib
	rm -rf logs/*.log

# Docker commands
docker-build:
	@echo "🐳 Building Docker images..."
	docker-compose -f docker/docker-compose.yml build

docker-run:
	@echo "🐳 Running Docker containers..."
	@echo "This will start both API and web interface in containers"
	@echo "API will be available at http://localhost:5001"
	@echo "Web interface will be available at http://localhost:5002"
	docker-compose -f docker/docker-compose.yml up -d

docker-stop:
	@echo "🛑 Stopping Docker containers..."
	docker-compose -f docker/docker-compose.yml down

docker-logs:
	@echo "📋 Viewing Docker container logs..."
	docker-compose -f docker/docker-compose.yml logs -f

docker-clean:
	@echo "🧹 Cleaning up Docker resources..."
	docker-compose -f docker/docker-compose.yml down -v
	docker system prune -f

# Quick start with Docker
docker-quick:
	@echo "🚀 Quick start with Docker..."
	@echo "Building and running containers..."
	./run_docker.sh 