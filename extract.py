import xml.dom.minidom
import base64
 
file = 'books/07_zakon_sily_roman_alekseya_osadchuka.fb2'
 
doc = xml.dom.minidom.parse(file)
pictures_links = doc.getElementsByTagName('binary')
minimal = 0
for pictures_link in pictures_links:
    nodes = pictures_link.childNodes
    for node in nodes:
        if node.nodeType == node.TEXT_NODE:
            base64_pictures_bytes = node.data.encode('utf-8')
            pictures_name = str('pictures') + str(minimal) + str('.png')
            with open(pictures_name, 'wb') as file_to_save:
                decoded_image_data = base64.decodebytes(base64_pictures_bytes)
                file_to_save.write(decoded_image_data)
                minimal = int(minimal)
                minimal = minimal + 1