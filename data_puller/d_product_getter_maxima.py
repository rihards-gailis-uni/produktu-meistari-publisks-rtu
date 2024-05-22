import requests
import os
import re
import xml.etree.ElementTree as ET

####################

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
current_working_dir = os.getcwd()

####################

url_t = ["http://www.barbora.lv/sitemap-1.xml", "http://www.barbora.lv/sitemap-2.xml"]

headers = {
    "contact" : "jautajumu gadijuma kontakteties - karlis.kaugars@edu.rtu.lv, rihards.ievins@edu.rtu.lv, ralfs.rengitis@edu.rtu.lv vai rihards.gailis@edu.rtu.lv"
}

all_pages = []

for i in url_t:

    url = i

    response = requests.get(url, headers=headers)

    print(response.reason)

    content = response.content.decode('utf-8-sig').strip()

    tree = ET.fromstring(content)

    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    for url_element in tree.findall('ns:url', namespace):
    
        loc_element = url_element.find('ns:loc', namespace).text

        if loc_element.split("/")[3] == "produkti":  
            all_pages.append(loc_element.split("/")[4])

with open("products_rimi22.txt", "w") as f:
    for line in all_pages:
        f.write(f"{line}\n")