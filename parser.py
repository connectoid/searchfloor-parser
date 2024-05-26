from pprint import pprint

from FB2 import FictionBook2, Author

from parsing.parsing import get_books, base_url
from tools.tools import download_file, convert_fb2_to_pdf, extract_cover_from_fb2

path = 'books'
search_url = 'https://searchfloor.org/popular?category=books&period=today'

books = get_books(search_url)
count = 0
if books:
    for book in books:
        filename = download_file(book['url'], path)
        if filename:
            print(f'Скачана книга {filename}')
            pdf_filename = convert_fb2_to_pdf(filename, path)
            picture_filename = extract_cover_from_fb2(filename, path)
            # print(pdf_filename, picture_filename)
            count += 1
        if count > 5:
            break
