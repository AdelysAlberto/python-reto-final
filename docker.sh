#!/bin/bash

case "$1" in
    "up")
        echo "Starting all services..."
        docker-compose up --build
        ;;
    "down")
        echo "Stopping all services..."
        docker-compose down
        ;;
    "db")
        echo "Starting only database..."
        docker-compose up db
        ;;
    "logs")
        docker-compose logs -f
        ;;
    "clean")
        echo "Cleaning up containers and volumes..."
        docker-compose down -v
        docker system prune -f
        ;;
    "test")
        echo "Running tests with coverage..."
        docker exec -it reto_final_python-web-1 python -m pytest --cov=app --cov-report=html --cov-report=term-missing tests/ -v
        ;;
    "test-simple")
        echo "Running tests without coverage..."
        docker exec -it reto_final_python-web-1 python -m pytest tests/ -v
        ;;
    "test-file")
        if [ -z "$2" ]; then
            echo "Usage: $0 test-file <test_file>"
            echo "Example: $0 test-file test_models.py"
            exit 1
        fi
        echo "Running specific test file: $2"
        docker exec -it reto_final_python-web-1 python -m pytest tests/$2 -v
        ;;
    *)
        echo "Usage: $0 {up|down|db|logs|clean|test|test-simple|test-file}"
        echo "  up         - Start all services (with build)"
        echo "  down       - Stop all services"
        echo "  db         - Start only database"
        echo "  logs       - Show logs"
        echo "  clean      - Clean containers and volumes"
        echo "  test       - Run tests with coverage"
        echo "  test-simple - Run tests without coverage"
        echo "  test-file  - Run specific test file (e.g., test-file test_models.py)"
        ;;
esac