import requests
from bs4 import BeautifulSoup  # pip install beautifulsoup4

# URL = 'https://www.pravda.com.ua/rss/view_news/'
URL = 'https://feeds.feedburner.com/TheHackersNews'

response = requests.get(URL)

soup = BeautifulSoup(response.content, features='html.parser')

items = soup.findAll('item')

for item in items:
    title = item.find('title')
    link = item.find('link')
    ahref = link.next_element.strip() if link else ''
    pub = item.find('pubDate') or item.find('pubdate')
    description = item.find('description')
    print(f'link: {ahref} \n Title: {title.text}\npublished: {pub.text}\n====')

print(f'Parsed {len(items)} news items from {URL}.')
