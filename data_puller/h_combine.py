import json
import re
from fuzzywuzzy import fuzz

def normalize_product_name(name):

    name = name.lower()
    name = re.sub(r'[^a-z0-9\s]', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    tokens = name.split()
    tokens.sort()

    return ' '.join(tokens)

# read and normalize data
def read_and_normalize(filepath):

    with open(filepath, "r", encoding="utf-8") as f:
        products = [line.strip() for line in f.readlines()]

    normalized_products = {prod: normalize_product_name(prod) for prod in products}

    print(f"finished reading and normalizing data from {filepath}")

    return normalized_products

# find all potential matches and their scores
def find_all_matches(maxima, rimi):

    match_scores = []
    maxima_count = len(maxima)

    print("starting")

    for i, (maxima_prod, maxima_norm) in enumerate(maxima.items(), 1):

        for rimi_prod, rimi_norm in rimi.items():

            score = fuzz.token_sort_ratio(maxima_norm, rimi_norm)
            match_scores.append((maxima_prod, rimi_prod, score))

        if i % 10 == 0 or i == maxima_count:  

            print(f"processed {i} of {maxima_count} maxima products for matching.")

    return sorted(match_scores, key = lambda x : x[2], reverse=True)

# match_scores = find_all_matches(normalized_maxima_products, normalized_rimi_products)

# assign matches based on the highest score
def assign_best_matches(match_scores):

    maxima_locked = set()
    rimi_locked = set()
    final_matches = []
    total_matches = len(match_scores)

    print("assigning best matches")

    for index, (maxima_prod, rimi_prod, score) in enumerate(match_scores, 1):

        if maxima_prod not in maxima_locked and rimi_prod not in rimi_locked:

            final_matches.append((maxima_prod, rimi_prod, score))
            maxima_locked.add(maxima_prod)
            rimi_locked.add(rimi_prod)

        if index % 100 == 0 or index == total_matches:  

            print(f"assigned {index} of {total_matches} matches.")

    return final_matches

def save_results(matches):

    results = {maxima: {'match': rimi, 'score': score} for maxima, rimi, score in matches}

    with open('unique_matching_results.json', 'w') as json_file:
        json.dump(results, json_file, indent=4)

    print("done")

################################

normalized_maxima_products = read_and_normalize("products_maxima.txt")

normalized_rimi_products = read_and_normalize("products_rimi.txt")

match_scores = find_all_matches(normalized_maxima_products, normalized_rimi_products)

final_matches = assign_best_matches(match_scores)

save_results(final_matches)
