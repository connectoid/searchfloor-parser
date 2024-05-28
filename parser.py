from pprint import pprint

from parsing.parsing import get_books, base_url, is_autorised
from tools.tools import (download_file, convert_fb2_to_pdf, extract_cover_from_fb2, extract_genres_from_fb2,
                        login_by_tg)
from gpt.gpt import get_description

path = 'books'
search_url = 'https://searchfloor.org/popular?category=books&period=today'


session, status_code = login_by_tg()
print(status_code)
authorised = is_autorised(base_url, session)
print(f'Authorised: {authorised}')


books = get_books(search_url, session)
count = 0
all_genres = []
if books:
    for book in books:
        filename = download_file(book['url'], path, session)
        if filename:
            print(f'Скачана книга {filename}')
            pdf_filename = convert_fb2_to_pdf(filename, path)
            picture_filename = extract_cover_from_fb2(filename, path)
            genres = extract_genres_from_fb2(filename, path)
            for genre in genres:
                if genre not in all_genres:
                    all_genres.append(genre)
            # description = get_description(pdf_filename, path)
            # print(description)
            count += 1
        if count >= 25:
            break
    print(all_genres)

