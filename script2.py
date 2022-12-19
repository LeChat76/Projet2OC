from script_ph2 import import_all_products_cat
from script_ph3 import import_all_products

import requests
from bs4 import BeautifulSoup
import datetime

main_url = "http://books.toscrape.com/"
main_page = requests.get(main_url)

print("Analyse des catégories sur l'url " + main_url)

if main_page.status_code != 200:
    print("Serveur injoignable")
    exit()
else:
    print("Accès serveur OK")

main_page_soup = BeautifulSoup(main_page.content, 'html.parser')

main_categories = []
main_url_categories = []

main_li = main_page_soup.find_all("li")
for li in main_li:
    if "category" in str(li) and not "books_1" in str(li):
        # extraction of the category
        pos1 = str(li).find("                                ") + 32
        pos2 = str(li).find("\n", pos1)
        cat = (str(li)[pos1:pos2])
        main_categories.append(cat)

img_download = " "
cat_choice = ""
index = -1
while cat_choice.upper() != "S" and cat_choice.upper() != "T":
    index += 1
    cat_choice = input("Analyser catégorie " + main_categories[index] + " ([ENTER] pour suivante, (s)electionner celle ci ou (t)outes)?")
    # if all categories listed, back to the first + warning
    if index + 1 == len(main_categories):
        print("\nVous avez fait le tour de toutes les categories, retour à la première!\n")
        index = -1

while img_download.upper() != "Y" and img_download.upper() != "N" and img_download != "":
    img_download = input("Télécharger les images? (Y/n) ")
    if img_download == "":
        img_download = "Y"

now_begin = datetime.datetime.now()
if cat_choice.upper() == "S":
    import_all_products_cat(main_categories[index], img_download)
    now_end = datetime.datetime.now()
    now_delta = now_end - now_begin
    print("Fin de l'extraction, vous pouvez consulter le fichiers CSV horodaté à la date du jour dans le dossier \Data\CSVs.")
    if img_download.upper() == "Y":
        print("Les images de couvertures sont enregistrées dans le dossier Data" + "\\" + main_categories[index] + ".")
    print("\nTemps de traitement : " + str(now_delta)[:7])

elif cat_choice.upper() == "T":
    import_all_products(main_url, img_download)
    now_end = datetime.datetime.now()
    now_delta = now_end - now_begin
    print("Fin de l'extraction, vous pouvez consulter les fichiers CSVs horodatés à la date du jour dans le dossier \Data\CSVs.")
    if img_download.upper() == "Y":
        print("Les images de couvertures sont enregistrées dans chaque dossiers nommés de leurs catégories.")
    print("\nTemps de traitement : " + str(now_delta)[:7])
