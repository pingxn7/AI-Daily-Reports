# Contributing to AI News Collector

Thank you for your interest in contributing to AI News Collector! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors.

### Our Standards

- Be respectful and considerate
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Accept responsibility and apologize for mistakes
- Prioritize the community's best interests

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a branch** for your changes
4. **Make your changes** following our coding standards
5. **Test your changes** thoroughly
6. **Submit a pull request**

## Development Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 14+
- Git

### Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
# Edit .env with your configuration
alembic upgrade head
python scripts/seed_accounts.py
```

### Frontend Setup

```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with your configuration
```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **Bug fixes**: Fix issues in existing code
- **New features**: Add new functionality
- **Documentation**: Improve or add documentation
- **Tests**: Add or improve test coverage
- **Performance**: Optimize existing code
- **Refactoring**: Improve code quality
- **UI/UX**: Enhance user interface and experience

### Finding Issues to Work On

- Check the [Issues](https://github.com/yourusername/ai-news-collector/issues) page
- Look for issues labeled `good first issue` for beginners
- Look for issues labeled `help wanted` for areas needing assistance
- Comment on an issue to let others know you're working on it

## Coding Standards

### Python (Backend)

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Keep functions small and focused
- Use meaningful variable names

**Example:**

```python
def calculate_engagement_score(tweet_data: dict) -> float:
    """
    Calculate engagement score from tweet metrics.

    Args:
        tweet_data: Dictionary containing engagement metrics

    Returns:
        Calculated engagement score
    """
    likes = tweet_data.get('like_count', 0)
    retweets = tweet_data.get('retweet_count', 0)
    # ... implementation
    return score
```

### TypeScript/JavaScript (Frontend)

- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use TypeScript for type safety
- Use functional components with hooks
- Keep components small and reusable
- Use meaningful component and variable names

**Example:**

```typescript
interface TweetCardProps {
  tweet: ProcessedTweet;
  variant: 'full' | 'compact';
}

export function TweetCard({ tweet, variant }: TweetCardProps) {
  // ... implementation
}
```

### General Guidelines

- Write clear, self-documenting code
- Add comments for complex logic
- Keep lines under 100 characters
- Use consistent indentation (2 spaces for JS/TS, 4 spaces for Python)
- Remove unused imports and variables
- Avoid hardcoded values; use configuration

## Testing

### Backend Testing

We use pytest for backend testing.

**Writing Tests:**

```python
# tests/test_twitter_collector.py
import pytest
from app.services.twitter_collector import TwitterCollector

def test_calculate_engagement_score():
    collector = TwitterCollector()
    tweet_data = {
        'like_count': 100,
        'retweet_count': 50,
        'reply_count': 25,
        'bookmark_count': 10
    }
    score = collector.calculate_engagement_score(tweet_data)
    assert score > 0
    assert isinstance(score, float)
```

**Running Tests:**

```bash
cd backend
pytest
pytest -v  # Verbose output
pytest tests/test_twitter_collector.py  # Specific file
pytest -k "test_engagement"  # Specific test pattern
```

### Frontend Testing

We use Jest and React Testing Library for frontend testing.

**Writing Tests:**

```typescript
// components/__tests__/TweetCard.test.tsx
import { render, screen } from '@testing-library/react';
import { TweetCard } from '../TweetCard';

describe('TweetCard', () => {
  it('renders tweet content', () => {
    const mockTweet = {
      // ... mock data
    };
    render(<TweetCard tweet={mockTweet} variant="full" />);
    expect(screen.getByText(/test tweet/i)).toBeInTheDocument();
  });
});
```

**Running Tests:**

```bash
cd frontend
npm test
npm test -- --coverage  # With coverage
```

### Test Coverage

- Aim for at least 80% code coverage
- Write tests for all new features
- Write tests for bug fixes to prevent regression
- Test edge cases and error conditions

## Pull Request Process

### Before Submitting

1. **Update your branch** with the latest main branch
2. **Run all tests** and ensure they pass
3. **Run linters** and fix any issues
4. **Update documentation** if needed
5. **Add/update tests** for your changes

### Submitting a Pull Request

1. **Push your branch** to your fork
2. **Create a pull request** on GitHub
3. **Fill out the PR template** completely
4. **Link related issues** using keywords (e.g., "Fixes #123")
5. **Request review** from maintainers

### PR Title Format

Use conventional commit format:

- `feat: Add new feature`
- `fix: Fix bug in component`
- `docs: Update documentation`
- `test: Add tests for feature`
- `refactor: Refactor code`
- `style: Format code`
- `chore: Update dependencies`

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
```

### Review Process

- Maintainers will review your PR
- Address any feedback or requested changes
- Once approved, a maintainer will merge your PR
- Your contribution will be included in the next release

## Reporting Bugs

### Before Reporting

1. **Check existing issues** to avoid duplicates
2. **Try the latest version** to see if the bug is fixed
3. **Gather information** about the bug

### Bug Report Template

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., macOS 13.0]
- Python version: [e.g., 3.11]
- Node version: [e.g., 18.0]
- Browser: [e.g., Chrome 120]

## Screenshots
If applicable

## Additional Context
Any other relevant information
```

## Suggesting Features

### Feature Request Template

```markdown
## Feature Description
Clear description of the feature

## Problem It Solves
What problem does this feature address?

## Proposed Solution
How should this feature work?

## Alternatives Considered
Other approaches you've considered

## Additional Context
Any other relevant information
```

## Development Workflow

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation
- `refactor/description` - Code refactoring
- `test/description` - Test additions

### Commit Messages

Follow conventional commit format:

```
type(scope): subject

body

footer
```

**Example:**

```
feat(backend): add engagement-based ranking

Implement importance scoring algorithm that combines
engagement metrics with AI relevance scores.

Closes #123
```

### Code Review Guidelines

**For Authors:**
- Keep PRs focused and small
- Respond to feedback promptly
- Be open to suggestions
- Explain your reasoning

**For Reviewers:**
- Be constructive and respectful
- Focus on code, not the person
- Explain why changes are needed
- Approve when ready

## Project Structure

### Backend Structure

```
backend/
├── app/
│   ├── main.py           # FastAPI app
│   ├── config.py         # Configuration
│   ├── database.py       # Database setup
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   ├── api/routes/       # API endpoints
│   └── tasks/            # Scheduled tasks
├── alembic/              # Migrations
├── scripts/              # Utility scripts
└── tests/                # Tests
```

### Frontend Structure

```
frontend/
├── app/                  # Next.js pages
├── components/           # React components
├── lib/                  # Utilities
└── hooks/                # Custom hooks
```

## Getting Help

- **Documentation**: Check README, QUICKSTART, and other docs
- **Issues**: Search existing issues or create a new one
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact maintainers directly for sensitive issues

## Recognition

Contributors will be recognized in:
- CHANGELOG.md for each release
- README.md contributors section
- GitHub contributors page

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

If you have questions about contributing, please:
1. Check this document
2. Search existing issues
3. Create a new issue with the `question` label

Thank you for contributing to AI News Collector! 🎉
