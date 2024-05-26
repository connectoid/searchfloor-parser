import urllib.parse
import os
import xml.dom.minidom
import base64

import requests
import pymupdf
import zipfile


def extract_cover_from_fb2(filename, path):
    file = f'{path}/{filename}'
    doc = xml.dom.minidom.parse(file)
    pictures_links = doc.getElementsByTagName('binary')
    minimal = 0
    for pictures_link in pictures_links:
        nodes = pictures_link.childNodes
        for node in nodes:
            if node.nodeType == node.TEXT_NODE:
                base64_pictures_bytes = node.data.encode('utf-8')
                pictures_name = file.replace('.fb2', '.png')
                with open(pictures_name, 'wb') as file_to_save:
                    decoded_image_data = base64.decodebytes(base64_pictures_bytes)
                    file_to_save.write(decoded_image_data)
                    minimal = int(minimal)
                    minimal = minimal + 1
                    return pictures_name


def extract_zip(archive, path):
    archive = f'{path}/{archive}'
    with zipfile.ZipFile(archive, 'r') as zip_file:
        filename = zip_file.namelist()[0]
        zip_file.extractall(path)
        os.remove(archive)
    return filename


def convert_fb2_to_pdf(filename, path):
    # filename = extract_zip(filename, path)
    # filename = filename.lower()
    pdf_filename = filename.replace('.fb2', '.pdf')
    pdf_full_filename = f'{path}/{pdf_filename}'
    filename = f'{path}/{filename}'
    doc = pymupdf.open(filename) 
    pdfbytes = doc.convert_to_pdf()
    pdf = pymupdf.open("pdf", pdfbytes)
    pdf.save(pdf_full_filename)
    return pdf_filename


def download_file(url, path):
    print(f'Загружаем файл книги по ссылке {url}')
    response = requests.get(url)
    if response.status_code == 200:
        headers = response.headers
        content_disposition = headers['content-disposition']
        filename = content_disposition.split("filename*=UTF-8''")[-1]
        filename = urllib.parse.unquote(filename)
        with open(f'{path}/{filename}', 'wb') as file:
            file.write(response.content)
            new_filename = extract_zip(filename, path)
            return new_filename
    else:
        print(f'Requests error in download_file: {response.status_code}')
        return False