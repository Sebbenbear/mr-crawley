from time import time

start = time()
from collections import deque, defaultdict
import sys
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from urltools import normalize

import aiohttp
import asyncio

root_url = sys.argv[1]

def scrape_url(root_url, url):
    url = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(url, 'html.parser')
    link_tags = soup.find_all('a')
    result = deque()
    for link in link_tags:
        current_link = link['href']
        if current_link.startswith(root_url):
            result.append(normalize(current_link))
    return result

site_map = defaultdict(set)
visited = set()
urls = deque([root_url])

while urls:
    # url = urls.popleft() - switching to BFS is very costly for this example.
    url = urls.pop()
    visited.add(url)
    new_urls = scrape_url(root_url, url)
    for new_url in new_urls:
        site_map[url].add(new_url)
    urls.extend((url for url in new_urls if url not in visited))

# Finally, print the site map
for url in site_map:
    print(url)
    values = site_map[url]
    for value in values:
        print('\t' + value)

end = time()
print('Time taken: {0:.2f}'.format(end-start))