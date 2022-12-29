# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import csv
from script_ph4 import download_img_product
def import_product_info(product_page_url, category, date_time, img_download):

    header = ["product_page_url", "universal_product_code (upc)", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]

    product_page = requests.get(product_page_url)

    print("Requesting URL " + product_page_url)

    if product_page.status_code != 200:
        print("Serveur injoignable")
        exit()
    else:
        print("Accès serveur OK")

    soup = BeautifulSoup(product_page.content, 'html.parser')

    csv_folder = os.path.join("data", "CSVs")
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    path_csv = os.path.join(csv_folder, category + "_" + date_time + "_CSV.csv")

    if not os.path.exists(path_csv):
        try:
            with open(path_csv, "a", newline='', encoding="utf-32") as csv_file:
                writer = csv.writer(csv_file, delimiter=",")
                writer.writerow(header)
                csv_file.close()

        except IOError:
            print("\nErreur lors de la creation du fichier CSV pour la catégorie " + category + ".\nAvez vous les droits de création?")
            exit()

    with open(path_csv, "a", newline='', encoding="utf-32") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")

        # values in 'td' will be used 4 times, so I declared "globally"
        # [0] universal product code
        # [2] price excluding tax
        # [3] price including tax
        # [5] number of books available
        td = soup.find_all("td")

        # product_page_url
        # already known, stored in product_page_url

        # universal_product_code(upc)
        universal_product_code = td[0].string

        # title
        title = (soup.find("li", class_="active"))
        title = title.string

        # price_including_tax
        price_including_tax = td[3].string

        # price_excluding_tax
        price_excluding_tax = td[2].string

        # number_available
        number_available = td[5].string
        number_available = (number_available.replace("In stock (", "")).replace(" available)", "")

        # product_description
        desc = soup.find("meta", attrs={"name": "description"})
        desc = (str(desc).replace("&quot;", "")).replace(";", ",")
        product_description = desc[20:-31]

        # category
        # already known, stored in category

        # image_url
        image = str(soup.find(class_="item active"))
        pos1 = image.find("../../") + 6
        pos2 = image.find("jpg", pos1) + 3
        image_url = ("http://books.toscrape.com/" + (image[pos1: pos2]))

        # review_rating
        review_rating = str(soup.find("p", class_="star-rating"))
        pos1 = review_rating.find("star-rating") + 12
        pos2 = review_rating.find(">") - 1
        review_rating = review_rating[pos1: pos2]

        line = [product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url]
        writer.writerow(line)
    csv_file.close()
    if img_download.upper() == "Y":
        download_img_product(product_page_url, title, category)
