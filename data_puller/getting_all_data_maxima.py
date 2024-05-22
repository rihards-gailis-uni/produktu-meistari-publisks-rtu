import re
import os
import time
import datetime

from bs4 import BeautifulSoup
from requests_html import HTMLSession

####################

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
current_working_dir = os.getcwd()

####################

current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
filename = f"complete_data_maxima_{formatted_time}.txt"

with open(filename, "w") as file:
    file.write("")

filename_faulty = f"faulty_products_maxima_{formatted_time}.txt"

with open(filename_faulty, "w") as file:
    file.write("")

####################

with open("sitemap_maxima.txt", "r", encoding="utf-8") as f:
    data = f.readlines()

# delteting \n and removing irrelevent links
category_links = []

for i in data:

    i = i.strip()

    if i.split("/")[3] not in ("produkti", "veikali", "ieteikumi", "mani-dati", "meklet", "jaunumi", "eko", "paldies-cena", "akcijas", "#") and len(i.split("/")) > 5:  
        
        category_links.append(i)

session = HTMLSession()

for base_url  in category_links:

    page_number = 1

    while True:

        url = f"{base_url}?page={page_number}"

        # calling different category links
        headers = {
            "contact" : "jautajumu gadijuma kontakteties - karlis.kaugars@edu.rtu.lv, rihards.ievins@edu.rtu.lv, ralfs.rengitis@edu.rtu.lv vai rihards.gailis@edu.rtu.lv"
        }

        # because page is using JavaScript to populate HTML elements we are using HTMLSession library
        response = session.get(url)
        response.html.render(timeout=50)
        html_content = response.html.html
        soup = BeautifulSoup(html_content, "html.parser")

        ul_element = soup.find('ul', class_="tw-mx-0 tw-p-0 tw-mt-4 tw-mb-4 md:tw-mb-5 tw-grid tw-grid-cols-2 tw-gap-2 tw-justify-items-center md:tw-gap-4 md:tw-grid-cols-4")

        if ul_element.text == "":
            break

        # getting page list of products
        li_elements = ul_element.find_all('li')

        for li in li_elements:

            try:

                one_product = {}

                a_tags = li.find_all('a')
                
                # primary details about one product
                for a in a_tags:

                    one_product["retail_store"] = "maxima"
                    one_product["link_name"] = a.get('href').split("/")[2]

                    if a.find("span") is not None:
                        one_product["name"] = a.find("span").text

                    if "https://www.barbora.lv" + a.get('href'):
                        one_product["link"] = "https://www.barbora.lv" + a.get('href')

                    img_tag = a.find("img")
                    if img_tag:
                        one_product["image"] = img_tag['src']

                # situation if product is unavailable

                if li.find('div', class_ = "tw-px-2 tw-pb-1 tw-text-center tw-text-b-paragraph-sm lg:tw-text-b-paragraph-base"):
                    if li.find('div', class_ = "tw-px-2 tw-pb-1 tw-text-center tw-text-b-paragraph-sm lg:tw-text-b-paragraph-base").text == "Atvainojiet, šobrīd prece nav pieejama.":

                        one_product["price_regular"] = None
                        one_product["price_in"] = None
                        one_product["measurment"] = None
                        print(one_product)

                        with open(filename, "a", encoding="utf-8") as f:
                            f.write(f"{one_product}\n")

                        continue

                # discounted products
                if li.find('div', class_ = "tw-flex tw-flex-shrink-0 tw-flex-row tw-mr-1") is not None:

                    #one_product["price_regular"] = ''.join(span.text for span in li.find('div', class_ = "tw-flex tw-flex-shrink-0 tw-flex-row tw-mr-1").find_all('span'))
                    one_product["price_regular"] = li.find('span', class_="tw-text-b-paragraph-xs tw-font-bold tw-text-gray-400 lg:tw-text-b-paragraph-sm").text.replace(",", ".")

                    match = re.search(r"(\d+,\d+)(€/[a-zA-Z]+)", ''.join(span.text for span in li.find('div', class_="tw-flex tw-flex-shrink-0 tw-flex-row").find_all('span')))
                    if match:
                        one_product["price_in"] = match.group(1).replace(",", ".")
                        one_product["measurment"] = "not_applicable"
                        one_product["measurment_in"] = match.group(2)

                    # situation with a regular discount
                    if li.find('div', class_ = "tw-flex tw-items-center tw-justify-center tw-rounded-product-card-label tw-border-[2px] tw-border-r-0 tw-border-solid tw-pl-1 tw-text-white tw-text-b-paragraph-xs lg:tw-text-b-paragraph-sm tw-h-[24px] tw-bg-b-red-500 lg:tw-h-[28px]") is not None:
                        
                        one_product["price_regular_with_discount"] = li.find('span', class_="tw-mr-0.5 tw-text-b-price-sm tw-font-semibold lg:tw-text-b-price-xl").text + "." + li.find('span', class_="tw-text-b-price-xs tw-font-semibold lg:tw-text-b-price-lg").text
                        
                        match = re.search(r"(\d+,\d+)(€/[a-zA-Z]+)", str(li.find('span', class_="tw-text-b-paragraph-xs tw-text-gray-400 lg:tw-text-b-paragraph-sm").text))
                        if match:
                            one_product["price_in_with_discount"] = match.group(1).replace(",", ".")

                    # situation if product has a discount with the retail store discount card
                    else:
                        
                        one_product["price_regular_with_discount_card"] = li.find('span', class_="tw-mr-0.5 tw-text-b-price-sm tw-font-semibold lg:tw-text-b-price-xl").text + "." + li.find('span', class_="tw-text-b-price-xs tw-font-semibold lg:tw-text-b-price-lg").text

                        match = re.search(r"(\d+,\d+)(€/[a-zA-Z]+)", str(li.find('span', class_="tw-text-b-paragraph-xs tw-text-gray-400 lg:tw-text-b-paragraph-sm").text))
                        if match:
                            one_product["price_in_with_discount_card"] = match.group(1).replace(",", ".")

                # regular products without the discount
                else:

                    one_product["price_regular"] = li.find('span', class_="tw-mr-0.5 tw-text-b-price-sm tw-font-semibold lg:tw-text-b-price-xl").text + "." + li.find('span', class_="tw-text-b-price-xs tw-font-semibold lg:tw-text-b-price-lg").text

                    match = re.search(r"(\d+,\d+)(€/[a-zA-Z]+)", str(li.find('span', class_="tw-text-b-paragraph-xs tw-text-gray-400 lg:tw-text-b-paragraph-sm").text))
                    if match:
                        one_product["price_in"] = match.group(1).replace(",", ".")
                        one_product["measurment"] = "not_applicable"
                        one_product["measurment_in"] = match.group(2)

                print(one_product)

                with open(filename, "a", encoding="utf-8") as f:
                    f.write(f"{one_product}\n")

            except:

                with open(filename_faulty, "a", encoding="utf-8") as f:
                    f.write(f"{one_product}\n")

        page_number += 1
        
session.close()
