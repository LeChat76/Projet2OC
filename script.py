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

# product_page_url

# universal_product_code(upc)
upc = soup.find_all('td')
upc = (upc[0].string)
print("UPC : " + upc)

# title
Title = (soup.find_all("li", class_="active"))
Title = (Title[0].string) # pourquoi devoir faire ça?!? Titles.string ne fonctionne pas directement ???
print("Titre : " + Title)

# price_including_tax
pit = soup.find_all('td')
pit = (pit[3].string)
print("Price including tax : " + pit)

# price_excluding_tax
pet = soup.find_all('td')
pet = (pet[2].string)
print("Price excluding tax : " + pet)

# number_available
available = soup.find_all('td')
available = (available[5].string)
print(available)

# product_description
desc = soup.find("meta", attrs={"name":"description"})

# category

# review_rating

# mage_url




