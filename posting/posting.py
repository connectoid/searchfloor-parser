import requests
import os
import base64
from pprint import pprint
from time import sleep

from dotenv import load_dotenv

from tools.tools import download_file, extract_zip
from settings.settings import endpoints, title_postfix

load_dotenv()
app_password = os.getenv('app_password')
user = "autoposter"
credentials = user + ':' + app_password
token = base64.b64encode(credentials.encode())
header = {'Authorization': 'Basic ' + token.decode('utf-8')}


def create_post(book):
    url = endpoints['posts']
    post = {
        'title': book['title'], # + title_postfix,
        'status': 'publish',
        'content': book['content'],
        # 'excerpt': 'Это поле EXCERPT',
        'categories': book['categories'],
        'featured_media': book['featured_media'],
        'tags': book['tags'],
        'acf': {
            "namebook": book['title'],
            "карточка_вклвыкл": "Вкл",
            "avtor": book['avtor'],
            "yazyk": book['yazyk'],
            "zhanr": ', '.join(book['genres']),
            "year": '2024',
            "download_title": f"Скачать книгу {book['title']} бесплатно",
            "enable-scan-download": True,
        }
    }
    post['acf'][f"choose_fb2"] = {
            "choose_type_of_load": "file",
            "choose_file": book['choose_file_fb2'],
            "choose_link": ""
        }
    post['acf'][f"choose_txt"] = {
            "choose_type_of_load": "file",
            "choose_file": book['choose_file_txt'],
            "choose_link": ""
        }
    response = requests.post(url , headers=header, json=post)
    book_slug = response.json()['slug']
    id = response.json()['id']
    return id, book_slug


def update_post_by_reedon_link(post_id, link):
    endpoint = endpoints['posts']
    url = f'{endpoint}/{post_id}'
    post = {
        'acf': {
            "reedon": link,
        }
    }
    response = requests.post(url , headers=header, json=post)
    if response.status_code == 200:
        return True
    else:
        return False



def upload_media(filename, path):
    url = endpoints['media']
    file_data = open(f'{path}/{filename}', 'rb').read()
    headers = {
        # 'Content-Type': 'multipart/form-data',
        'Content-Type': 'image/jpeg',
        'Content-Disposition': f'attachment;filename={filename}',
        'Authorization': 'Basic ' + token.decode('utf-8')
    }
    response = requests.post(url, data=file_data, headers=headers)
    return response.json()['id']


def upload_book(filename, path):
    url = endpoints['media']
    file_data = open(f'{path}/{filename}', 'rb').read()
    headers = {
        'Content-Type': 'multipart/form-data',
        'Content-Disposition': f'attachment;filename={filename}',
        'Authorization': 'Basic ' + token.decode('utf-8')
    }
    response = requests.post(url, data=file_data, headers=headers)
    return response.json()['id']


def get_tag_by_id(id):
    endpoint = endpoints['tags']
    endpoint = f'{endpoint}/{id}'
    response = requests.get(endpoint , headers=header)
    link = response.json()['link']
    return link





def get_or_create_tag(authors):
    endpoint = endpoints['tags']
    authors_ids = []
    authors_urls = []
    author_slug = ''
    for author in authors:
        print(f'Processing Author: {author}')
        tag = {
            'name': author,
            'description': f'В нашей рубрике вы найдете бесплатные онлайн версии книг автора {author}. Сможете прочитать или же скачать их. Откройте для себя великолепный мир слов, где каждая строчка – это приглашение в увлекательное приключение.',
        }
        response = requests.post(endpoint , headers=header, json=tag)
        response_json = response.json()
        if 'code' in response_json:
            if response_json['code'] == 'term_exists':
                id = response_json['data']['term_id']
                url = get_tag_by_id(id)
                tag_endpoint = f'{endpoint}/{id}'
                tag_response = requests.post(tag_endpoint , headers=header,)
                if not author_slug:
                    author_slug = tag_response.json()['slug']
        else:
            id = response_json['id']
            url = response_json['link']
            if not author_slug:
                author_slug = response_json['slug']
        authors_ids.append(id)
        authors_urls.append(url)
    return authors_ids, authors_urls, author_slug


def find_author(author_name):
    url = endpoints['tags']
    response = requests.get(url, headers=header)
    for item in response.json():
        if item['name'] == author_name:
            return item['link']
    return False


def get_category_link_by_id(id):
    url = endpoints['categories']
    url = f'{url}/{id}'
    response = requests.get(url, headers=header)
    category_link = response.json()['link']
    return category_link


def get_categories():
    print('Запрашиваем список категорий (жанров)')
    categories_list = []
    categories_dict = {}
    url = endpoints['categories']
    response = requests.get(url, headers=header)
    for category in response.json():
        category_name = category['name']
        category_id = category['id']
        categories_list.append(f'{category_name}')
        categories_dict[category_name] = category_id
    return categories_list, categories_dict

