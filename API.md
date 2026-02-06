# API Documentation

Complete API reference for the AI News Collection Tool backend.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://your-backend.railway.app`

## Authentication

Currently, the API does not require authentication. For production use, consider adding API key authentication.

## Endpoints

### Health & Monitoring

#### GET /api/health

Health check endpoint to verify system status.

**Response**
```json
{
  "status": "healthy",
  "database": "healthy",
  "scheduler": "running",
  "timestamp": "2024-02-06T10:30:00Z"
}
```

**Status Codes**
- `200 OK`: System is healthy
- `503 Service Unavailable`: System is degraded

---

#### GET /api/metrics

Get system metrics and statistics.

**Response**
```json
{
  "total_summaries": 45,
  "total_tweets": 1250,
  "ai_related_tweets": 890,
  "ai_related_percentage": 71.2,
  "latest_summary_date": "2024-02-06",
  "scheduler": {
    "running": true,
    "jobs": [
      {
        "id": "collect_tweets",
        "name": "Collect tweets from monitored accounts",
        "next_run": "2024-02-06T12:00:00Z",
        "trigger": "cron[hour='*/2']"
      },
      {
        "id": "daily_summary",
        "name": "Create daily summary and send email",
        "next_run": "2024-02-07T08:00:00Z",
        "trigger": "cron[hour='8']"
      }
    ]
  }
}
```

---

### Summaries

#### GET /api/summaries

List all daily summaries with pagination.

**Query Parameters**
- `page` (integer, default: 1): Page number
- `page_size` (integer, default: 10, max: 100): Items per page

**Response**
```json
{
  "items": [
    {
      "id": 1,
      "date": "2024-02-06T00:00:00Z",
      "url_slug": "2024-02-06-ai-news",
      "tweet_count": 87,
      "top_tweets_count": 10,
      "other_tweets_count": 77,
      "topics": ["GPT", "OpenAI", "LLM", "Research"],
      "highlights_summary": "今日AI领域关键进展包括...",
      "created_at": "2024-02-06T08:00:00Z",
      "email_sent_at": "2024-02-06T08:05:00Z"
    }
  ],
  "total": 45,
  "page": 1,
  "page_size": 10,
  "total_pages": 5
}
```

**Example**
```bash
curl "http://localhost:8000/api/summaries?page=1&page_size=10"
```

---

#### GET /api/summaries/{id}

Get detailed summary by ID with all tweets.

**Path Parameters**
- `id` (integer): Summary ID

**Response**
```json
{
  "id": 1,
  "date": "2024-02-06T00:00:00Z",
  "url_slug": "2024-02-06-ai-news",
  "tweet_count": 87,
  "top_tweets_count": 10,
  "other_tweets_count": 77,
  "topics": ["GPT", "OpenAI", "LLM"],
  "highlights_summary": "今日AI领域关键进展包括...",
  "summary_text": "Daily AI news summary for 2024-02-06",
  "created_at": "2024-02-06T08:00:00Z",
  "email_sent_at": "2024-02-06T08:05:00Z",
  "highlights": [
    {
      "id": 123,
      "tweet_id": 456,
      "is_ai_related": true,
      "summary": "OpenAI announces GPT-5 with significant improvements...",
      "translation": "OpenAI 宣布 GPT-5，带来重大改进...",
      "topics": ["GPT", "OpenAI"],
      "screenshot_url": "https://s3.amazonaws.com/...",
      "screenshot_generated_at": "2024-02-06T08:10:00Z",
      "importance_score": 9.2,
      "processed_at": "2024-02-06T07:30:00Z",
      "tweet": {
        "id": 456,
        "tweet_id": "1234567890",
        "text": "Announcing GPT-5...",
        "created_at": "2024-02-06T10:30:00Z",
        "tweet_url": "https://twitter.com/openai/status/1234567890",
        "like_count": 5420,
        "retweet_count": 1230,
        "reply_count": 456,
        "bookmark_count": 890,
        "engagement_score": 8950.0,
        "user_id": 1,
        "collected_at": "2024-02-06T11:00:00Z",
        "processed": true
      }
    }
  ],
  "other_news": [
    {
      "id": 154,
      "tweet_id": 789,
      "is_ai_related": true,
      "summary": "New research paper on transformer architectures...",
      "translation": null,
      "topics": ["Research", "Transformers"],
      "screenshot_url": null,
      "screenshot_generated_at": null,
      "importance_score": 5.1,
      "processed_at": "2024-02-06T07:35:00Z",
      "tweet": {
        "id": 789,
        "tweet_id": "9876543210",
        "text": "New paper explores...",
        "created_at": "2024-02-06T14:20:00Z",
        "tweet_url": "https://twitter.com/researcher/status/9876543210",
        "like_count": 45,
        "retweet_count": 12,
        "reply_count": 3,
        "bookmark_count": 8,
        "engagement_score": 125.5,
        "user_id": 2,
        "collected_at": "2024-02-06T15:00:00Z",
        "processed": true
      }
    }
  ]
}
```

**Status Codes**
- `200 OK`: Summary found
- `404 Not Found`: Summary does not exist

**Example**
```bash
curl "http://localhost:8000/api/summaries/1"
```

---

#### GET /api/summaries/slug/{url_slug}

Get detailed summary by URL slug.

**Path Parameters**
- `url_slug` (string): URL-friendly slug (e.g., "2024-02-06-ai-news")

**Response**

Same as GET /api/summaries/{id}

**Status Codes**
- `200 OK`: Summary found
- `404 Not Found`: Summary does not exist

**Example**
```bash
curl "http://localhost:8000/api/summaries/slug/2024-02-06-ai-news"
```

---

### Tweets

#### GET /api/tweets

List processed tweets with optional filtering.

**Query Parameters**
- `ai_related` (boolean, optional): Filter by AI-related status
- `limit` (integer, default: 50, max: 200): Number of tweets to return
- `offset` (integer, default: 0): Number of tweets to skip

**Response**
```json
[
  {
    "id": 123,
    "tweet_id": 456,
    "is_ai_related": true,
    "summary": "OpenAI announces GPT-5...",
    "translation": "OpenAI 宣布 GPT-5...",
    "topics": ["GPT", "OpenAI"],
    "screenshot_url": "https://s3.amazonaws.com/...",
    "screenshot_generated_at": "2024-02-06T08:10:00Z",
    "importance_score": 9.2,
    "processed_at": "2024-02-06T07:30:00Z",
    "tweet": {
      "id": 456,
      "tweet_id": "1234567890",
      "text": "Announcing GPT-5...",
      "created_at": "2024-02-06T10:30:00Z",
      "tweet_url": "https://twitter.com/openai/status/1234567890",
      "like_count": 5420,
      "retweet_count": 1230,
      "reply_count": 456,
      "bookmark_count": 890,
      "engagement_score": 8950.0,
      "user_id": 1,
      "collected_at": "2024-02-06T11:00:00Z",
      "processed": true
    }
  }
]
```

**Examples**
```bash
# Get all AI-related tweets
curl "http://localhost:8000/api/tweets?ai_related=true&limit=50"

# Get all tweets (including non-AI)
curl "http://localhost:8000/api/tweets?limit=100"

# Pagination
curl "http://localhost:8000/api/tweets?limit=50&offset=50"
```

---

## Data Models

### Tweet

Raw tweet collected from Twitter.

```typescript
{
  id: number;
  tweet_id: string;           // Twitter tweet ID
  text: string;               // Tweet text
  created_at: string;         // ISO 8601 datetime
  tweet_url: string;          // Full Twitter URL
  like_count: number;
  retweet_count: number;
  reply_count: number;
  bookmark_count: number;
  engagement_score: number;   // Calculated engagement score
  user_id: number;            // Foreign key to monitored_accounts
  collected_at: string;       // ISO 8601 datetime
  processed: boolean;         // Whether AI analysis is complete
}
```

### ProcessedTweet

Tweet analyzed by AI with importance scoring.

```typescript
{
  id: number;
  tweet_id: number;           // Foreign key to tweets
  is_ai_related: boolean;
  summary: string | null;     // AI-generated summary
  translation: string | null; // Chinese translation (top 10 only)
  topics: string[] | null;    // Array of topic tags
  screenshot_url: string | null;
  screenshot_generated_at: string | null;
  importance_score: number;   // 0-10 combined score
  processed_at: string;       // ISO 8601 datetime
  tweet: Tweet;               // Nested tweet object
}
```

### DailySummary

Daily aggregation of AI news.

```typescript
{
  id: number;
  date: string;               // ISO 8601 datetime
  url_slug: string;           // URL-friendly slug
  tweet_count: number;        // Total AI-related tweets
  top_tweets_count: number;   // Number in highlights (usually 10)
  other_tweets_count: number; // Number in summary section
  topics: string[] | null;    // Array of topics covered
  highlights_summary: string | null; // AI-generated overview
  summary_text: string | null;
  created_at: string;         // ISO 8601 datetime
  email_sent_at: string | null;
  highlights: ProcessedTweet[];      // Top 10 curated tweets
  other_news: ProcessedTweet[];      // Remaining tweets
}
```

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Invalid parameter value"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

### 503 Service Unavailable
```json
{
  "detail": "Service temporarily unavailable"
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider adding rate limiting middleware.

Recommended limits:
- 100 requests per minute per IP
- 1000 requests per hour per IP

---

## CORS

CORS is configured to allow requests from the frontend URL specified in `CORS_ORIGINS` environment variable.

Default development: `http://localhost:3000`

---

## Webhooks (Future)

Future versions may include webhook support for:
- New summary created
- Tweet collection completed
- Email sent

---

## SDK Examples

### Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Get health status
response = requests.get(f"{BASE_URL}/api/health")
print(response.json())

# List summaries
response = requests.get(f"{BASE_URL}/api/summaries", params={"page": 1, "page_size": 10})
summaries = response.json()

# Get summary detail
summary_id = summaries["items"][0]["id"]
response = requests.get(f"{BASE_URL}/api/summaries/{summary_id}")
detail = response.json()

# Get AI-related tweets
response = requests.get(f"{BASE_URL}/api/tweets", params={"ai_related": True, "limit": 50})
tweets = response.json()
```

### JavaScript/TypeScript

```typescript
const BASE_URL = "http://localhost:8000";

// Get health status
const health = await fetch(`${BASE_URL}/api/health`).then(r => r.json());

// List summaries
const summaries = await fetch(`${BASE_URL}/api/summaries?page=1&page_size=10`)
  .then(r => r.json());

// Get summary detail
const summaryId = summaries.items[0].id;
const detail = await fetch(`${BASE_URL}/api/summaries/${summaryId}`)
  .then(r => r.json());

// Get AI-related tweets
const tweets = await fetch(`${BASE_URL}/api/tweets?ai_related=true&limit=50`)
  .then(r => r.json());
```

### cURL

```bash
# Health check
curl -X GET "http://localhost:8000/api/health"

# List summaries
curl -X GET "http://localhost:8000/api/summaries?page=1&page_size=10"

# Get summary by ID
curl -X GET "http://localhost:8000/api/summaries/1"

# Get summary by slug
curl -X GET "http://localhost:8000/api/summaries/slug/2024-02-06-ai-news"

# Get AI-related tweets
curl -X GET "http://localhost:8000/api/tweets?ai_related=true&limit=50"

# Get metrics
curl -X GET "http://localhost:8000/api/metrics"
```

---

## Interactive Documentation

FastAPI provides interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These interfaces allow you to:
- View all endpoints
- See request/response schemas
- Test endpoints directly in the browser
- Download OpenAPI specification

---

## OpenAPI Specification

The OpenAPI (Swagger) specification is available at:

`http://localhost:8000/openapi.json`

This can be imported into tools like Postman, Insomnia, or used to generate client SDKs.

---

## Versioning

Current API version: **v1**

Future versions will be prefixed with version number:
- `/api/v1/summaries`
- `/api/v2/summaries`

---

## Support

For API issues or questions:
- Check interactive docs at `/docs`
- Review error messages in response
- Check backend logs for detailed errors
- Open GitHub issue for bugs
