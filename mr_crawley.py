from time import time, sleep

start = time()
from collections import deque, defaultdict
import sys
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from urltools import normalize

from queue import Queue
from threading import Thread, current_thread

NUM_WORKER_THREADS = 20

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

messages_for_producer = Queue()
messages_for_workers = Queue()

def producer():
    counter = 0
    task_counter = 0
    active_threads = NUM_WORKER_THREADS
    just_started = True # Set this to try to avoid premptive completion
    while (active_threads > 0) and (just_started or (task_counter != 0)):
        print('Top of assigner loop: task_counter == {}'.format(task_counter))
        just_started = False
        msg_type, data = messages_for_producer.get()
        if msg_type == 'url_for_processing':
            parent_url, new_url = data
            print('a({}): assigner recieved {}, {}'.format(counter, parent_url, new_url))
            site_map[parent_url].add(new_url)
            if new_url not in site_map:
                messages_for_workers.put(new_url)
                task_counter += 1
                print('a({}): assigner added {} to messages_for_workers'.format(counter, new_url))
            else:
                print('a({}): assigner did nothing with {}'.format(counter, new_url))
        elif msg_type == 'worker_task_complete':
            print('a({}): assigner recieved completion message, {}'.format(counter, data))
            task_counter -= 1
        elif msg_type == 'worker_task_failure':
            print('a({}): assigner recieved failure message, {}'.format(counter, data))
            active_threads -= 1
            task_counter -= 1
            
        counter += 1
        print('Bottom of assigner loop: task_counter == {}, active_threads = {}'.format(task_counter, active_threads))
    
    for _ in range(NUM_WORKER_THREADS):
        messages_for_workers.put(None) # tell thread workers to stop

# Define our workers to get a url off the queue, process it, and add things back onto the queue
def worker():
    while True:
        url = messages_for_workers.get()
        if url is None:
            break
        try:    
            new_urls = scrape_url(root_url, url)
        except: #urllib.error.HTTPError, etc
            messages_for_producer.put(('worker_task_failure', url))
        
        for new_url in new_urls:
            messages_for_producer.put(('url_for_processing', (url, new_url))) # add everything to messages_for_producer

        messages_for_producer.put(('worker_task_complete', url))

threads = []

t = Thread(target=producer)
t.start()
threads.append(t)

# Add our threads to a collection and start them up
for i in range(NUM_WORKER_THREADS):
    t = Thread(target=worker)
    t.start()
    threads.append(t)

# Put the root url in the queue
messages_for_producer.put(('found', ('root', root_url)))

for t in threads:
    t.join()  # wait for all the threads to finish

# Finally, print the site map
for url in site_map:
    print(url)
    values = site_map[url]
    for value in values:
        print('\t' + value)

end = time()
print('Time taken: {0:.2f}'.format(end-start))