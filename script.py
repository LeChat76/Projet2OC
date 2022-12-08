import requests
from bs4 import BeautifulSoup

## URL=input("Wich URL to scrap ? : [ENTER] = http://books.toscrape.com/catalogue/set-me-free_988/]")
## if URL == "":
##     URL ="http://books.toscrape.com/catalogue/set-me-free_988/"
URL ="http://books.toscrape.com/catalogue/set-me-free_988/"

page = requests.get(URL)

print("Requesting URL " + URL)

if page.status_code != 200:
    print("Unable to access to the server, please check URL")
    exit()
else:
    print("Server access OK")

soup = BeautifulSoup(page.content, 'html.parser')

########## Data extraction ##########

## values in 'td' will be used 4 times
## so I declared "globally"
## [0] universal product code
## [2] price excluding tax
## [3] price including tax
## [5] number of books available
td = soup.find_all('td')

## values for a href will be used 2 times
## so I declared "globally"
ahref = soup.find_all("a")




# product_page_url
print("Product page URL : " + URL)

# universal_product_code(upc)
upc = (td[0].string)
print("UPC : " + upc)

# title
## title stored on the first class active found
title = (soup.find("li", class_="active"))
title = (title.string)
print("Title : " + title)

# price_including_tax
pit = (td[3].string)
print("Price including tax : " + pit)

# price_excluding_tax
pet = (td[2].string)
print("Price excluding tax : " + pet)

# number_available
available = (td[5].string)
print("Number available : " + available)

# product_description
desc = str(soup.find("meta", attrs={"name":"description"}))
desc=desc[20:-31]
print("Description : " + desc)

# category
## looking for "category/books/" on ahref list
for cat in ahref:
    if "category/books/" in str(cat):
        cat = cat.string
        print("Category : " + cat)

# review_rating
rating = (td[6].string)
print("Review rating : " + rating)

# image_url
## find class item active (only one on all the html)
## and looking for img url by searching ../../ at the beginning and jpg at the end
image = str(soup.find(class_="item active"))
pos1 = image.find("../../") + 6
pos2 = image.find("jpg",pos1) + 3
subString = ("http://books.toscrape.com/" + (image[pos1 : pos2]))
print("Image URL : " + subString)

