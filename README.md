# Scraping of http://books.toscrape.com library shop
## _Project 2 OpenClassRooms_
This script download all data stored in "Books to Scrape" e-shope.
## Installation
```sh
"git clone https://github.com/LeChat76/Projet2OC.git"
"cd Projet2OC"
Create virtual environment :
* "python -m venv .env"
* activate environment :
    * for Linux "source .env/bin/activate"
    * for Windows ".\.env\Scripts\activate"
Install all needed libraries by typing : "pip install -r requirements.txt"
```
## Execution
```sh
Simply launch the script by typing "py script.py" and follow instruction :
* First : select all categories (t) or just one (s)
* Then : select to download images files or not (to exporte quickly)
```
## Features
- Select only one category or all
- All data extracted to data\CSVs's folder
- All book cover downloaded on each subfolder data\[category] and named by the name of the book (easy way to find the good one)
- timestamp of the extracted CSV in the file name (in that way by relaunching the script all olds
extractions are keeped in the folder)
- elapsed time displayed at the end of the script
## Features to come
 - Create an log file for each using
 - Create a progress bar (when launching all categories it takes some times so I think it will be good to see where we are in the execution of the script)
