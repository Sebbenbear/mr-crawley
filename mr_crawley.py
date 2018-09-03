import sys
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from time import time
root_url = sys.argv[1]

def scrape_url(root_url, url):
    # if link.startswith('/'):
    #     url = parse.urljoin(root_url, url)
    url = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(url, 'html.parser')
    link_tags = soup.find_all('a')
    links = [link['href'] for link in link_tags]
    # internal_links = [link for link in links if link.startswith('/') or link.startswith(root_url)]
    internal_links = [link for link in links if link.startswith(root_url)]
    return internal_links

site_map = []
visited = set()
urls = [root_url]

while urls:
    url = urls.pop()
    visited.add(url)
    new_urls = scrape_url(root_url, url)
    site_map.extend(new_urls)
    urls.extend([url for url in new_urls if url not in visited])

for url in site_map:
    print(url)
