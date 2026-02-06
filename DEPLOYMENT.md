# Deployment Guide

This guide covers deploying the AI News Collection Tool to production.

## Deployment Architecture

```
Frontend (Vercel) ←→ Backend (Railway) ←→ PostgreSQL (Railway)
                           ↓
                    AWS S3 (Screenshots)
                           ↓
                    Resend (Email)
```

## Option 1: Railway (Recommended for Backend)

Railway provides easy deployment with integrated PostgreSQL.

### Backend Deployment to Railway

1. **Install Railway CLI**
```bash
npm install -g @railway/cli
```

2. **Login to Railway**
```bash
railway login
```

3. **Initialize Project**
```bash
cd backend
railway init
```

4. **Add PostgreSQL Database**
```bash
railway add --database postgresql
```

5. **Set Environment Variables**
```bash
# Set all required environment variables
railway variables set TWITTER_API_KEY=your_key
railway variables set ANTHROPIC_API_KEY=your_key
railway variables set AWS_ACCESS_KEY_ID=your_key
railway variables set AWS_SECRET_ACCESS_KEY=your_secret
railway variables set AWS_S3_BUCKET=your_bucket
railway variables set RESEND_API_KEY=your_key
railway variables set EMAIL_FROM=noreply@yourdomain.com
railway variables set EMAIL_TO=your-email@example.com
railway variables set FRONTEND_URL=https://your-frontend.vercel.app
railway variables set CORS_ORIGINS=https://your-frontend.vercel.app

# Feature flags
railway variables set ENABLE_TRANSLATION=True
railway variables set ENABLE_SCREENSHOT=True
railway variables set ENABLE_EMAIL=True

# Ranking configuration
railway variables set TOP_TWEETS_COUNT=10
railway variables set ENGAGEMENT_WEIGHT_LIKES=1.0
railway variables set ENGAGEMENT_WEIGHT_RETWEETS=2.0
railway variables set ENGAGEMENT_WEIGHT_REPLIES=1.5
railway variables set ENGAGEMENT_WEIGHT_BOOKMARKS=2.5
railway variables set AI_RELEVANCE_WEIGHT=3.0
```

6. **Create Procfile**
```bash
cat > Procfile << EOF
web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT
EOF
```

7. **Create railway.json**
```bash
cat > railway.json << EOF
{
  "\$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port \$PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF
```

8. **Deploy**
```bash
railway up
```

9. **Get Database URL**
```bash
railway variables get DATABASE_URL
```

10. **Run Migrations**
```bash
# Connect to Railway shell
railway run alembic upgrade head

# Seed accounts
railway run python scripts/seed_accounts.py
```

11. **Get Deployment URL**
```bash
railway domain
```

Your backend will be available at the provided Railway URL.

## Option 2: Vercel (Frontend)

### Frontend Deployment to Vercel

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Login to Vercel**
```bash
vercel login
```

3. **Deploy from Frontend Directory**
```bash
cd frontend
vercel
```

4. **Set Environment Variables**
```bash
# Set production environment variable
vercel env add NEXT_PUBLIC_API_URL production
# Enter your Railway backend URL: https://your-backend.railway.app

vercel env add NEXT_PUBLIC_API_TIMEOUT production
# Enter: 10000

vercel env add NEXT_PUBLIC_APP_NAME production
# Enter: AI News Collector

vercel env add NEXT_PUBLIC_ENV production
# Enter: production
```

5. **Deploy to Production**
```bash
vercel --prod
```

Your frontend will be available at the provided Vercel URL.

## Option 3: Docker Deployment

### Backend Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright
RUN playwright install chromium
RUN playwright install-deps chromium

# Copy application
COPY . .

# Run migrations and start server
CMD alembic upgrade head && \
    python scripts/seed_accounts.py && \
    uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

### Frontend Dockerfile

Create `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:18-alpine AS runner

WORKDIR /app

ENV NODE_ENV production

COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000

CMD ["node", "server.js"]
```

### Docker Compose

Create `docker-compose.yml` in project root:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: ai_news
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/ai_news
      TWITTER_API_KEY: ${TWITTER_API_KEY}
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
      AWS_ACCESS_KEY_ID: ${AWS_ACCESS_KEY_ID}
      AWS_SECRET_ACCESS_KEY: ${AWS_SECRET_ACCESS_KEY}
      AWS_S3_BUCKET: ${AWS_S3_BUCKET}
      RESEND_API_KEY: ${RESEND_API_KEY}
      EMAIL_FROM: ${EMAIL_FROM}
      EMAIL_TO: ${EMAIL_TO}
      FRONTEND_URL: http://localhost:3000
      CORS_ORIGINS: http://localhost:3000
    depends_on:
      - postgres

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    depends_on:
      - backend

volumes:
  postgres_data:
```

Run with:
```bash
docker-compose up -d
```

## AWS S3 Setup

1. **Create S3 Bucket**
```bash
aws s3 mb s3://ai-news-screenshots --region us-east-1
```

2. **Set Bucket Policy**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::ai-news-screenshots/*"
    }
  ]
}
```

3. **Enable CORS**
```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["GET", "HEAD"],
    "AllowedOrigins": ["*"],
    "ExposeHeaders": []
  }
]
```

4. **Create IAM User**
- Create user with programmatic access
- Attach policy: `AmazonS3FullAccess` (or create custom policy)
- Save access key and secret key

## Resend Email Setup

1. **Sign up at https://resend.com**

2. **Verify Domain** (optional but recommended)
- Add DNS records to verify your domain
- Use verified domain in `EMAIL_FROM`

3. **Get API Key**
- Create API key in dashboard
- Add to environment variables

## Post-Deployment Checklist

### Backend
- [ ] Database migrations completed
- [ ] Monitored accounts seeded
- [ ] Health check endpoint responding: `/api/health`
- [ ] Metrics endpoint working: `/api/metrics`
- [ ] Scheduler running (check metrics)
- [ ] Test tweet collection manually
- [ ] Test AI analysis manually
- [ ] Test summary creation manually
- [ ] Test email sending

### Frontend
- [ ] Home page loads
- [ ] Can view summary list
- [ ] Can view summary details
- [ ] Images loading from S3
- [ ] API calls working
- [ ] No console errors

### Integration
- [ ] Frontend can reach backend API
- [ ] CORS configured correctly
- [ ] Screenshots uploading to S3
- [ ] Emails sending successfully
- [ ] Scheduled tasks running

## Monitoring Setup

### Health Checks

Set up monitoring for:
- `GET /api/health` - Should return 200
- `GET /api/metrics` - Check scheduler status

### Logging

Backend logs are output to stdout. Configure log aggregation:

**Railway**: Logs available in dashboard

**Docker**: Use logging driver
```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Alerts

Set up alerts for:
- API downtime
- Database connection failures
- Scheduler stopped
- High error rates
- Failed tweet collections
- Failed email sends

## Scaling Considerations

### Database
- Enable connection pooling (already configured)
- Add read replicas for high traffic
- Regular backups (Railway does this automatically)

### Backend
- Railway auto-scales based on traffic
- For manual scaling, increase instance count
- Consider Redis for caching if needed

### Storage
- S3 automatically scales
- Set lifecycle policies to delete old screenshots:
  - Transition to Glacier after 90 days
  - Delete after 1 year

### Rate Limits

Monitor API usage:
- Twitter API: Check rate limits
- Claude API: Monitor token usage
- Resend: Check email quota

## Cost Optimization

### Current Estimated Costs (Monthly)

- **Railway**: $5-20 (Hobby plan)
- **Vercel**: $0 (Free tier sufficient)
- **Claude API**: $8-25 (with optimization)
- **Twitter API**: $0-20 (twitterapi.io pricing)
- **S3**: $1-3 (with lifecycle policies)
- **Resend**: $0-10 (Free tier: 3000 emails/month)

**Total**: $20-60/month

### Optimization Tips

1. **Reduce screenshot generation**
   - Only top 10 tweets (already implemented)
   - Lower image quality if needed
   - Use WebP format

2. **Reduce translation costs**
   - Only top 10 tweets (already implemented)
   - Cache translations

3. **Optimize Claude API usage**
   - Batch process tweets
   - Use smaller model for simple tasks
   - Cache analysis results

4. **Database optimization**
   - Regular VACUUM
   - Add indexes for common queries
   - Archive old data

## Backup Strategy

### Database Backups

**Railway**: Automatic daily backups

**Manual backup**:
```bash
pg_dump -h your-host -U your-user -d ai_news > backup.sql
```

**Restore**:
```bash
psql -h your-host -U your-user -d ai_news < backup.sql
```

### S3 Backups

Enable versioning on S3 bucket:
```bash
aws s3api put-bucket-versioning \
  --bucket ai-news-screenshots \
  --versioning-configuration Status=Enabled
```

## Security Best Practices

1. **Environment Variables**
   - Never commit `.env` files
   - Use secrets management in production
   - Rotate API keys regularly

2. **Database**
   - Use strong passwords
   - Enable SSL connections
   - Restrict network access

3. **API Security**
   - Enable rate limiting
   - Add API authentication if needed
   - Keep dependencies updated

4. **CORS**
   - Only allow specific origins
   - Don't use wildcard in production

## Troubleshooting Production Issues

### Backend Not Starting
```bash
# Check logs
railway logs

# Check environment variables
railway variables

# Test database connection
railway run python -c "from app.database import engine; engine.connect()"
```

### Scheduler Not Running
```bash
# Check metrics endpoint
curl https://your-backend.railway.app/api/metrics

# Check logs for scheduler errors
railway logs --filter "scheduler"
```

### High Memory Usage
- Reduce batch size in `.env`
- Optimize database queries
- Add connection pooling limits

### Slow API Responses
- Add database indexes
- Enable caching
- Optimize Claude API calls

## Rollback Procedure

### Backend Rollback
```bash
# Railway
railway rollback

# Docker
docker-compose down
docker-compose up -d --build
```

### Database Rollback
```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade <revision>
```

### Frontend Rollback
```bash
# Vercel
vercel rollback
```

## Support and Maintenance

### Regular Maintenance Tasks

**Weekly**:
- Check error logs
- Monitor API usage
- Review cost metrics

**Monthly**:
- Update dependencies
- Review and optimize queries
- Clean up old data
- Check backup integrity

**Quarterly**:
- Security audit
- Performance review
- Cost optimization review
- Update documentation

### Getting Help

- Railway: https://railway.app/help
- Vercel: https://vercel.com/support
- Anthropic: https://support.anthropic.com
- AWS: https://aws.amazon.com/support
