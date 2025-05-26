import requests
from datetime import datetime, timedelta

def fetch_reddit_top():
    """Fetch top 5 posts from r/programming in past 24h"""
    # Use custom User-Agent to avoid API issues
    headers = {'User-Agent': 'TrendingTechBot/1.0'}
    
    # Get posts from r/programming sorted by top from past day
    url = "https://www.reddit.com/r/programming/top.json?t=day&limit=5"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return []
        
    posts = response.json()['data']['children']
    
    # Format response
    return [{
        'title': post['data']['title'],
        'url': post['data']['url'],
        'upvotes': post['data']['score']
    } for post in posts]
