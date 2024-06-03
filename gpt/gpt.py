import requests
import os

from dotenv import load_dotenv

from settings.settings import prompt_description
from posting.posting import get_categories

load_dotenv()
# api_key = os.getenv('api_key')
api_keys = []
api_keys.append(os.getenv('api_key_1'))
api_keys.append(os.getenv('api_key_2'))
api_keys.append(os.getenv('api_key_3'))




def add_file(filename, path, api_key):
    print('Загружаем файл на ChatPDF')
    files = [
        ('file', ('file', open(f'{path}/{filename}', 'rb'), 'application/octet-stream'))
    ]
    headers = {
        'x-api-key': api_key
    }
    try:
        response = requests.post(
            'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)

        if response.status_code == 200:
            print('Получен Source ID:', response.json()['sourceId'])
            source_id = response.json()['sourceId']
            return source_id
        else:
            print('Status:', response.status_code)
            print('ChatPDF: add_file Error:', response.text)
            return False
    except Exception as e:
        print(f'Ошибка запроса к ЧатПФД: {e}')
        print(f'Возможно закончилась подписка, пробуем следующий ключ')


def get_description(filename, path):
    genres_list, genres_dict = get_categories()
    prompt_genre =  f"""
        Выбери один или несколько жанров из этого списка {genres_list} к которым можно отнести эти книги. В ответе укажи только один или несколько жанров через запятную, в точности так же как в этом списке {genres_list}
    """
    print('Получаем описание книги с ChatPDF')
    for api_key in api_keys:
        source_id = add_file(filename, path, api_key)
        if source_id:
            headers = {
                'x-api-key': f'{api_key}',
                "Content-Type": "application/json",
            }
            data_description = {
                'sourceId': source_id,
                'messages': [
                    {
                        'role': "user",
                        'content': prompt_description,
                    }
                ]
            }

            data_genre = {
                'sourceId': source_id,
                'messages': [
                    {
                        'role': "user",
                        'content': prompt_genre,
                    }
                ]
            }

            response_description = requests.post(
                'https://api.chatpdf.com/v1/chats/message', headers=headers, json=data_description)
            if response_description.status_code == 200:
                print('Описание получено')
                description = response_description.json()['content']
                print(description[:50] + '...')
            else:
                print('Status:', response_description.status_code)
                print('ChatPDF: response_description Error:', response_description.text)
                description = False

            
            response_genre = requests.post(
                'https://api.chatpdf.com/v1/chats/message', headers=headers, json=data_genre)
            if response_genre.status_code == 200:
                print('Жанры получены')
                genres = response_genre.json()['content']
                try:
                    genres_names = genres.split(',')
                    genres_ids = [genres_dict[genre.strip()] for genre in genres_names]
                except:
                    print('ChatPDF: Error converting genres to list')
                    genres_names = ['Романы']
                    genres_ids = [14]
            else:
                print('Status:', response_genre.status_code)
                print('ChatPDF: response_genre Error:', response_genre.text)
                genres_ids = False
                genres_names = False
            
            return description, genres_names, genres_ids
        else:
            print('ChatPDF: Ошибка загрузки файла, возможно закончилась подписка на ChatPDF')
            print('Пробуем следующий ключ')
    print('Попытки использования ключа закончились')
    return False, False, False
