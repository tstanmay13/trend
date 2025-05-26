import requests
from bs4 import BeautifulSoup

def fetch_github_trending():
    """Fetch top 5 trending GitHub repositories from github.com/trending"""
    url = "https://github.com/trending"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    trending_repos = []
    repo_articles = soup.select('article.Box-row')[:5]
    
    for article in repo_articles:
        # Get repository name (format: owner/repo)
        name = article.select_one('h2 a').get('href').strip('/')
        
        # Get stars gained today
        try:
            stars_today = article.select_one('.float-sm-right').text.strip()
            stars_today = int(stars_today.split()[0].replace(',', ''))
        except:
            stars_today = 0
            
        # Construct repository URL
        url = f"https://github.com/{name}"
        
        trending_repos.append({
            'name': name,
            'stars_today': stars_today,
            'url': url
        })
    
    return trending_repos
