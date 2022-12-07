import requests
from bs4 import BeautifulSoup

## URL=input("Wich URL to scrap ? : [ENTER = http://books.toscrape.com/]")
# note pour plus tard : gérer les exceptions
## if URL == "":
##     URL ="http://books.toscrape.com/"

URL ="http://books.toscrape.com/"

page = requests.get(URL)

print("Requesting URL " + URL)

if page.status_code != 200:
    print("Unable to access to the server, please check URL")
    exit()
else:
    print("Server access OK")

soup = BeautifulSoup(page.content, 'html.parser')

# Data extraction

Title = soup.title.string
