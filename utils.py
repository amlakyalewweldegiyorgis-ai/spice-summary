import requests
from bs4 import BeautifulSoup


def fetch_url_text(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: Page not found or inaccessible")
    soup = BeautifulSoup(response.text, 'html.parser')
    for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
        tag.decompose()
    paragraphs = soup.find_all('p')
    text = ' '.join([p.get_text() for p in paragraphs])
    if len(text) < 100:
        raise Exception("Not enough content on page")
    return text