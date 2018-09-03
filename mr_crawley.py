import urllib.request
from bs4 import BeautifulSoup

# https://stackoverflow.com/questions/9029822/how-can-i-bring-google-like-recrawling-in-my-applicationweb-or-console/9099798#9099798
def scrape(root_url, url):
    # do some conditional checking here
    url = root_url + url
    url = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(url, 'html.parser')
    link_tags = soup.find_all('a')
    links = [link['href'] for link in link_tags if 'href' in link.attrs.keys() and link['href'].startswith('.')]
    return links

root_url = 'https://vaibhavsagar.com/'

# visited = set()
# urls = []
# urls.extend(scrape('', root_url))
# while urls:
#     url = urls.pop()
#     visited.add(url)
#     urls.extend([link for link in scrape(root_url, url) if link not in visited])
# print(visited)

site_map = {root_url: {}}

visited = set()
urls = scrape('', root_url)
for url in urls:
    site_map[url] = scrape(root_url, url)

print(site_map)

