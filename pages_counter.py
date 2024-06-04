import PyPDF2
from pathlib import Path

pathlist = Path('books').rglob('*.pdf')
overall_pages = 0
books_count = 0
for path in pathlist:
    books_count += 1
    path_in_str = str(path)
    print(f'{books_count}. {path_in_str}')
    pdfReader = PyPDF2.PdfReader(path_in_str)
    totalPages = len(pdfReader.pages)           
    overall_pages += totalPages
print(f'Total book: {books_count}\n Total pages: {overall_pages}\n Average pages in book: {overall_pages / books_count}\n')