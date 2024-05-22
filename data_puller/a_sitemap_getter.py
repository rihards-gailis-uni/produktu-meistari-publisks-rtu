import re
import os
import json
import requests
import xml.etree.ElementTree as ET

from urllib.parse import urlparse

####################

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
current_working_dir = os.getcwd()

####################


def sitemap_rimi():

    sitemap = "https://www.rimi.lv/e-veikals/sitemap.xml"

    headers = {
        "contact" : "jautajumu gadijuma kontakteties - karlis.kaugars@edu.rtu.lv, rihards.ievins@edu.rtu.lv, ralfs.rengitis@edu.rtu.lv vai rihards.gailis@edu.rtu.lv"
    }

    response = requests.get(url=sitemap, headers=headers)

    if response.status_code == 200:
            ns = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            root = ET.fromstring(response.content)

            category_lv_urls = []

            for url in root.findall('.//sitemap:loc', namespaces=ns):
                if 'Category_lv' in url.text:
                    category_lv_urls.append(url.text)
    else:
        raise Exception (f"error in getting sitemap from {sitemap}")
    
    ###

    urls = []

    for sitemap in category_lv_urls:
         
        response = requests.get(url=sitemap, headers=headers)

        if response.status_code == 200:
                
                ns = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
                root = ET.fromstring(response.content)

                for url in root.findall('.//sitemap:loc', namespaces=ns):

                    url = url.text
                    url = url.strip()

                    if url and url != "https://www.rimi.lv/e-veikals/lv" and url != "https://www.rimi.lv/e-veikals/lv/produkti/c/SH":

                        parsed_url = urlparse(url)
                        path_segments = parsed_url.path.split('/')
                        
                        categories = [
                            segment for segment in path_segments
                            if segment and segment not in ('e-veikals', 'lv', 'produkti', 'c')
                        ]

                        categories = [
                            segment for segment in categories
                            if not re.match(r"^SH-\d+(-\d+)*$", segment)
                        ]

                        if categories:
                            category_map = {f"level_{index}": category for index, category in enumerate(categories)}
                            category_map["url"] = url
                            urls.append(category_map)
                        
        else:
            raise Exception (f"error in getting sitemap from {sitemap}")
    
    ###

    seen_categories = set()
    filtered_categories = []

    for ordered_list in sorted(urls, key=lambda x: len(x), reverse=True):

        category_levels = []
        for i in range(3):
            key = 'level_' + str(i)
            if key in ordered_list:
                category_levels.append(ordered_list.get(key))
        category_levels = tuple(category_levels)
        
        if category_levels not in seen_categories:

            seen_categories.add(category_levels)
            url = ordered_list.get('url')
            
            modified_url = re.sub(r'(\d+)-(\d+)-(\d+)-\d+$', r'\1-\2-\3', url)

            ordered_list['url'] = modified_url
            
            filtered_categories.append(ordered_list)

            for i in range(1, len(category_levels) + 1):

                seen_categories.add(category_levels[:i])

    return filtered_categories

###########################################################################

def sitemap_maxima():
     
    sitemap = "https://www.barbora.lv/sitemap.xml"

    headers = {
        "contact" : "jautajumu gadijuma kontakteties - karlis.kaugars@edu.rtu.lv, rihards.ievins@edu.rtu.lv, ralfs.rengitis@edu.rtu.lv vai rihards.gailis@edu.rtu.lv"
    }

    response = requests.get(url=sitemap, headers=headers)

    if response.status_code == 200:
            ns = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            root = ET.fromstring(response.content)

            sitemap_urls = []

            for url in root.findall('.//sitemap:loc', namespaces=ns):
                sitemap_urls.append(url.text)
    else:
        raise Exception (f"error in getting sitemap from {sitemap}")
    
    ###

    urls = []

    for sitemap in sitemap_urls:
         
        response = requests.get(url=sitemap, headers=headers)

        if response.status_code == 200:
                ns = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
                root = ET.fromstring(response.content)

                for url in root.findall('.//sitemap:loc', namespaces=ns):
                    if url.text.split("/")[3] not in ("produkti", "veikali", "ieteikumi", "mani-dati", "meklet", "jaunumi", "eko", "paldies-cena", "akcijas", "#") and len(url.text.split("/")) > 5:
                        urls.append(url.text)

        else:
            raise Exception (f"error in getting sitemap from {sitemap}")
        
    return urls
        
rimi_sites = sitemap_rimi()

with open("sitemap_rimi.txt", 'w') as file:
    for site in rimi_sites:
        json.dump(site, file)
        file.write('\n') 

maxima_sites = sitemap_maxima()

with open("sitemap_maxima.txt", 'w') as file:
    for url in maxima_sites:
        file.write(url + '\n')