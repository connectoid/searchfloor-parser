from pprint import pprint

from parsing.parsing import get_books, base_url, is_autorised
from tools.tools import download_file, convert_fb2_to_pdf, extract_cover_from_fb2, extract_genres_from_fb2
from gpt.gpt import get_description

path = 'books'
search_url = 'https://searchfloor.org/popular?category=books&period=today'

cookies = {
    '_ym_uid': '1715815768896534988',
    '_ym_d': '1715815768',
    '_ym_isad': '2',
    'session': 'eyJfcGVybWFuZW50Ijp0cnVlLCJ0ZWxlZ3JhbV9pZCI6IjY4MDM2Nzc5OTYifQ.ZlOnPg.ULWPYlINI4S8ek6-uwH28vp_3Do',
}


books = get_books(search_url)
count = 0
all_genres = []
if books:
    for book in books:
        filename = download_file(book['url'], path)
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
        if count >= 15:
            break
    print(all_genres)


# button = is_autorised(base_url, cookies)
# print(button)