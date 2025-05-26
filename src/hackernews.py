import requests
from datetime import datetime, timedelta
import time

def fetch_hackernews_top():
    """Fetch top 5 most upvoted Hacker News stories from past 24h using Algolia API"""
    # Get timestamp for 24 hours ago
    yesterday = datetime.now() - timedelta(days=1)
    timestamp = int(yesterday.timestamp())
    
    # Fetch stories from Algolia API
    url = f"https://hn.algolia.com/api/v1/search_by_date?tags=story&numericFilters=created_at_i>{timestamp}"
    response = requests.get(url)
    stories = response.json()['hits']
    
    # Sort by points and get top 5
    stories.sort(key=lambda x: x.get('points', 0), reverse=True)
    top_stories = stories[:5]
    
    # Format response
    return [{
        'title': story.get('title'),
        'points': story.get('points', 0),
        'url': story.get('url', f"https://news.ycombinator.com/item?id={story.get('objectID')}")
    } for story in top_stories]
