# 📰 Daily Tech Trends

Automatically fetches and commits trending repositories, news, and packages from top developer sources:

- 🚀 GitHub Trending
- 🔥 Hacker News (last 24h)
- 👨‍💻 Reddit /r/programming  -- not working at the moment
- 📦 npm (top packages)
- 🐍 PyPI (popular Python packages)

## 📆 How It Works

This project uses **GitHub Actions** to run a Python script every day at 4AM UTC. The script:

1. Pulls top 5 items from each platform.
2. Generates a Markdown and JSON report.
3. Commits the report to the `data/` directory.

## 🚀 Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/daily-tech-trends.git
cd daily-tech-trends
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python src/main.py
``` 

## Testing

You can test individual scrapers:

```bash
python src/github_trending.py        # Test GitHub trends
python src/hackernews_trending.py    # Test Hacker News
python src/reddit_trending.py        # Test Reddit
python src/npm_trending.py           # Test npm
python src/pypi_trending.py          # Test PyPI

```
Or run everything and generate the full report:

```bash
python src/main.py
Check the output in data/YYYY-MM-DD-summary.md and .json.
```
