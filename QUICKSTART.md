# Quick Start Guide

This guide will help you get the AI News Collection Tool up and running quickly.

## Prerequisites Checklist

- [ ] Python 3.9 or higher installed
- [ ] Node.js 18 or higher installed
- [ ] PostgreSQL 14 or higher installed and running
- [ ] Git installed

## API Keys Required

You'll need to obtain the following API keys:

1. **Twitter API** (twitterapi.io)
   - Sign up at https://twitterapi.io
   - Get your API key from the dashboard

2. **Anthropic Claude API**
   - Sign up at https://console.anthropic.com
   - Create an API key

3. **Resend** (for emails, optional)
   - Sign up at https://resend.com
   - Get your API key

4. **AWS S3** (for screenshots, optional)
   - Create an S3 bucket
   - Get access key and secret key

## Step-by-Step Setup

### 1. Clone and Navigate to Project

```bash
cd /Users/pingxn7/Desktop/x
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Create .env file from example
cp .env.example .env
```

### 3. Configure Backend Environment

Edit `backend/.env` with your API keys:

```bash
# Required
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/ai_news
TWITTER_API_KEY=your_twitterapi_io_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional (but recommended)
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_S3_BUCKET=your-bucket-name
RESEND_API_KEY=your_resend_key
EMAIL_TO=your-email@example.com
```

### 4. Set Up Database

```bash
# Create database
createdb ai_news

# Or using psql
psql -U postgres
CREATE DATABASE ai_news;
\q

# Run migrations
alembic upgrade head

# Seed monitored accounts
python scripts/seed_accounts.py
```

### 5. Test Backend

```bash
# Start the server
uvicorn app.main:app --reload

# In another terminal, test the API
curl http://localhost:8000/api/health
```

You should see a health check response. Visit http://localhost:8000/docs for API documentation.

### 6. Frontend Setup

```bash
# Open new terminal
cd /Users/pingxn7/Desktop/x/frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.local.example .env.local

# Edit .env.local (should work with defaults)
# NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 7. Start Frontend

```bash
npm run dev
```

Visit http://localhost:3000 to see the frontend.

## Testing the System

### Manual Tweet Collection

```bash
# In backend directory with venv activated
python -c "
import asyncio
from app.database import get_db_context
from app.services.twitter_collector import twitter_collector

async def test():
    with get_db_context() as db:
        stats = await twitter_collector.collect_all_tweets(db)
        print(f'Collected {stats[\"total_tweets\"]} tweets')

asyncio.run(test())
"
```

### Manual AI Analysis

```bash
python -c "
import asyncio
from app.database import get_db_context
from app.services.ai_analyzer import ai_analyzer

async def test():
    with get_db_context() as db:
        count = await ai_analyzer.process_unprocessed_tweets(db)
        print(f'Processed {count} tweets')

asyncio.run(test())
"
```

### Create Test Summary

```bash
python -c "
import asyncio
from datetime import date
from app.database import get_db_context
from app.services.aggregator import aggregator_service

async def test():
    with get_db_context() as db:
        summary = await aggregator_service.create_daily_summary(db, date.today())
        if summary:
            print(f'Created summary {summary.id} with {summary.tweet_count} tweets')
        else:
            print('No AI tweets found to create summary')

asyncio.run(test())
"
```

## Scheduled Tasks

The system automatically runs:
- **Tweet collection**: Every 2 hours (configurable)
- **Daily summary**: Every day at 8 AM UTC (configurable)

To change the schedule, edit `SCHEDULE_TWEET_COLLECTION_CRON` and `SCHEDULE_DAILY_SUMMARY_CRON` in `.env`.

## Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
pg_isready

# Check connection
psql -U your_user -d ai_news -c "SELECT 1;"
```

### Python Import Errors

```bash
# Make sure virtual environment is activated
which python  # Should show path to venv

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend Build Errors

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### API Connection Issues

Check that:
1. Backend is running on port 8000
2. Frontend `.env.local` has correct `NEXT_PUBLIC_API_URL`
3. CORS is configured correctly in backend `.env`

## Next Steps

1. **Add more Twitter accounts**: Edit `scripts/seed_accounts.py` and run it again
2. **Customize ranking weights**: Adjust engagement weights in `.env`
3. **Configure email templates**: Edit `app/services/email_service.py`
4. **Deploy to production**: See deployment section in main README

## Getting Help

- Check logs in terminal where backend is running
- Visit API docs at http://localhost:8000/docs
- Check metrics at http://localhost:8000/api/metrics
- Review main README.md for detailed documentation

## Production Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` to a secure random value
- [ ] Set `DEBUG=False`
- [ ] Configure production database URL
- [ ] Set up proper CORS origins
- [ ] Configure S3 for screenshot storage
- [ ] Set up email service (Resend)
- [ ] Test all scheduled tasks
- [ ] Set up monitoring and alerts
- [ ] Configure backup strategy for database
- [ ] Review and adjust rate limits
- [ ] Set up SSL/HTTPS
