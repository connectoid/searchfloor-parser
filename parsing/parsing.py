import requests
from bs4 import BeautifulSoup

base_url = 'https://searchfloor.org'


def get_books(url, session):
    books = []
    response = session.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        main_div = soup.find('div', class_='tab-content')
        book_divs = main_div.find_all('div', class_='container')
        count = 0
        skiped = 0
        for book in book_divs:
            book_json = {}
            items = book.find_all('p')
            title = items[0].find('b').text
            if items[0].find('a'):
                count += 1
                skiped += 1
                print(f'{count}. Найдена донатная книга {title}')
            book_json['title'] = title
            book_json['author'] = items[1].find('a').text
            try:
                book_json['series'] = items[2].find('a').text
            except:
                book_json['series'] = ''
            try:
                book_json['url'] = base_url + book.find('button')['data-url']
            except:
                print(f'Пропускаем донатную книгу {title}, так как нет подписки')
                continue
            count += 1
            print(f'{count}. Добавляем книгу {title}')
            books.append(book_json)
        print(f'Донатных книг {skiped} из {count}')
        return books
    else:
        print(f'Request error: {response.status_code}')
        return False
    

def is_autorised(url, session):
    response = session.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    loginbar = soup.find('div', class_='loginbar')
    try:
        button = loginbar.find('a').text
        return True
    except:
        return False
