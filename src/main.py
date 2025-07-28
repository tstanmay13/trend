import requests
import json
from datetime import datetime
from pathlib import Path
import os

def fetch_github_trending():
    """Fetch top 5 trending GitHub repositories"""
    url = "https://api.github.com/search/repositories?q=created:>2024-01-01&sort=stars&order=desc"
    
    # Add headers to avoid rate limiting issues
    headers = {
        'User-Agent': 'TechTrendsBot/1.0',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # This will raise an exception for 4XX/5XX status codes
        
        data = response.json()
        
        # Debug: print the response structure
        print(f"GitHub API Response Status: {response.status_code}")
        print(f"GitHub API Response Keys: {list(data.keys())}")
        
        if 'items' not in data:
            print(f"Unexpected GitHub API response: {data}")
            return []
            
        repos = data['items'][:5]
        return [{
            'title': repo['full_name'],
            'url': repo['html_url'],
            'stars': repo['stargazers_count'],
            'description': repo['description']
        } for repo in repos]
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching GitHub data: {str(e)}")
        return []
    except KeyError as e:
        print(f"Error parsing GitHub response: {str(e)}")
        print(f"Response data: {response.text[:500]}...")  # Print first 500 chars
        return []
    except Exception as e:
        print(f"Unexpected error in fetch_github_trending: {str(e)}")
        return []

def fetch_hackernews_top():
    """Fetch top 5 Hacker News stories from past 24h"""
    try:
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(url)
        response.raise_for_status()
        story_ids = response.json()[:5]
        
        stories = []
        for id in story_ids:
            try:
                story_response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json")
                story_response.raise_for_status()
                story = story_response.json()
                
                if story and 'title' in story:
                    stories.append({
                        'title': story['title'],
                        'url': story.get('url', f"https://news.ycombinator.com/item?id={id}"),
                        'score': story.get('score', 0)
                    })
            except Exception as e:
                print(f"Error fetching Hacker News story {id}: {str(e)}")
                continue
                
        return stories
    except Exception as e:
        print(f"Error fetching Hacker News data: {str(e)}")
        return []

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
    try:
        url = "https://pypi.org/rss/packages.xml"
        response = requests.get(url)
        response.raise_for_status()
        
        # Simple XML parsing - in production you'd want to use proper XML parsing
        entries = response.text.split("<item>")[1:6]
        packages = []
        
        for entry in entries:
            try:
                name = entry.split("<title>")[1].split("</title>")[0]
                url = entry.split("<link>")[1].split("</link>")[0]
                packages.append({
                    'name': name,
                    'url': url
                })
            except Exception as e:
                print(f"Error parsing PyPI entry: {str(e)}")
                continue
                
        return packages
    except Exception as e:
        print(f"Error fetching PyPI data: {str(e)}")
        return []

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
    try:
        print("Starting tech trends data collection...")
        
        # Create data directory if it doesn't exist
        Path("data").mkdir(exist_ok=True)
        
        # Fetch data from all sources with individual error handling
        print("Fetching GitHub trending data...")
        github_data = fetch_github_trending()
        print(f"GitHub data: {len(github_data)} items found")
        
        print("Fetching Hacker News data...")
        hackernews_data = fetch_hackernews_top()
        print(f"Hacker News data: {len(hackernews_data)} items found")
        
        print("Fetching Reddit data...")
        reddit_data = fetch_reddit_top()
        print(f"Reddit data: {len(reddit_data)} items found")
        
        print("Fetching NPM trending data...")
        npm_data = fetch_npm_trending()
        print(f"NPM data: {len(npm_data)} items found")
        
        print("Fetching PyPI trending data...")
        pypi_data = fetch_pypi_trending()
        print(f"PyPI data: {len(pypi_data)} items found")
        
        # Check if we have any data at all
        total_items = len(github_data) + len(hackernews_data) + len(reddit_data) + len(npm_data) + len(pypi_data)
        print(f"Total items collected: {total_items}")
        
        if total_items == 0:
            print("Warning: No data was collected from any source. Creating empty summary.")
            markdown = f"# Tech Trends Summary - {datetime.now().strftime('%Y-%m-%d')}\n\nNo data was available at this time."
        else:
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
            'pypi_trending': pypi_data,
            'summary': {
                'total_items': total_items,
                'sources_with_data': sum([
                    len(github_data) > 0,
                    len(hackernews_data) > 0,
                    len(reddit_data) > 0,
                    len(npm_data) > 0,
                    len(pypi_data) > 0
                ])
            }
        }
        
        # Save files
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        print(f"Saving data to data/{date_str}-summary.md")
        with open(f"data/{date_str}-summary.md", 'w') as f:
            f.write(markdown)
            
        print(f"Saving data to data/{date_str}-trends.json")
        with open(f"data/{date_str}-trends.json", 'w') as f:
            json.dump(json_data, f, indent=2)
            
        print("Data collection completed successfully!")
        
    except Exception as e:
        print(f"Critical error in main function: {str(e)}")
        print("Attempting to save partial data...")
        
        # Try to save whatever we have
        try:
            date_str = datetime.now().strftime("%Y-%m-%d")
            error_markdown = f"# Tech Trends Summary - {date_str}\n\nError occurred during data collection: {str(e)}"
            
            with open(f"data/{date_str}-summary.md", 'w') as f:
                f.write(error_markdown)
                
            error_json = {
                'date': date_str,
                'error': str(e),
                'status': 'failed'
            }
            
            with open(f"data/{date_str}-trends.json", 'w') as f:
                json.dump(error_json, f, indent=2)
                
            print("Error data saved successfully.")
        except Exception as save_error:
            print(f"Failed to save error data: {str(save_error)}")
        
        # Don't exit with error code - let the workflow continue
        print("Continuing despite errors...")

if __name__ == "__main__":
    main()
