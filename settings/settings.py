import logging
import datetime


path = 'books'

db_file = 'titles.txt'

# search_url = 'https://searchfloor.org' # All books
# search_url = 'https://searchfloor.org/popular?category=books&period=today' # Most popular today
search_url = 'https://searchfloor.org/popular?category=books&period=month' # Most popular month

base_url = 'https://searchfloor.org'

title_postfix = ': скачать или читать онлайн'

endpoints = {
    'posts': 'https://skanbook.ru/wp-json/wp/v2/posts',
    'media': 'https://skanbook.ru/wp-json/wp/v2/media',
    'tags': 'https://skanbook.ru/wp-json/wp/v2/tags',
    'categories': 'https://skanbook.ru/wp-json/wp/v2/categories',
    'series': 'https://skanbook.ru/wp-json/wp/v2/categories',
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
    'id': '696112726',
    'first_name': '%D0%94%D0%B0%D1%80%D1%8C%D1%8F',
    'last_name': '%D0%9A%D1%83%D1%80%D0%B8%D0%BB%D0%BA%D0%BE',
    'username': 'goldperson666',
    'auth_date': '1717851442',
    'hash': 'a0b5a35f22a7035a414ff88251ec3ce47ebe3f929caff6993d9c64b1062b3b88',
}

current_year = datetime.datetime.now().strftime("%Y")
current_date = datetime.datetime.now().strftime("%d.%m.%Y")

PARSE_INTERVAL = 0 # seconds

series_category_id = 207
exclude_category_names = ['Серия', 'read']
