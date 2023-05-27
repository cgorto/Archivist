import requests
from bs4 import BeautifulSoup
import os

# URL of the documentation
base_url = 'https://python.langchain.com/'

# Make a request to the website
r = requests.get(base_url)
r.raise_for_status()

# Parse the HTML of the site
soup = BeautifulSoup(r.text, 'html.parser')

# Get all 'a' tags with 'href' containing '.html'
links = [a['href'] for a in soup.select('a[href$=".html"]')]

for link in links:
    # Make a request to each link
    r = requests.get(base_url + link)
    r.raise_for_status()

    # Save the HTML content as a .html file
    with open(os.path.join("docs", os.path.basename(link)), 'w', encoding='utf-8') as f:
        f.write(r.text)