import requests
import os

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('api_key')
files_dir = 'books'
prompt =  """
    Максимально подробно от 500 слов опиши о чем книга, главных героев и сюжетную линию. Вступление не нужно, пиши сразу про книгу! Пиши только по сути, без размытых слов и фраз! Разбей текст на абзацы!
    Только не начинай с фразы: - это захватывающая книга. Пытайся писать разнообразно, не используя одни и те же вступления и заключения.
"""

def add_file(filename, path):
    print('Загружаем файл на ChatPDF')
    files = [
        ('file', ('file', open(f'{path}/{filename}', 'rb'), 'application/octet-stream'))
    ]
    headers = {
        'x-api-key': api_key
    }
    response = requests.post(
        'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)

    if response.status_code == 200:
        print('Получен Source ID:', response.json()['sourceId'])
        source_id = response.json()['sourceId']
        return source_id
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)
        return False
    

def get_description(filename, path):
    print('Получаем описание книги с ChatPDF')
    source_id = add_file(filename, path)
    headers = {
        'x-api-key': f'{api_key}',
        "Content-Type": "application/json",
    }
    data = {
        'sourceId': source_id,
        'messages': [
            {
                'role': "user",
                'content': prompt,
            }
        ]
    }
    response = requests.post(
        'https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)

    if response.status_code == 200:
        print('Описание получено')
        return response.json()['content']
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)
        return False
    

# source_id = add_file('hendi.pdf', 'books')
# if source_id:
#     description = get_description(source_id)