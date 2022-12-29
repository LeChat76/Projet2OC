import requests
from bs4 import BeautifulSoup
import os
import shutil
def download_img_product(product_page_url, title, category):

    product_page = requests.get(product_page_url)
    soup_img = BeautifulSoup(product_page.content, 'html.parser')

    # image_url
    # find class item active (only one on all the html)
    # and looking for img url by searching ../../ at the beginning and jpg at the end
    image = str(soup_img.find(class_="item active"))
    pos1 = image.find("../../") + 6
    pos2 = image.find("jpg", pos1) + 3
    image_url = ("http://books.toscrape.com/" + (image[pos1: pos2]))

    img_folder = os.path.join("data", category)
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)

    # downloading image file
    img = requests.get(image_url, stream=True)
    title = title.replace(":", " ").replace("'", " ").replace("*", ".").replace("/", "-").replace('"', '-').replace("?",
                                                                                                                    ".").replace(
        ",", " ")  # replace special caracters incompatible with name file
    image_ext = image_url[-4:]  # to keep the same extension in cas of other image format (bmp or other)
    with open(os.path.join(img_folder, title + image_ext), 'wb') as img_file:
        shutil.copyfileobj(img.raw, img_file)
        img_file.close()
