import requests

def fetch_pypi_trending():
    """Fetch top 5 most downloaded Python packages using PyPI Stats API"""
    # Get top packages from PyPI Stats API
    url = "https://pypistats.org/api/packages/overall"
    response = requests.get(url)
    
    if response.status_code != 200:
        return []
        
    packages = response.json()['data']
    
    # Sort by downloads and get top 5
    packages.sort(key=lambda x: x['downloads'], reverse=True)
    top_packages = packages[:5]
    
    # Format response
    return [{
        'name': pkg['package'],
        'downloads': pkg['downloads'],
        'url': f"https://pypi.org/project/{pkg['package']}"
    } for pkg in top_packages]
