# mr-crawley

A small sitemap generator.

## Design Considerations

- The sitemap excludes and does not follow any external links.
- The sitemap excludes files with the following extensions:
   - .png
- Is the sitemap directed or undirected?
- How are the internal links represented?
- We need to show the static assets each url depends on
- Show the links between pages

### What links should we include?
- Internal links can start with a /, for example `/archive`
- Internal links can start with the site name, for example `http://mysite.com/rss`

### How do we traverse the site?
What are the advantages of traversing the site using either a BFS or a DFS?
- BFS: Good for finding the shortest path - not something we really need here
- DFS: exhausting all possibilities - this sounds more appropriate.

### What container type should we use for our DFS?
- regular list with pop/append operations
- deque: High performance data type, is thread-safe and memory efficient.

### How do we represent this graph?
Some of the options:
- edge lists
- adjacency matrix
- adjacency list
- instances of a Node class linked to children Nodes

### How do we display this graph?
- Print out some ASCII form of a sitemap
- Generate a pdf with nodes (circles) with text inside(url) and directed lines linking to other nodes
- Display adjacency matrix
- Create XML document

### Set up the Virtual Environment

Install pyenv if you don't have it already, to manage the different python runtimes you might need. If you're on OSX, use homebrew with the following command, otherwise defer to the [github page](https://github.com/pyenv/pyenv)
`brew install pyenv`

Locate the version of Python to install in your home directory.
`pyenv versions -l`

Install the version you want, for example 3.7.0.
`pyenv install 3.7.0`

Create the virtual environment, for example:
`~/.pyenv/versions/3.7.0/bin/python -m venv venv`

Next, we should activate our new virtual environment.
`source ./venv/bin/activate`

We should then generate our requirements.txt file for others to use later.
`pip freeze > requirements.txt`
