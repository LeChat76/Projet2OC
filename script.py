############ Variables ############
'''
main_url = url main page of the site
main_page = content of the main page
main_categories[] = list of categories displayed in the main page
main_url_categories[] =  list of URLs associated of each main categories
category_page_url = URL of one category
products_url[] = list of products
product_url = URL of one book
list_products_url[] = list of products
product_page_url = URL of one book
'''

import csv
import requests
from bs4 import BeautifulSoup
import shutil

#####################################
########## Category choice ##########
#####################################

main_url = "http://books.toscrape.com/"
main_page = requests.get(main_url)

print("Requesting URL " + main_url)

if main_page.status_code != 200:
    print("Serveur injoignable")
    exit()
else:
    print("Acces serveur OK")

main_page_soup = BeautifulSoup(main_page.content, 'html.parser')

main_categories = []
main_url_categories =  []

main_li = main_page_soup.find_all("li")
for li in main_li:
    if "category" in str(li) and not "books_1" in str(li):
        # extraction of the category
        pos1 = str(li).find("                                ") + 32
        pos2 = str(li).find("\n", pos1)
        cat = (str(li)[pos1:pos2]).capitalize()
        main_categories.append(cat)
        # extraction of the URL of this category
        pos1 = str(li).find("href") + 6
        pos2 = str(li).find(".html") + 5
        url_cat = "http://books.toscrape.com/" + (str(li)[pos1:pos2])
        main_url_categories.append(url_cat)

cat_choice = ""
index = -1
while cat_choice.upper() != "S" and cat_choice.upper() != "T":
    index += 1
    cat_choice = input("Analyser categorie " + main_categories[index] + " ([ENTER] pour suivante, (s)electionner celle ci ou (t)outes)?")
    # if all categories listed, back to the first + warning
    if index == len(main_categories):
        print("\nVous avez fait le tour de toutes les categories, retour à la première!\n")
        index = -1

##################################################################
########## script of extraction of one or more products ##########
##################################################################

if cat_choice.upper() == "S":
    nb_cat = 1
else:
    nb_cat = len(main_categories)
    index = 0

for m in range(nb_cat):

    category_page_url = main_url_categories[index]

    page = requests.get(category_page_url)

    print("Requesting URL " + category_page_url)

    if page.status_code != 200:
        print("Serveur injoignable")
        exit()
    else:
        print("Acces serveur OK")

    soup = BeautifulSoup(page.content, 'html.parser')

    products_url = soup.find_all("h3")

    list_products_url = []
    for url in products_url:
        pos1 = str(url).find("../../") + 9
        pos2 = str(url).find("index.html", pos1)
        product_url = ("http://books.toscrape.com/catalogue/" + str(url)[pos1: pos2])
        list_products_url.append(product_url)

    ########## opening CSV file ##########

    try:
        test_opening_csv = open("book_to_scrape_" + main_categories[index] + ".csv","w")
    except IOError:
        print("\nErreur lors de la creation du fichier.\nEst il déjà ouvert? Avez vous les droits de création?")
        exit()

    header = ["product_page_url", "universal_product_code (upc)", "title", "price_including_tax", "price_excluding_tax",
              "number_available", "product_description", "category", "review_rating", "image_url"]

    with open("book_to_scrape_" + main_categories[index] + ".csv","w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(header)

        for product_page_url in list_products_url:

            page = requests.get(product_page_url)
            soup = BeautifulSoup(page.content, 'html.parser')

            ########## Data extraction ##########

            ## values in 'td' will be used 4 times
            ## so I declared "globally"
            ## [0] universal product code
            ## [2] price excluding tax
            ## [3] price including tax
            ## [5] number of books available
            td = soup.find_all("td")

            ## values for a href will be used twice
            ## so I declared "globally"
            ahref = soup.find_all("a")

            # product_page_url

            # universal_product_code(upc)
            universal_product_code = (td[0].string)

            # title
            ## title stored on the first class active found
            title = (soup.find("li", class_="active"))
            title = (title.string)

            # price_including_tax
            price_including_tax = (td[3].string)

            # price_excluding_tax
            price_excluding_tax = (td[2].string)

            # number_available
            number_available = (td[5].string)
            number_available = (number_available.replace("In stock (","")).replace(" available)", "")
            #number_available.replace(" available(", "")


            # product_description
            desc = soup.find("meta", attrs={"name":"description"})
            # ";" removing for opening CSV
            desc=(str(desc).replace("&quot;","")).replace(";",",")
            product_description=desc[20:-31]

            # category
            ## looking for "category/books/" on ahref list
            for cat in ahref:
                if "category/books/" in str(cat):
                    category = cat.string

            # review_rating
            review_rating = (td[6].string)

            # image_url
            ## find class item active (only one on all the html)
            ## and looking for img url by searching ../../ at the beginning and jpg at the end
            image = str(soup.find(class_="item active"))
            pos1 = image.find("../../") + 6
            pos2 = image.find("jpg",pos1) + 3
            image_url = ("http://books.toscrape.com/" + (image[pos1 : pos2]))

            # downloading image file
            img = requests.get(image_url, stream = True)
            title = title.replace(":"," ").replace("'"," ") # replace special caracters incompatible with name file
            image_ext = image_url[-4:] # to keep the same extension
            with open(title + image_ext, 'wb') as img_file:
                shutil.copyfileobj(img.raw, img_file)

            line=[product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url]
            writer.writerow(line)

        csv_file.close()

    index += 1

print("Fin de l'extraction, vous pouvez consulter les fichiers CSV")

