import json
import re
import os 

####################

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
current_working_dir = os.getcwd()

####################

def load_json_lines(file_path):

    data = []

    with open(file_path, 'r', encoding='utf-8') as file:

        line_number = 0

        for line in file:

            line_number += 1

            corrected_line = re.sub(r"(\s*?{\s*?|\s*?,\s*?)(\w+)(\s*?:)", r'\1"\2"\3', line.strip().replace("'", '"'))
            
            if corrected_line: 
                data.append(json.loads(corrected_line))

    return data

def load_json(file_path):

    with open(file_path, 'r', encoding='utf-8') as file:

        return json.load(file)

def save_json(data, file_path):

    with open(file_path, 'w', encoding='utf-8') as file:

        json.dump(data, file, indent=4)

def append_category_data(maxima_products, rimi_products, mappings):

    rimi_index = {product['link_name']: product for product in rimi_products}

    updated_maxima = []

    for maxima_product in maxima_products:

        maxima_link_name = maxima_product['link_name']

        if maxima_link_name in mappings and mappings[maxima_link_name].get('match') in rimi_index:

            rimi_match_name = mappings[maxima_link_name]['match']
            rimi_product = rimi_index.get(rimi_match_name)

            if rimi_product:

                maxima_product['category'] = rimi_product.get('category')
                maxima_product['sub_category'] = rimi_product.get('sub_category')

                if 'sub_sub_category' in rimi_product:
                
                    maxima_product['sub_sub_category'] = rimi_product.get('sub_sub_category')

                updated_maxima.append(maxima_product)

    return updated_maxima

if __name__ == "__main__":
    
    maxima_products = load_json_lines('complete_data_maxima_2024-05-03_16-14-38.txt')
    rimi_products = load_json_lines('complete_data_rimi_2024-05-02_20-03-47.txt')
    mappings = load_json('matching_results.json')  

    updated_maxima_products = append_category_data(maxima_products, rimi_products, mappings)

    save_json(updated_maxima_products, 'updated_maxima_products.json')
