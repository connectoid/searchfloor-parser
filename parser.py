from pprint import pprint

from parsing.parsing import get_books, base_url, is_autorised, extract_txt_from_fb2
from tools.tools import (download_file, convert_fb2_to_pdf, extract_cover_from_fb2, extract_genres_from_fb2,
                        login_by_tg, add_title_to_db, check_is_title_exists, get_file_size)
from posting.posting import (create_post, get_or_create_tag, upload_book, upload_media, get_category_link_by_id,
                             update_post_by_reedon_link)
from gpt.gpt import get_description
from settings.settings import path, search_url, logging, MAX_PDF_SIZE



logging.info('PARSER STARTED')

books_limit = 1

def main(session):
    books = get_books(search_url, session)
    count = 0
    if books:
        for book in books:
            if not check_is_title_exists(book['title']):
                filename = download_file(book['url'], path, session)
                txt_filename = extract_txt_from_fb2(filename, path)
                if filename:
                    print(f'Скачана книга {filename}')
                    logging.info(f'Скачана книга {filename}')
                    pdf_filename = convert_fb2_to_pdf(filename, path)
                    if get_file_size(pdf_filename, path) > MAX_PDF_SIZE:
                        print(f'Файл {pdf_filename} слишком большой, пропускаем')
                        logging.warning(f'Файл {pdf_filename} слишком большой, пропускаем')
                        continue
                    picture_filename = extract_cover_from_fb2(filename, path)
                    description, genres_names, genres_ids = get_description(pdf_filename, path)
                    if description and genres_names and genres_ids:
                        genres_urls = [get_category_link_by_id(id) for id in genres_ids]
                        genres_dict = dict(zip(genres_names, genres_urls))
                        genres = [f'<a href=\"{genres_dict[genre]}">{genre}</a>' for genre in genres_dict]
                        book['genres'] = genres
                        book['content'] = f'[xyz-ips snippet="Card"]\n<h2>Содержание книги</h2>\n{description}'
                        book['categories'] = genres_ids
                        authors_ids, authors_urls, author_slug = get_or_create_tag(book['authors'])
                        book['tags'] = authors_ids
                        authors_dict = dict(zip(book['authors'], authors_urls))
                        authors = [f'<a href=\"{authors_dict[book]}">{book}</a>' for book in authors_dict]
                        book['authors'] = authors
                        book['avtor'] = ', '.join(book['authors'])
                        book['yazyk'] = 'Русский'
                        book['year'] = '2024'
                        book['featured_media'] = upload_media(picture_filename, path)
                        book['choose_file_fb2'] = upload_book(filename, path)
                        book['choose_file_txt'] = upload_book(txt_filename, path)
                        count += 1
                        # pprint(book)
                        id, book_slug = create_post(book)
                        reedon_link = f'https://skanbook.ru/read/{book_slug}-{author_slug}-chitat-onlayn/'
                        reedon_link = reedon_link.replace('-skachat-i-chitat-onlayn', '')
                        update_post_by_reedon_link(id, reedon_link)
                        add_title_to_db(book['title'])
                    else:
                        print(f'Описание и жанр не получены, возможно закончилась подписка на ChatPDF')
                        logging.warning(f'Описание и жанр не получены, возможно закончилась подписка на ChatPDF')
                        count += 1
                        # add_title_to_db(book['title'])
                        continue
            else:
                title = book['title']
                print(f'Книга {title} уже добавлена, пропускаем.')
                logging.info(f'Книга {title} уже добавлена, пропускаем.')
            # if count >= books_limit:
            #     break


if __name__ == '__main__':
    session, status_code = login_by_tg()
    if status_code == 200:
        authorised = is_autorised(base_url, session)
        if authorised:
            print(f'Authorised: {authorised}')
            main(session)
        else:
            print(f'Авторизация на сайте источнике не пройдена')
    else:
        print(f'Ошибка при авторизации: {status_code}')