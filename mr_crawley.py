from time import time

start = time()
from collections import deque
import sys
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

root_url = sys.argv[1]

def scrape_url(root_url, url):
    url = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(url, 'html.parser')
    link_tags = soup.find_all('a')
    result = deque()
    for link in link_tags:
        current_link = link['href']
        if current_link.startswith(root_url):
            result.append(current_link)
    return result

site_map = deque()
visited = set()
urls = deque([root_url])

while urls:
    url = urls.pop()
    visited.add(url)
    new_urls = scrape_url(root_url, url)
    site_map.extend(new_urls)
    urls.extend([url for url in new_urls if url not in visited])

for url in site_map:
    print(url)

end = time()
print('Time taken: {0:.2f}'.format(end-start))