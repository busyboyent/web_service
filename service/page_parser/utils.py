import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def parse_page(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        return {
            'h1': len(soup.find_all('h1')),
            'h2': len(soup.find_all('h2')),
            'h3': len(soup.find_all('h3')),
            'a': list(map(lambda x: urljoin(url, x['href']), soup.find_all('a', href=True)))
        }
    except Exception as e:
        return {'error': str(e)}
