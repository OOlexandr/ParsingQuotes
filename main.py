import requests
from bs4 import BeautifulSoup
import json

def parse_quote(container):
    quote = container.find('span', class_='text').text
    author = container.find('small', class_='author').text
    tags = container.find_all('a', class_='tag')
    strtags = []
    for t in tags:
        strtags.append(t.text)
    quote_dict = {
        'tags': strtags,
        'author': author,
        'quote': quote}
    ref = container.find('a').attrs["href"]
    return quote_dict, ref

def parse_author(soup):
    fullname = soup.find('h3', class_='author-title').text
    born_date = soup.find('span', class_='author-born-date').text
    born_location = soup.find('span', class_='author-born-location').text
    description = soup.find('div', class_='author-description').text.strip()
    author_dict = {
        'fullname': fullname,
        'born_date': born_date,
        'born_location': born_location,
        'description': description}
    return author_dict

def main():
    url = 'https://quotes.toscrape.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    quotes = []
    authors = []
    found_authors = []
    containers = soup.find_all('div', class_='quote')

    for c in containers:
        quote, ref = parse_quote(c)
        if not quote['author'] in found_authors:
            found_authors.append(quote['author'])
            author_url = url + ref
            author_response = requests.get(author_url)
            author = parse_author(BeautifulSoup(author_response.text, 'lxml'))
            quotes.append(quote)
            authors.append(author)
    
    with open('authors.json', 'w') as a:
        json.dump(authors, a)
    with open('quotes.json', 'w') as q:
        json.dump(quotes, q)

if __name__ == "__main__":
    main()