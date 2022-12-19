# -*- coding: utf-8 -*-

def import_all_products_infos_cat(main_categories):

    from script_ph1 import import_product_info
    import requests
    from bs4 import BeautifulSoup
    import datetime

    main_url = "http://books.toscrape.com/"
    main_page = requests.get(main_url)
    list_products_url = []
    next_category_page_url = ""
    # main_categories = "Women Fiction"
    now = datetime.datetime.now()
    date_time = now.strftime("%d%m%Y_%H%M%S")

    # print("Requesting URL " + main_url)
    '''
    if main_page.status_code != 200:
        print("Serveur injoignable")
        exit()
    else:
        print("Accès serveur OK")
    '''
    main_page_soup = BeautifulSoup(main_page.content, 'html.parser')

    main_li = main_page_soup.find_all("li")

    for li in main_li:
        if ("  " + main_categories) in str(li) and not "books_1" in str(li) and "category" in str(li):
            # extraction of the URL of this category
            pos1 = str(li).find("href") + 6
            pos2 = str(li).find(".html") + 5
            main_url_category = "http://books.toscrape.com/" + (str(li)[pos1:pos2])

    pages = 1

    page = requests.get(main_url_category)

    print("(ph2a) Requesting URL " + main_url_category)

    while page.status_code == 200:

        if next_category_page_url:
            print("(ph2b) Requesting URL " + next_category_page_url)

        if page.status_code != 200:
            print("Serveur injoignable")
            exit()
        else:
            print("Accès serveur OK")

        soup = BeautifulSoup(page.content, 'html.parser')

        products_url = soup.find_all("h3")

        # extraction of all products url
        for url in products_url:
            pos1 = str(url).find("../../") + 9
            pos2 = str(url).find("index.html", pos1)
            product_url = ("http://books.toscrape.com/catalogue/" + str(url)[pos1: pos2])
            list_products_url.append(product_url)

        # test if next page exists
        next_category_page_name = str(soup.find("li", class_="next"))
        if next_category_page_name != "None":
            pos1 = next_category_page_name.find("href=") + 6
            pos2 = next_category_page_name.find(">next") -1
            next_category_page_name = next_category_page_name[pos1:pos2]
            next_category_page_url = main_url_category.replace("index.html", next_category_page_name)
            page = requests.get(next_category_page_url)
        else:
            page.status_code = 404

    for product in list_products_url:
        import_product_info(product, main_categories, date_time)

    list_products_url.clear()
