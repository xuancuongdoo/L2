.PHONY: install build up down test lint format clean

# Install dependencies
install:
	poetry install

# Build Docker image and capture container name
build:
	docker-compose build

# Start Docker containers
up:
	@docker-compose up -d

# Stop Docker containers
down:
	@docker-compose down

# Run tests
test:
	poetry run python3 -m pytest 

# Lint code
lint:
	poetry run flake8

# Format code
format:
	poetry run black .

# Clean up unused Docker resources
clean:
	docker system prune -f
