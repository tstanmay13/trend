import requests

def fetch_npm_trending():
    """Fetch top 5 trending NPM packages using npms.io API"""
    url = "https://api.npms.io/v2/search/suggestions?q=boost:gte:0"
    response = requests.get(url)
    
    if response.status_code != 200:
        return []
        
    packages = response.json()[:5]
    
    trending_packages = []
    for pkg in packages:
        # Get package details
        name = pkg['package']['name']
        
        # Fetch download counts from npm registry
        downloads_url = f"https://api.npmjs.org/downloads/point/last-week/{name}"
        downloads_response = requests.get(downloads_url)
        weekly_downloads = downloads_response.json().get('downloads', 0)
        
        trending_packages.append({
            'name': name,
            'downloads': weekly_downloads,
            'url': f"https://www.npmjs.com/package/{name}"
        })
    
    # Sort by weekly downloads
    trending_packages.sort(key=lambda x: x['downloads'], reverse=True)
    
    return trending_packages
