import csv
import requests
from bs4 import BeautifulSoup

## product_page_url=input("Wich URL to scrap ? : [ENTER] = http://books.toscrape.com/catalogue/set-me-free_988/]")
## if product_page_url == "":
##     product_page_url ="http://books.toscrape.com/catalogue/set-me-free_988/"
product_page_url ="http://books.toscrape.com/catalogue/set-me-free_988/"

page = requests.get(product_page_url)

print("Requesting URL " + product_page_url)

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
print("Product page URL : " + product_page_url)

# universal_product_code(upc)
universal_product_code = (td[0].string)
print("UPC : " + universal_product_code)

# title
## title stored on the first class active found
title = (soup.find("li", class_="active"))
title = (title.string)
print("Title : " + title)

# price_including_tax
price_including_tax = (td[3].string)
print("Price including tax : " + price_including_tax)

# price_excluding_tax
price_excluding_tax = (td[2].string)
print("Price excluding tax : " + price_excluding_tax)

# number_available
number_available = (td[5].string)
print("Number available : " + number_available)

# product_description
desc = str(soup.find("meta", attrs={"name":"description"}))
product_description=desc[20:-31]
print("Description : " + product_description)

# category
## looking for "category/books/" on ahref list
for cat in ahref:
    if "category/books/" in str(cat):
        category = cat.string
        print("Category : " + category)

# review_rating
review_rating = (td[6].string)
print("Review rating : " + review_rating)

# image_url
## find class item active (only one on all the html)
## and looking for img url by searching ../../ at the beginning and jpg at the end
image = str(soup.find(class_="item active"))
pos1 = image.find("../../") + 6
pos2 = image.find("jpg",pos1) + 3
image_url = ("http://books.toscrape.com/" + (image[pos1 : pos2]))
print("Image URL : " + image_url)

########## Creation of the CSV file ##########

header = ["product_page_url","universal_ product_code (upc)","title","price_including_tax","price_excluding_tax","number_available","product_description","category","review_rating","image_url"]

with open("book_to_scrape.csv","w", newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(header)
    line=[product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url]
    writer.writerow(line)
    writer.writerow(line)