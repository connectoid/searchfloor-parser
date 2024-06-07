import logging

path = 'books'

db_file = 'titles.txt'

# search_url = 'https://searchfloor.org/popular?category=books&period=today'
search_url = 'https://searchfloor.org/popular?category=books&period=month'

base_url = 'https://searchfloor.org'

title_postfix = ': скачать или читать онлайн'

endpoints = {
    'posts': 'https://skanbook.ru/wp-json/wp/v2/posts',
    'media': 'https://skanbook.ru/wp-json/wp/v2/media',
    'tags': 'https://skanbook.ru/wp-json/wp/v2/tags',
    'categories': 'https://skanbook.ru/wp-json/wp/v2/categories',
}
prompt_description =  """
    Максимально подробно от 500 слов и не менее 5 абзацев опиши о чем книга, главных героев и сюжетную линию. Вступление не нужно, пиши сразу про книгу! Пиши только по сути, без размытых слов и фраз! Разбей текст на абзацы!
    Только не начинай с фразы: - это захватывающая книга. Пытайся писать разнообразно, не используя одни и те же вступления и заключения.
"""

logging.basicConfig(
    level=logging.DEBUG, 
    filename = "parserlog.log", 
    format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s", 
    datefmt='%H:%M:%S',
    )

MAX_PDF_SIZE = 5000000

api_keys_file = 'api_keys.txt'

login_params = {
    'id': '327720091',
    'first_name': '%D0%90%D0%BB%D0%B5%D0%BA%D1%81%D0%B5%D0%B9',
    'username': 'alex_web',
    'auth_date': '1717621921',
    'hash': '2f5a2e434fd8e6895071d64d36401bcc640918dcc73aa7232c8aee897d2a37da',
}