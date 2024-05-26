import requests
from bs4 import BeautifulSoup

base_url = 'https://searchfloor.org'


def get_books(url):
    books = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        main_div = soup.find('div', class_='tab-content')
        book_divs = main_div.find_all('div', class_='container')
        for book in book_divs:
            book_json = {}
            items = book.find_all('p')
            book_json['title'] = items[0].find('b').text
            book_json['author'] = items[1].find('a').text
            try:
                book_json['series'] = items[2].find('a').text
            except:
                book_json['series'] = ''
            book_json['url'] = base_url + book.find('button')['data-url']
            books.append(book_json)
        return books
    else:
        print(f'Request error: {response.status_code}')
        return False