#!/bin/bash

# AI News Collector - Quick Setup Script
# This script automates the initial setup process

set -e  # Exit on error

echo "=================================="
echo "AI News Collector - Quick Setup"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo "Checking prerequisites..."

command -v python3 >/dev/null 2>&1 || { echo -e "${RED}Error: Python 3 is not installed${NC}"; exit 1; }
command -v node >/dev/null 2>&1 || { echo -e "${RED}Error: Node.js is not installed${NC}"; exit 1; }
command -v psql >/dev/null 2>&1 || { echo -e "${RED}Error: PostgreSQL is not installed${NC}"; exit 1; }

echo -e "${GREEN}✓ All prerequisites found${NC}"
echo ""

# Backend setup
echo "Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt

# Install Playwright
echo "Installing Playwright browsers..."
playwright install chromium

# Create .env file
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo -e "${YELLOW}⚠ Please edit backend/.env with your API keys${NC}"
fi

cd ..

# Frontend setup
echo ""
echo "Setting up frontend..."
cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

# Create .env.local file
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file..."
    cp .env.local.example .env.local
fi

cd ..

# Database setup
echo ""
echo "Setting up database..."

# Check if database exists
if psql -lqt | cut -d \| -f 1 | grep -qw ai_news; then
    echo -e "${YELLOW}Database 'ai_news' already exists${NC}"
else
    echo "Creating database..."
    createdb ai_news
    echo -e "${GREEN}✓ Database created${NC}"
fi

# Run migrations
echo "Running database migrations..."
cd backend
source venv/bin/activate
alembic upgrade head
echo -e "${GREEN}✓ Migrations complete${NC}"

# Seed accounts
echo "Seeding monitored accounts..."
python scripts/seed_accounts.py
echo -e "${GREEN}✓ Accounts seeded${NC}"

cd ..

# Summary
echo ""
echo "=================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Edit backend/.env with your API keys:"
echo "   - TWITTER_API_KEY"
echo "   - ANTHROPIC_API_KEY"
echo "   - AWS credentials (optional)"
echo "   - RESEND_API_KEY (optional)"
echo ""
echo "2. Start the application:"
echo "   make run"
echo "   OR"
echo "   Terminal 1: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "   Terminal 2: cd frontend && npm run dev"
echo ""
echo "3. Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Useful commands:"
echo "   make status   - Check system status"
echo "   make collect  - Manually collect tweets"
echo "   make summary  - Create daily summary"
echo "   make help     - Show all available commands"
echo ""
