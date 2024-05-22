import requests
import os
import re
import xml.etree.ElementTree as ET

####################

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
current_working_dir = os.getcwd()

####################

url_t = ["https://www.rimi.lv/e-veikals/sitemaps/products/siteMap_rimiLvSite_Product_lv_1.xml", "https://www.rimi.lv/e-veikals/sitemaps/products/siteMap_rimiLvSite_Product_lv_2.xml", "https://www.rimi.lv/e-veikals/sitemaps/products/siteMap_rimiLvSite_Product_lv_3.xml", "https://www.rimi.lv/e-veikals/sitemaps/products/siteMap_rimiLvSite_Product_lv_4.xml", "https://www.rimi.lv/e-veikals/sitemaps/products/siteMap_rimiLvSite_Product_lv_5.xml"]

headers = {
    "contact" : "jautajumu gadijuma kontakteties - karlis.kaugars@edu.rtu.lv, rihards.ievins@edu.rtu.lv, ralfs.rengitis@edu.rtu.lv vai rihards.gailis@edu.rtu.lv"
}

all_pages = []

for i in url_t:

    url = i

    response = requests.get(url, headers=headers)

    print(response.reason)

    tree = ET.fromstring(response.text)

    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    store_data = {}

    new_url_id_entries = []

    category_table_names = []

    for url_element in tree.findall('ns:url', namespace):
        
        loc_element = url_element.find('ns:loc', namespace).text

        match = re.search(r'/([^/]+)/p/', loc_element)
        if match:
            product_part = match.group(1)
            all_pages.append(product_part)

with open("products_rimi.txt", "w") as f:
    for line in all_pages:
        f.write(f"{line}\n")
