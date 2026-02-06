# Makefile for AI News Collector

.PHONY: help install setup test run clean deploy

help:
	@echo "AI News Collector - Makefile Commands"
	@echo ""
	@echo "Setup Commands:"
	@echo "  make install          Install all dependencies (backend + frontend)"
	@echo "  make setup            Complete setup (install + database + seed)"
	@echo ""
	@echo "Development Commands:"
	@echo "  make run              Run both backend and frontend"
	@echo "  make run-backend      Run backend only"
	@echo "  make run-frontend     Run frontend only"
	@echo "  make test             Run all tests"
	@echo "  make test-backend     Run backend tests"
	@echo "  make lint             Run linters"
	@echo ""
	@echo "Database Commands:"
	@echo "  make db-create        Create database"
	@echo "  make db-migrate       Run database migrations"
	@echo "  make db-seed          Seed monitored accounts"
	@echo "  make db-reset         Reset database (drop + create + migrate + seed)"
	@echo ""
	@echo "Utility Commands:"
	@echo "  make collect          Manually collect tweets"
	@echo "  make summary          Manually create daily summary"
	@echo "  make status           Check system status"
	@echo "  make clean            Clean temporary files"
	@echo ""
	@echo "Deployment Commands:"
	@echo "  make deploy-backend   Deploy backend to Railway"
	@echo "  make deploy-frontend  Deploy frontend to Vercel"

# Setup Commands
install:
	@echo "Installing backend dependencies..."
	cd backend && python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt && playwright install chromium
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "Installation complete!"

setup: install
	@echo "Setting up environment files..."
	cd backend && cp .env.example .env || true
	cd frontend && cp .env.local.example .env.local || true
	@echo "Creating database..."
	createdb ai_news || echo "Database may already exist"
	@echo "Running migrations..."
	cd backend && . venv/bin/activate && alembic upgrade head
	@echo "Seeding accounts..."
	cd backend && . venv/bin/activate && python scripts/seed_accounts.py
	@echo "Setup complete! Edit .env files with your API keys."

# Development Commands
run:
	@echo "Starting backend and frontend..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@echo "API Docs: http://localhost:8000/docs"
	@make -j2 run-backend run-frontend

run-backend:
	cd backend && . venv/bin/activate && uvicorn app.main:app --reload

run-frontend:
	cd frontend && npm run dev

test:
	@make test-backend
	@echo "All tests passed!"

test-backend:
	cd backend && . venv/bin/activate && pytest

lint:
	@echo "Linting backend..."
	cd backend && . venv/bin/activate && flake8 app/ || true
	@echo "Linting frontend..."
	cd frontend && npm run lint || true

# Database Commands
db-create:
	createdb ai_news

db-migrate:
	cd backend && . venv/bin/activate && alembic upgrade head

db-seed:
	cd backend && . venv/bin/activate && python scripts/seed_accounts.py

db-reset:
	@echo "Resetting database..."
	dropdb ai_news || true
	createdb ai_news
	cd backend && . venv/bin/activate && alembic upgrade head
	cd backend && . venv/bin/activate && python scripts/seed_accounts.py
	@echo "Database reset complete!"

# Utility Commands
collect:
	cd backend && . venv/bin/activate && python scripts/manual_collect.py

summary:
	cd backend && . venv/bin/activate && python scripts/manual_summary.py

status:
	cd backend && . venv/bin/activate && python scripts/check_status.py

clean:
	@echo "Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	cd frontend && rm -rf .next 2>/dev/null || true
	@echo "Clean complete!"

# Deployment Commands
deploy-backend:
	@echo "Deploying backend to Railway..."
	cd backend && railway up

deploy-frontend:
	@echo "Deploying frontend to Vercel..."
	cd frontend && vercel --prod

# Docker Commands
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Development helpers
dev-backend:
	cd backend && . venv/bin/activate && python -m app.main

dev-frontend:
	cd frontend && npm run dev

# Check environment
check-env:
	@echo "Checking environment..."
	@command -v python3 >/dev/null 2>&1 || { echo "Python 3 is not installed"; exit 1; }
	@command -v node >/dev/null 2>&1 || { echo "Node.js is not installed"; exit 1; }
	@command -v psql >/dev/null 2>&1 || { echo "PostgreSQL is not installed"; exit 1; }
	@echo "Environment check passed!"

# Generate migration
migration:
	@read -p "Enter migration message: " msg; \
	cd backend && . venv/bin/activate && alembic revision --autogenerate -m "$$msg"

# Show logs
logs-backend:
	cd backend && tail -f logs/*.log 2>/dev/null || echo "No logs found"

# Quick start
quickstart: setup
	@echo ""
	@echo "Quick start complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Edit backend/.env with your API keys"
	@echo "2. Edit frontend/.env.local if needed"
	@echo "3. Run 'make run' to start the application"
	@echo ""
	@echo "Useful commands:"
	@echo "  make status   - Check system status"
	@echo "  make collect  - Manually collect tweets"
	@echo "  make summary  - Create daily summary"
	@echo ""
