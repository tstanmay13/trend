import json
from datetime import datetime

def format_markdown(github, hn, reddit, npm, pypi):
    """
    Format trending data into markdown and JSON formats
    Returns tuple of (markdown_string, json_string)
    """
    # Build markdown sections
    md = "# Daily Tech Trends\n\n"
    
    md += "## 🔥 Trending on GitHub\n"
    for repo in github:
        md += f"- [{repo['name']}]({repo['url']}) - {repo['stars_today']} stars today\n"
    
    md += "\n## 📰 Hacker News Top Stories\n"
    for story in hn:
        md += f"- [{story['title']}]({story['url']}) - {story['points']} points\n"
        
    md += "\n## 💻 r/programming Top Posts\n"
    for post in reddit:
        md += f"- [{post['title']}]({post['url']}) - {post['upvotes']} upvotes\n"
        
    md += "\n## 📦 Trending NPM Packages\n"
    for pkg in npm:
        md += f"- [{pkg['name']}]({pkg['url']}) - {pkg['downloads']:,} weekly downloads\n"
        
    md += "\n## 🐍 Top PyPI Packages\n"
    for pkg in pypi:
        md += f"- [{pkg['name']}]({pkg['url']}) - {pkg['downloads']:,} downloads\n"

    # Build JSON data
    json_data = {
        'github_trending': github,
        'hackernews_top': hn,
        'reddit_programming': reddit,
        'npm_trending': npm,
        'pypi_top': pypi,
        'generated_at': datetime.now().isoformat()
    }
    
    return md, json.dumps(json_data, indent=2)

def save_report(md, json_data):
    """Save markdown and JSON reports to data directory"""
    date = datetime.now().strftime('%Y-%m-%d')
    
    # Save markdown report
    with open(f'data/{date}-summary.md', 'w') as f:
        f.write(md)
        
    # Save JSON report  
    with open(f'data/{date}-summary.json', 'w') as f:
        f.write(json_data)

