# -*- coding: utf-8 -*-

from script_ph2 import import_all_products_infos_cat
import requests
from bs4 import BeautifulSoup

main_url = "http://books.toscrape.com/"
main_page = requests.get(main_url)

print("Requesting URL " + main_url)

if main_page.status_code != 200:
    print("Serveur injoignable")
    exit()
else:
    print("Accès serveur OK")

main_page_soup = BeautifulSoup(main_page.content, 'html.parser')

main_categories = []
# main_url_categories = []

main_li = main_page_soup.find_all("li")
for li in main_li:
    if "category" in str(li) and not "books_1" in str(li):
        # extraction of the category
        pos1 = str(li).find("                                ") + 32
        pos2 = str(li).find("\n", pos1)
        cat = (str(li)[pos1:pos2])
        main_categories.append(cat)

for category in main_categories:
    import_all_products_infos_cat(category)
