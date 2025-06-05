import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def parse_page(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        h1 = len(soup.find_all('h1'))
        h2 = len(soup.find_all('h2'))
        h3 = len(soup.find_all('h3'))

        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(url, href)
            links.append(absolute_url)

        return {
            'h1_count': h1,
            'h2_count': h2,
            'h3_count': h3,
            'links': links
        }
    except Exception as e:
        return {'error': str(e)}
