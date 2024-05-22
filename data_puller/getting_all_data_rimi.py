import re
import os
import time
import json
import requests
import datetime

from bs4 import BeautifulSoup
from urllib.parse import urlparse

####################

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
current_working_dir = os.getcwd()

####################

current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
filename = f"complete_data_rimi_{formatted_time}.txt"

with open(filename, "w") as file:
    file.write("")

####################

data = []
with open('sitemap_rimi.txt', 'r') as file:
    for line in file:
        json_object = json.loads(line)
        data.append(json_object)

# gettign the data
for category in data:

    page_number = 1

    while True:

        url = category.get("url")

        url = f"{url}?currentPage={page_number}&pageSize=80"

        # calling different category links
        headers = {
            "contact" : "jautajumu gadijuma kontakteties - karlis.kaugars@edu.rtu.lv, rihards.ievins@edu.rtu.lv, ralfs.rengitis@edu.rtu.lv vai rihards.gailis@edu.rtu.lv"
        }

        response = requests.get(url, headers=headers)
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")

        # getting error pages
        if soup.find("h1", class_ = "error-page__heading") is not None:
            with open("faulty_pages_rimi.txt", "a", encoding="utf-8") as f:
                f.write(f"{url}\n")
            break

        # getting page list of products
        li_elements = soup.find("ul", class_="product-grid").find_all("li")

        if li_elements == []:
            break

        for li in li_elements:

            one_product = {}

            a = li.find('a')

            # assign category depth levels
            if category.get('level_0') is not None:
                one_product['category'] = category.get('level_0')
            
            if category.get('level_1') is not None:
                one_product['sub_category'] = category.get('level_1')
            
            if category.get('level_2') is not None:
                one_product['sub_sub_category'] = category.get('level_2')

            # primary details about one product
            one_product["retail_store"] = "rimi"
            one_product["link_name"] = a.get('href').split("/")[len(a.get('href').split("/"))-3]
            one_product["link"] = "https://www.rimi.lv" + a.get('href')
            one_product["image"] = li.find('div', class_ = "card__image-wrapper").find("img")['src']
            one_product["name"] = li.find('div', class_ = "card__details").find('p', class_ = "card__name").text

            # situation if product is unavailable
            if li.find('p', class_ = "card__price-per").text.strip() == "Īslaicīgi nav pieejamas e-veikalā":

                one_product["price_regular"] = None
                one_product["price_in"] = None
                one_product["measurment"] = None
                one_product["measurment_in"] = None
                print(one_product)

                with open(filename, "a", encoding="utf-8") as f:
                    f.write(f"{one_product}\n")

                continue

            # situation if product has a regular discount
            if li.find('div', class_ = "card__price-wrapper -has-discount"):
                
                try:

                    one_product["price_regular"] = li.find('div', class_ = "old-price-tag card__old-price").find("span").text.replace("€", "").replace(",", ".")
            
                    price_regular_with_discount_temp = str(li.find('div', class_ = "price-tag card__price").find('span').text) + '.' + str(li.find('div', class_ = "price-tag card__price").find('div').find('sup').text)
                    match = re.search(r"\d+[,\.]\d+", li.find('p', class_ = "card__price-per").text)
                    if match:
                        price_in_with_discount_temp = match.group().replace(',', '.')

                    one_product["price_in"] = str(round(float(one_product["price_regular"]) * float(price_in_with_discount_temp) / float(price_regular_with_discount_temp), 2))
                    one_product["price_regular_with_discount"] = price_regular_with_discount_temp
                    one_product["price_in_with_discount"] = price_in_with_discount_temp

                    one_product["measurment"] = li.find('div', class_ = "price-tag card__price").find('div').find('sub').text.replace('.', '')
                    match = re.search(r"[^\d,\s]+", li.find('p', class_ = "card__price-per").text)
                    if match:
                        one_product["measurment_in"] = match.group().strip()  

                except:

                    with open("faulty_products_rimi.txt", "a", encoding="utf-8") as f:
                        f.write(f"{one_product}\n")
            
            # situation if product has not a regular discount
            else:

                one_product["price_regular"] = str(li.find('div', class_ = "price-tag card__price").find('span').text) + '.' + str(li.find('div', class_ = "price-tag card__price").find('div').find('sup').text)
                match = re.search(r"\d+[,\.]\d+", li.find('p', class_ = "card__price-per").text)
                if match:
                    one_product["price_in"] = match.group().replace(',', '.')

                one_product["measurment"] = li.find('div', class_ = "price-tag card__price").find('div').find('sub').text.replace('.', '')
                match = re.search(r"[^\d,\s]+", li.find('p', class_ = "card__price-per").text)
                if match:
                    one_product["measurment_in"] = match.group().strip()  

                # situation if product has a discount with the retail store discount card
                if li.find('div', class_ = "price-badge__price"):

                    one_product["price_regular_with_discount_card"] = '.'.join(span.text for span in li.find('div', class_ = "price-badge__price").find_all('span') if span.text.isdigit())
                    one_product["price_in_with_discount_card"] = str(round(float(one_product["price_regular_with_discount_card"]) * float(one_product["price_in"]) / float(one_product["price_regular"]), 2))
                    #one_product["measurment_with_discount"] = one_product["measurment"]

            print(one_product)

            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"{one_product}\n")

        page_number += 1
