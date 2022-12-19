from script_ph1 import import_product_info
from script_ph2 import import_all_products_infos_cat
from script_ph3 import import_all_products
from script_ph4 import download_img_product

#import_product_info("http://books.toscrape.com/catalogue/shtum_733/index.html", "Fiction", "1708")
#import_all_products_infos_cat("Fiction")
import_all_products("http://books.toscrape.com/")
#download_img_product("http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html", "its only Himalaya", "Travel")