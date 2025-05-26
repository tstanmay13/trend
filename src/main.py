import requests
import json
from datetime import datetime
from pathlib import Path
import os

def fetch_github_trending():
    """Fetch top 5 trending GitHub repositories"""
    url = "https://api.github.com/search/repositories?q=created:>2024-01-01&sort=stars&order=desc"
    response = requests.get(url)
    repos = response.json()['items'][:5]
    return [{
        'title': repo['full_name'],
        'url': repo['html_url'],
        'stars': repo['stargazers_count'],
        'description': repo['description']
    } for repo in repos]

def fetch_hackernews_top():
    """Fetch top 5 Hacker News stories from past 24h"""
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    story_ids = requests.get(url).json()[:5]
    stories = []
    for id in story_ids:
        story = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json").json()
        stories.append({
            'title': story['title'],
            'url': story.get('url', f"https://news.ycombinator.com/item?id={id}"),
            'score': story['score']
        })
    return stories

def fetch_reddit_top():
    """Fetch top 5 posts from r/programming"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json'
    }
    url = "https://www.reddit.com/r/programming/top.json?t=day&limit=5"
    try:
        response = requests.get(url, headers=headers, allow_redirects=True)
        response.raise_for_status()
        data = response.json()
        posts = data['data']['children']
        return [{
            'title': post['data']['title'],
            'url': f"https://reddit.com{post['data']['permalink']}",
            'score': post['data']['score']
        } for post in posts]
    except Exception as e:
        print(f"Error fetching Reddit data: {str(e)}")
        return []

def fetch_npm_trending():
    """Fetch top 5 NPM packages by downloads"""
    try:
        # Get top packages from npmjs.com/browse/depended
        url = "https://registry.npmjs.org/-/v1/search?text=popularity:>10000&size=5"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        return [{
            'name': pkg['package']['name'],
            'downloads': pkg['package']['downloads'] if 'downloads' in pkg['package'] else 'N/A'
        } for pkg in data['objects']]
    except Exception as e:
        print(f"Error fetching NPM data: {str(e)}")
        return []

def fetch_pypi_trending():
    """Fetch top 5 trending PyPI packages"""
    url = "https://pypi.org/rss/packages.xml"
    response = requests.get(url)
    # Simple XML parsing - in production you'd want to use proper XML parsing
    entries = response.text.split("<item>")[1:6]
    return [{
        'name': entry.split("<title>")[1].split("</title>")[0],
        'url': entry.split("<link>")[1].split("</link>")[0]
    } for entry in entries]

def format_markdown(github, hackernews, reddit, npm, pypi):
    """Format the data as markdown"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    md = f"# Tech Trends Summary - {today}\n\n"
    
    if github:
        md += "## GitHub Trending\n"
        for repo in github:
            md += f"- [{repo['title']}]({repo['url']}) - ⭐ {repo['stars']}\n  {repo['description']}\n"
    
    if hackernews:
        md += "\n## Hacker News Top Stories\n"
        for story in hackernews:
            md += f"- [{story['title']}]({story['url']}) - 👍 {story['score']}\n"
    
    if reddit:
        md += "\n## Reddit r/programming\n"
        for post in reddit:
            md += f"- [{post['title']}]({post['url']}) - 👍 {post['score']}\n"
    
    if npm:
        md += "\n## NPM Trending\n"
        for pkg in npm:
            downloads = pkg['downloads'] if isinstance(pkg['downloads'], int) else 'N/A'
            md += f"- {pkg['name']} - 📦 {downloads}\n"
    
    if pypi:
        md += "\n## PyPI Trending\n"
        for pkg in pypi:
            md += f"- [{pkg['name']}]({pkg['url']})\n"
    
    return md

def main():
    # Create data directory if it doesn't exist
    Path("data").mkdir(exist_ok=True)
    
    # Fetch data from all sources
    github_data = fetch_github_trending()
    hackernews_data = fetch_hackernews_top()
    reddit_data = fetch_reddit_top()
    npm_data = fetch_npm_trending()
    pypi_data = fetch_pypi_trending()
    
    # Generate markdown summary
    markdown = format_markdown(
        github_data,
        hackernews_data,
        reddit_data,
        npm_data,
        pypi_data
    )
    
    # Prepare JSON data
    json_data = {
        'date': datetime.now().strftime("%Y-%m-%d"),
        'github_trending': github_data,
        'hackernews_top': hackernews_data,
        'reddit_programming': reddit_data,
        'npm_trending': npm_data,
        'pypi_trending': pypi_data
    }
    
    # Save files
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    with open(f"data/{date_str}-summary.md", 'w') as f:
        f.write(markdown)
        
    with open(f"data/{date_str}-trends.json", 'w') as f:
        json.dump(json_data, f, indent=2)

if __name__ == "__main__":
    main()
