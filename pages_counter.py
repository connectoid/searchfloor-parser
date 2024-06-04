import PyPDF2
from pathlib import Path

pathlist = Path('books').rglob('*.pdf')
overall_pages = 0
books_count = 0
for path in pathlist:
    # because path is object not string
    path_in_str = str(path)
    pdfReader = PyPDF2.PdfReader(path_in_str)
    totalPages = len(pdfReader.pages)           
    overall_pages += totalPages
    books_count += 1
print(f'Total book: {books_count}\n Total pages: {overall_pages}\n Average pages in book: {overall_pages / books_count}\n')