# AI News Collection Tool

An automated system that monitors Twitter/X accounts for AI-related content, analyzes tweets using Claude API, generates daily summaries, and sends email notifications.

## Features

- 🤖 **Automated Tweet Collection**: Monitors Twitter accounts every 2 hours
- 🧠 **AI Analysis**: Uses Claude API to identify AI-related content and generate summaries
- 📊 **Engagement-Based Ranking**: Ranks tweets by importance (engagement + AI relevance)
- 🎯 **Curated Highlights**: Top 10 tweets get full display with screenshots and translations
- 📧 **Daily Email Digest**: Automated email summaries sent daily
- 🌐 **Web Interface**: Browse and view daily summaries
- 💰 **Cost Optimized**: Selective screenshot generation and translation (90% cost reduction)

## Architecture

```
Twitter API → Backend (FastAPI) → Claude API → Database (PostgreSQL)
                ↓
        Scheduled Tasks (APScheduler)
                ↓
        Frontend (Next.js) + Email (Resend)
```

## Tech Stack

### Backend
- **FastAPI**: Modern async Python web framework
- **PostgreSQL**: Database with JSONB support
- **SQLAlchemy + Alembic**: ORM and migrations
- **APScheduler**: Scheduled tasks
- **Anthropic Claude API**: AI analysis and summarization
- **Playwright**: Screenshot generation
- **AWS S3**: Screenshot storage
- **Resend**: Email service

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Axios**: HTTP client

## Project Structure

```
/Users/pingxn7/Desktop/x/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI entry point
│   │   ├── config.py                  # Configuration
│   │   ├── database.py                # Database setup
│   │   ├── models/                    # SQLAlchemy models
│   │   ├── schemas/                   # Pydantic schemas
│   │   ├── services/                  # Business logic
│   │   │   ├── twitter_collector.py
│   │   │   ├── ai_analyzer.py
│   │   │   ├── screenshot_service.py
│   │   │   ├── aggregator.py
│   │   │   └── email_service.py
│   │   ├── api/routes/                # API endpoints
│   │   └── tasks/                     # Scheduled tasks
│   ├── alembic/                       # Database migrations
│   ├── scripts/                       # Utility scripts
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/
    ├── app/                           # Next.js pages
    │   ├── page.tsx                   # Home (summary list)
    │   └── summary/[id]/page.tsx      # Summary detail
    ├── components/                    # React components
    │   ├── TweetCard.tsx
    │   ├── SummaryView.tsx
    │   └── HighlightsSummary.tsx
    ├── lib/
    │   └── api.ts                     # API client
    └── package.json
```

## Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 14+
- Twitter API key (twitterapi.io)
- Anthropic API key
- AWS S3 bucket (optional, for screenshots)
- Resend API key (optional, for emails)

### Backend Setup

1. **Create virtual environment**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
playwright install chromium
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

4. **Set up database**
```bash
# Create PostgreSQL database
createdb ai_news

# Run migrations
alembic upgrade head
```

5. **Seed monitored accounts**
```bash
python scripts/seed_accounts.py
```

6. **Run the server**
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Install dependencies**
```bash
cd frontend
npm install
```

2. **Configure environment**
```bash
cp .env.local.example .env.local
# Edit .env.local with your API URL
```

3. **Run development server**
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Configuration

### Backend Environment Variables

Key configuration options in `.env`:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ai_news

# APIs
TWITTER_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
RESEND_API_KEY=your-key

# AWS S3 (optional)
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_S3_BUCKET=your-bucket

# Scheduling
SCHEDULE_TWEET_COLLECTION_CRON=0 */2 * * *  # Every 2 hours
SCHEDULE_DAILY_SUMMARY_CRON=0 8 * * *       # Daily at 8 AM

# Feature Flags
ENABLE_TRANSLATION=True
ENABLE_SCREENSHOT=True
ENABLE_EMAIL=True

# Ranking Configuration
TOP_TWEETS_COUNT=10
ENGAGEMENT_WEIGHT_LIKES=1.0
ENGAGEMENT_WEIGHT_RETWEETS=2.0
ENGAGEMENT_WEIGHT_REPLIES=1.5
ENGAGEMENT_WEIGHT_BOOKMARKS=2.5
AI_RELEVANCE_WEIGHT=3.0
```

## Usage

### Manual Operations

**Collect tweets manually:**
```bash
# In Python shell
from app.database import get_db_context
from app.services.twitter_collector import twitter_collector

with get_db_context() as db:
    stats = await twitter_collector.collect_all_tweets(db)
    print(stats)
```

**Process tweets with AI:**
```bash
from app.services.ai_analyzer import ai_analyzer

with get_db_context() as db:
    count = await ai_analyzer.process_unprocessed_tweets(db)
    print(f"Processed {count} tweets")
```

**Create daily summary:**
```bash
from app.services.aggregator import aggregator_service
from datetime import date

with get_db_context() as db:
    summary = await aggregator_service.create_daily_summary(db, date.today())
    print(f"Created summary: {summary.id}")
```

### API Endpoints

- `GET /api/health` - Health check
- `GET /api/metrics` - System metrics
- `GET /api/summaries` - List summaries (paginated)
- `GET /api/summaries/{id}` - Get summary detail
- `GET /api/summaries/slug/{slug}` - Get summary by URL slug
- `GET /api/tweets` - List processed tweets

## Key Features Explained

### Engagement-Based Ranking

Tweets are ranked by an **importance score** that combines:
- **Engagement metrics**: likes, retweets, replies, bookmarks
- **AI relevance**: How central AI/ML is to the content (0-10)

Formula:
```python
engagement_score = (
    likes * 1.0 +
    retweets * 2.0 +
    replies * 1.5 +
    bookmarks * 2.5
)

importance_score = (
    normalized_engagement * 0.7 +
    ai_relevance * 0.3
)
```

### Two-Tier Display

1. **精选 (Highlights)** - Top 10 tweets:
   - Full tweet card with screenshot
   - AI-generated summary
   - Chinese translation
   - All engagement metrics
   - Link to original

2. **更多AI资讯 (More News)** - Remaining tweets:
   - Compact card format
   - Summary only (no screenshot, no translation)
   - Engagement metrics
   - Link to original

### Cost Optimization

- **Screenshots**: Only generated for top 10 tweets (90% reduction)
- **Translation**: Only for top 10 tweets (90% reduction)
- **Batch processing**: Multiple tweets analyzed in single API call
- **Selective processing**: Focus resources on high-value content

**Estimated monthly cost**: $20-60 (vs $80-150 without optimization)

## Deployment

### Backend (Railway)

```bash
railway login
railway init
railway add --database postgresql
railway variables set TWITTER_API_KEY=xxx ANTHROPIC_API_KEY=xxx ...
railway up
```

### Frontend (Vercel)

```bash
vercel login
vercel
vercel env add NEXT_PUBLIC_API_URL production
vercel --prod
```

## Monitoring

- **Health check**: `GET /api/health`
- **Metrics**: `GET /api/metrics`
- **Logs**: Structured logging with Loguru
- **Scheduler status**: Included in metrics endpoint

## Troubleshooting

**Tweets not being collected:**
- Check Twitter API credentials
- Verify monitored accounts are active
- Check scheduler status in `/api/metrics`

**AI analysis failing:**
- Verify Anthropic API key
- Check API rate limits
- Review logs for errors

**Screenshots not generating:**
- Ensure Playwright is installed: `playwright install chromium`
- Check S3 credentials if using cloud storage
- Verify `ENABLE_SCREENSHOT=True`

**Email not sending:**
- Verify Resend API key
- Check `ENABLE_EMAIL=True`
- Confirm email addresses are valid

## Development

**Run tests:**
```bash
cd backend
pytest
```

**Create new migration:**
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

**Add new monitored account:**
```python
from app.models.monitored_account import MonitoredAccount
from app.database import SessionLocal

db = SessionLocal()
account = MonitoredAccount(
    user_id="twitter_user_id",
    username="username",
    display_name="Display Name",
    is_active=True
)
db.add(account)
db.commit()
```

## License

MIT

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

## Support

For issues and questions, please open a GitHub issue.
