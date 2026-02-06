# AI News Collector

[![CI](https://github.com/yourusername/ai-news-collector/workflows/CI/badge.svg)](https://github.com/yourusername/ai-news-collector/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)

> Automated AI news collection from Twitter with engagement-based ranking, AI analysis, and daily summaries.

[Features](#features) • [Quick Start](#quick-start) • [Documentation](#documentation) • [Demo](#demo) • [Contributing](#contributing)

---

## 🎯 Overview

AI News Collector automatically monitors Twitter accounts for AI-related content, analyzes tweets using Claude API, ranks them by importance (engagement + AI relevance), and generates beautiful daily summaries with email notifications.

### Key Highlights

- 🤖 **AI-Powered Analysis**: Uses Claude API to identify and summarize AI-related content
- 📊 **Engagement-Based Ranking**: Combines social engagement with AI relevance for importance scoring
- 🎯 **Curated Highlights**: Top 10 tweets get full display with screenshots and translations
- 💰 **Cost Optimized**: 90% cost reduction through selective processing ($20-60/month)
- 📧 **Daily Email Digest**: Beautiful HTML emails with key highlights
- 🌐 **Web Interface**: Browse and search daily summaries
- 🐳 **Docker Ready**: One-command deployment with Docker Compose
- 🔒 **Production Ready**: Complete with tests, CI/CD, and security guidelines

---

## ✨ Features

### Core Features

- **Automated Tweet Collection**: Monitors Twitter accounts every 2 hours
- **AI Content Filtering**: Identifies AI/ML/LLM related tweets
- **Smart Ranking**: Importance score = engagement metrics + AI relevance
- **Two-Tier Display**:
  - 🔥 **Highlights** (Top 10): Full cards with screenshots, summaries, translations
  - 📰 **More News**: Compact cards with summaries and engagement metrics
- **Daily Summaries**: AI-generated overview of key developments
- **Email Notifications**: Daily digest with highlights and link to full summary
- **Web Interface**: Browse summaries with pagination and filtering
- **REST API**: 7 endpoints for programmatic access

### Technical Features

- **Async Processing**: FastAPI with async/await for high performance
- **Scheduled Tasks**: APScheduler for automated collection and aggregation
- **Database Migrations**: Alembic for version-controlled schema changes
- **Screenshot Generation**: Playwright for high-quality tweet screenshots
- **Cloud Storage**: AWS S3 integration for scalable storage
- **Email Service**: Resend integration for reliable delivery
- **Type Safety**: TypeScript frontend, Python type hints
- **Testing**: Unit tests with pytest and fixtures
- **CI/CD**: GitHub Actions for automated testing
- **Docker Support**: Multi-stage builds with health checks

---

## 🚀 Quick Start

### One-Command Setup

```bash
git clone https://github.com/yourusername/ai-news-collector.git
cd ai-news-collector
./setup.sh
```

Edit `backend/.env` with your API keys, then:

```bash
make run
```

Visit:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Docker Setup

```bash
cp .env.example .env
# Edit .env with your API keys
docker-compose up -d
```

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions.

---

## 📚 Documentation

- **[README.md](README.md)** - Main documentation (you are here)
- **[QUICKSTART.md](QUICKSTART.md)** - Step-by-step setup guide
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide
- **[API.md](API.md)** - Complete API reference
- **[FAQ.md](FAQ.md)** - Frequently asked questions
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[SECURITY.md](SECURITY.md)** - Security policy
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

---

## 🎬 Demo

### Web Interface

![Home Page](docs/images/home.png)
*Browse daily summaries with pagination*

![Summary Detail](docs/images/summary.png)
*View curated highlights and more news*

### Email Digest

![Email](docs/images/email.png)
*Daily email with key highlights*

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Twitter API (twitterapi.io)          │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              Backend (FastAPI + PostgreSQL)             │
│  • Tweet Collection (every 2 hours)                     │
│  • AI Analysis (Claude API)                             │
│  • Engagement Scoring                                   │
│  • Screenshot Generation (Playwright)                   │
│  • Daily Aggregation (8 AM)                             │
│  • Email Notifications (Resend)                         │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│           Frontend (Next.js 14 + TypeScript)            │
│  • Summary List (paginated)                             │
│  • Summary Detail (highlights + more news)              │
│  • Responsive Design (Tailwind CSS)                     │
└─────────────────────────────────────────────────────────┘
```

---

## 💻 Tech Stack

### Backend
- **FastAPI** - Modern async Python web framework
- **PostgreSQL** - Reliable relational database
- **SQLAlchemy** - Powerful ORM
- **Alembic** - Database migrations
- **APScheduler** - Scheduled tasks
- **Anthropic Claude API** - AI analysis
- **Playwright** - Screenshot generation
- **AWS S3** - Cloud storage
- **Resend** - Email service

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Axios** - HTTP client

### DevOps
- **Docker** - Containerization
- **GitHub Actions** - CI/CD
- **Railway** - Backend hosting
- **Vercel** - Frontend hosting

---

## 📊 Cost Breakdown

**Estimated Monthly Cost: $20-60**

| Service | Cost | Notes |
|---------|------|-------|
| Claude API | $8-25 | AI analysis and summarization |
| Twitter API | $0-20 | twitterapi.io pricing |
| Railway | $5-20 | Backend + PostgreSQL |
| Vercel | $0 | Free tier sufficient |
| AWS S3 | $1-3 | ~300 screenshots/month |
| Resend | $0-10 | Free tier: 3000 emails/month |

**Cost Optimization:**
- Screenshots: Only top 10 tweets (90% reduction)
- Translation: Only top 10 tweets (90% reduction)
- Batch processing: Multiple tweets per API call
- Selective processing: Focus on high-value content

---

## 🎯 Use Cases

- **AI Researchers**: Stay updated on latest developments
- **Tech Companies**: Monitor AI trends and competitors
- **Journalists**: Track AI news for reporting
- **Investors**: Follow AI industry developments
- **Educators**: Curate AI content for students
- **Enthusiasts**: Keep up with AI advancements

---

## 🔧 Configuration

### Environment Variables

Key configuration options:

```bash
# Required
TWITTER_API_KEY=your_key
ANTHROPIC_API_KEY=your_key

# Optional
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
RESEND_API_KEY=your_key

# Ranking Weights
ENGAGEMENT_WEIGHT_LIKES=1.0
ENGAGEMENT_WEIGHT_RETWEETS=2.0
ENGAGEMENT_WEIGHT_REPLIES=1.5
ENGAGEMENT_WEIGHT_BOOKMARKS=2.5
AI_RELEVANCE_WEIGHT=3.0

# Display
TOP_TWEETS_COUNT=10

# Features
ENABLE_SCREENSHOT=True
ENABLE_TRANSLATION=True
ENABLE_EMAIL=True
```

See [backend/.env.example](backend/.env.example) for all options.

---

## 📈 Roadmap

### v1.1 (Planned)
- [ ] User authentication
- [ ] Custom monitored accounts per user
- [ ] Advanced filtering and search
- [ ] Analytics dashboard

### v1.2 (Planned)
- [ ] Mobile app
- [ ] Real-time notifications
- [ ] Sentiment analysis
- [ ] Topic clustering

### v2.0 (Future)
- [ ] Multi-platform support (Reddit, HN, etc.)
- [ ] Custom AI models
- [ ] Team collaboration features
- [ ] API rate limiting and authentication

See [CHANGELOG.md](CHANGELOG.md) for details.

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`make test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## 🐛 Bug Reports

Found a bug? Please open an issue with:
- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details

---

## 💡 Feature Requests

Have an idea? Open an issue with the `feature request` label!

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Anthropic** - Claude API for AI analysis
- **twitterapi.io** - Twitter API access
- **FastAPI** - Excellent Python web framework
- **Next.js** - Amazing React framework
- **Vercel** - Frontend hosting
- **Railway** - Backend hosting

---

## 📞 Support

- **Documentation**: Check the docs folder
- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-news-collector/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-news-collector/discussions)
- **Email**: support@yourdomain.com

---

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

---

## 📸 Screenshots

### Home Page
Browse daily summaries with key statistics and topics.

### Summary Detail
View curated highlights with full tweet cards including screenshots, AI summaries, and translations.

### Email Digest
Receive daily emails with key highlights and a link to the full summary.

---

## 🔗 Links

- **Live Demo**: https://ai-news-demo.vercel.app (coming soon)
- **Documentation**: https://docs.ai-news-collector.com (coming soon)
- **Blog**: https://blog.ai-news-collector.com (coming soon)

---

## 📊 Stats

- **Lines of Code**: ~7,300
- **Files**: 60+
- **Tests**: 15+ unit tests
- **API Endpoints**: 7
- **Database Models**: 4
- **Services**: 5
- **Components**: 3

---

## 🎓 Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

<div align="center">

**Built with ❤️ using FastAPI, Next.js, and Claude API**

[⬆ Back to Top](#ai-news-collector)

</div>
