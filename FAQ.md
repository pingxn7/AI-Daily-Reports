# Frequently Asked Questions (FAQ)

## General Questions

### What is AI News Collector?

AI News Collector is an automated system that monitors Twitter accounts for AI-related content, analyzes tweets using Claude API, ranks them by importance, and generates daily summaries with email notifications.

### Who is this for?

- AI researchers and practitioners who want to stay updated
- Tech companies monitoring AI developments
- Journalists covering AI news
- Anyone interested in tracking AI trends

### How much does it cost to run?

Estimated monthly cost: **$20-60**
- Claude API: $8-25
- Twitter API: $0-20
- Railway (backend): $5-20
- Vercel (frontend): $0 (free tier)
- S3 (storage): $1-3
- Resend (email): $0-10

### Is it open source?

Yes! Licensed under MIT. You can use, modify, and distribute it freely.

---

## Setup Questions

### What are the prerequisites?

- Python 3.9+
- Node.js 18+
- PostgreSQL 14+
- Git

### How do I get started quickly?

```bash
./setup.sh
# Edit backend/.env with your API keys
make run
```

See QUICKSTART.md for detailed instructions.

### Do I need all the API keys?

**Required:**
- Twitter API key (twitterapi.io)
- Anthropic API key

**Optional:**
- AWS S3 (for screenshots, can disable)
- Resend (for emails, can disable)

### Can I run it without Docker?

Yes! Use the native setup:
```bash
./setup.sh
make run
```

### Can I run it with Docker?

Yes! Use Docker Compose:
```bash
docker-compose up -d
```

---

## Configuration Questions

### How do I add more Twitter accounts to monitor?

Edit `backend/scripts/seed_accounts.py` and add accounts to the list, then run:
```bash
cd backend
source venv/bin/activate
python scripts/seed_accounts.py
```

### How do I change the collection schedule?

Edit `backend/.env`:
```bash
SCHEDULE_TWEET_COLLECTION_CRON=0 */2 * * *  # Every 2 hours
SCHEDULE_DAILY_SUMMARY_CRON=0 8 * * *       # Daily at 8 AM
```

### How do I adjust the ranking weights?

Edit `backend/.env`:
```bash
ENGAGEMENT_WEIGHT_LIKES=1.0
ENGAGEMENT_WEIGHT_RETWEETS=2.0
ENGAGEMENT_WEIGHT_REPLIES=1.5
ENGAGEMENT_WEIGHT_BOOKMARKS=2.5
AI_RELEVANCE_WEIGHT=3.0
```

### How do I change the number of curated highlights?

Edit `backend/.env`:
```bash
TOP_TWEETS_COUNT=10  # Change to desired number
```

### Can I disable screenshots or translations?

Yes, edit `backend/.env`:
```bash
ENABLE_SCREENSHOT=False
ENABLE_TRANSLATION=False
ENABLE_EMAIL=False
```

---

## Usage Questions

### How do I manually collect tweets?

```bash
make collect
# OR
cd backend && source venv/bin/activate && python scripts/manual_collect.py
```

### How do I manually create a summary?

```bash
make summary
# OR
cd backend && source venv/bin/activate && python scripts/manual_summary.py
```

### How do I check system status?

```bash
make status
# OR
cd backend && source venv/bin/activate && python scripts/check_status.py
```

### Where can I view the API documentation?

Visit http://localhost:8000/docs when the backend is running.

### How do I access the web interface?

Visit http://localhost:3000 when the frontend is running.

---

## Troubleshooting

### Backend won't start

**Check:**
1. Virtual environment is activated
2. All dependencies are installed: `pip install -r requirements.txt`
3. Database is running: `pg_isready`
4. Environment variables are set in `.env`
5. Database migrations are up to date: `alembic upgrade head`

**Common errors:**
- `ModuleNotFoundError`: Run `pip install -r requirements.txt`
- `Connection refused`: Check database is running
- `No module named 'app'`: Make sure you're in the backend directory

### Frontend won't start

**Check:**
1. Dependencies are installed: `npm install`
2. `.env.local` file exists
3. Backend is running on port 8000

**Common errors:**
- `Module not found`: Run `npm install`
- `EADDRINUSE`: Port 3000 is already in use
- `API connection failed`: Check backend is running

### Database connection errors

**Check:**
1. PostgreSQL is running: `pg_isready`
2. Database exists: `psql -l | grep ai_news`
3. Credentials in `.env` are correct
4. Database URL format: `postgresql://user:password@host:port/dbname`

**Fix:**
```bash
# Recreate database
dropdb ai_news
createdb ai_news
cd backend && source venv/bin/activate && alembic upgrade head
```

### Tweets not being collected

**Check:**
1. Twitter API key is valid
2. Monitored accounts are seeded: `python scripts/seed_accounts.py`
3. Scheduler is running: Check `/api/metrics`
4. Check logs for errors

**Test manually:**
```bash
make collect
```

### AI analysis not working

**Check:**
1. Anthropic API key is valid
2. API key has sufficient credits
3. Check logs for rate limit errors

**Test manually:**
```bash
cd backend && source venv/bin/activate
python -c "
import asyncio
from app.database import get_db_context
from app.services.ai_analyzer import ai_analyzer
asyncio.run(ai_analyzer.process_unprocessed_tweets(get_db_context().__enter__()))
"
```

### Screenshots not generating

**Check:**
1. Playwright is installed: `playwright install chromium`
2. S3 credentials are correct (if using S3)
3. `ENABLE_SCREENSHOT=True` in `.env`

**Test manually:**
```bash
cd backend && source venv/bin/activate
python -c "
import asyncio
from app.services.screenshot_service import screenshot_service
asyncio.run(screenshot_service.init_browser())
"
```

### Email not sending

**Check:**
1. Resend API key is valid
2. `ENABLE_EMAIL=True` in `.env`
3. Email addresses are correct
4. Check Resend dashboard for delivery status

---

## Performance Questions

### How many tweets can it handle?

The system can handle:
- 100+ monitored accounts
- 1000+ tweets per day
- 10,000+ tweets in database

Performance depends on:
- Database size
- Server resources
- API rate limits

### How can I improve performance?

1. **Database optimization:**
   - Add indexes for common queries
   - Regular VACUUM
   - Connection pooling

2. **API optimization:**
   - Increase batch size
   - Cache API responses
   - Use Redis for caching

3. **Resource optimization:**
   - Increase server memory
   - Use faster database
   - Enable CDN for frontend

### What are the rate limits?

**Twitter API (twitterapi.io):**
- Check their documentation for limits
- Default: Collect every 2 hours

**Claude API:**
- Depends on your plan
- Batch processing reduces API calls

**Resend:**
- Free tier: 3000 emails/month
- Paid plans available

---

## Deployment Questions

### Where should I deploy?

**Recommended:**
- Backend: Railway (easy PostgreSQL integration)
- Frontend: Vercel (optimized for Next.js)
- Database: Railway PostgreSQL
- Storage: AWS S3

**Alternatives:**
- Heroku, Render, DigitalOcean, AWS, GCP, Azure
- Docker on any VPS

### How do I deploy to production?

See DEPLOYMENT.md for detailed instructions.

**Quick start:**
```bash
# Backend (Railway)
cd backend && railway up

# Frontend (Vercel)
cd frontend && vercel --prod
```

### Do I need a custom domain?

No, but recommended for production:
- Railway provides a subdomain
- Vercel provides a subdomain
- You can add custom domains to both

### How do I set up SSL/HTTPS?

Railway and Vercel provide SSL automatically. For custom deployments, use:
- Let's Encrypt (free)
- Cloudflare (free)
- AWS Certificate Manager

---

## Customization Questions

### Can I customize the email template?

Yes! Edit `backend/app/services/email_service.py` in the `format_email_body` method.

### Can I change the frontend design?

Yes! The frontend uses Tailwind CSS. Edit components in `frontend/components/` and pages in `frontend/app/`.

### Can I add more data sources besides Twitter?

Yes! Create a new service similar to `twitter_collector.py` for other platforms.

### Can I customize the AI analysis prompts?

Yes! Edit prompts in `backend/app/services/ai_analyzer.py`.

### Can I add user authentication?

Not currently implemented, but you can add:
- NextAuth.js for frontend
- FastAPI authentication middleware for backend
- See CONTRIBUTING.md for guidance

---

## Data Questions

### Where is data stored?

- **Tweets**: PostgreSQL database
- **Screenshots**: AWS S3 (or local filesystem)
- **Logs**: Local filesystem

### How long is data retained?

Default: Forever

To implement retention:
1. Add cleanup script
2. Set S3 lifecycle policies
3. Archive old summaries

### Can I export data?

Yes! Use the API or database directly:
```bash
# Export via API
curl http://localhost:8000/api/tweets > tweets.json

# Export from database
pg_dump ai_news > backup.sql
```

### Can I import existing data?

Yes! Use the database directly or create a custom import script.

---

## API Questions

### Is there an API?

Yes! REST API with 7 endpoints. See API.md for documentation.

### Do I need authentication?

Currently no. For production, consider adding API key authentication.

### What's the API rate limit?

No rate limiting by default. Add middleware for production.

### Can I use the API from other applications?

Yes! The API is designed to be consumed by any client.

---

## Contributing Questions

### How can I contribute?

See CONTRIBUTING.md for guidelines. We welcome:
- Bug fixes
- New features
- Documentation improvements
- Tests
- Performance optimizations

### How do I report bugs?

Create a GitHub issue with:
- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details

### How do I suggest features?

Create a GitHub issue with the `feature request` label.

---

## Support Questions

### Where can I get help?

1. Check this FAQ
2. Read the documentation (README, QUICKSTART, etc.)
3. Search GitHub issues
4. Create a new GitHub issue
5. Check API docs at `/docs`

### Is there a community?

- GitHub Discussions (coming soon)
- GitHub Issues for bug reports
- Pull requests welcome!

### Can I hire someone to set this up?

Yes! This is open source, so you can hire any developer familiar with Python and Next.js.

---

## License Questions

### What license is this under?

MIT License - very permissive. You can:
- Use commercially
- Modify
- Distribute
- Sublicense

### Can I use this for my company?

Yes! MIT license allows commercial use.

### Do I need to credit the original authors?

Not required, but appreciated! The MIT license only requires including the license text.

---

## Future Plans

### What features are planned?

See CHANGELOG.md for planned features:
- User authentication
- Multiple users
- Advanced filtering
- Analytics dashboard
- Mobile app
- Real-time notifications
- And more!

### Can I request features?

Yes! Create a GitHub issue with the `feature request` label.

### How often is this updated?

Check the GitHub repository for the latest updates and releases.

---

## Still Have Questions?

- **Documentation**: Check README.md, QUICKSTART.md, DEPLOYMENT.md, API.md
- **GitHub Issues**: Search existing issues or create a new one
- **Email**: Contact the maintainers (see README.md)

---

**Last Updated**: 2024-02-06
**Version**: 1.0.0
