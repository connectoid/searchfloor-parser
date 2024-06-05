import PyPDF2
import os
from pathlib import Path

pathlist = Path('books').rglob('*.pdf')
overall_pages = 0
books_count = 0
for path in pathlist:
    books_count += 1
    path_in_str = str(path)
    filesize = os.path.getsize(path_in_str)
    print(f'{books_count}. {path_in_str} - {filesize}')
    pdfReader = PyPDF2.PdfReader(path_in_str)
    totalPages = len(pdfReader.pages)           
    overall_pages += totalPages
print(f'Total book: {books_count}\n Total pages: {overall_pages}\n Average pages in book: {overall_pages / books_count}\n')