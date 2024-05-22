import pymysql

# Savienojums ar datu bāzi
def get_connection():
    return pymysql.connect(
        host='35.228.31.187',
        user='root',
        password='TcPeAyvVyX7vRxg!7NZ6X3AFAXQjfkaqdCLf',
        database='PRODUKTU_MEISTARI',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# Formatē tekstu no datu bāzes uz smukāku
def format(values):
    if not values:
        return []

    formatted_categories = []
    for category in values:
        key_to_use = None
        for possible_key in ['value', 'sub_category', 'sub_sub_category']:
            if possible_key in category:
                key_to_use = possible_key
                break

        if key_to_use is None:
            continue

        category_value = category.get(key_to_use)

        if category_value is None:
            return []

        formatted_value = category_value.replace('-', ' ').title()
        formatted_categories.append({
            key_to_use: category_value,
            'label': formatted_value
        })

    return formatted_categories

# Izpilda padoto vaicājumu un atgriež datus
def fetch_data(sql_query):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()
            return result
    except pymysql.MySQLError as e:
        print("Error while connecting to MySQL or executing SQL:", e)
    finally:
        conn.close()


# Iegūstam visas kategorijas
def fetch_category():
    sql = "SELECT * FROM category"
    categories = fetch_data(sql)
    return format(categories)

# Iegūstam visas apakškategorijas vajadzīgajai kategorijai
def fetch_sub_category(category_name):
    sql = f"SELECT sub_category FROM category_subcategory WHERE category = '{category_name}'"
    products = fetch_data(sql)
    return format(products)


def fetch_sub_category_info(sub_category_name, sort_type):
    sub_category_name = sub_category_name.replace('-', '_')
    print("KAS IR SEIT: ", sort_type)
    sql = f"SELECT * FROM `{sub_category_name}`"
    if sort_type:
        print("Izveletais tips sub kategorija: ", sort_type)
        if sort_type == "cenaAugosa":
            sql = f"SELECT * FROM `{sub_category_name}` ORDER BY price_regular ASC"
        elif sort_type == "cenaDilstosa":
            sql = f"SELECT * FROM `{sub_category_name}` ORDER BY price_regular DESC"
        elif sort_type == "cenaKgAugosa":
            sql = f"SELECT * FROM `{sub_category_name}` ORDER BY price_in ASC"
        elif sort_type == "cenaKgDilstosa":
            sql = f"SELECT * FROM `{sub_category_name}` ORDER BY price_in DESC"
        else:
            raise ValueError("Ja tu esi seit ticis, tad apsveicu tevi")
    product_info = fetch_data(sql)
    return product_info

def fetch_sub_sub_category(sub_category_name):
    sub_category_name = sub_category_name.replace('-', '_')
    sql = f"SELECT DISTINCT sub_sub_category FROM `{sub_category_name}`"
    sub_sub_categories = fetch_data(sql)
    return format(sub_sub_categories)

def fetch_sub_sub_category_info(sub_category_name, sub_sub_category_name, sort_type):
    sub_category_name = sub_category_name.replace('-', '_')
    sql = f"SELECT * FROM `{sub_category_name}` WHERE sub_sub_category = '{sub_sub_category_name}'"
    if sort_type:
        print("Izveletais tips sub sub kategorija: ", sort_type)
        if sort_type == "cenaAugosa":
            sql = f"SELECT * FROM `{sub_category_name}` WHERE sub_sub_category = '{sub_sub_category_name}' ORDER BY price_regular ASC"
        elif sort_type == "cenaDilstosa":
            sql = f"SELECT * FROM `{sub_category_name}` WHERE sub_sub_category = '{sub_sub_category_name}' ORDER BY price_regular DESC"
        elif sort_type == "cenaKgAugosa":
            sql = f"SELECT * FROM `{sub_category_name}` WHERE sub_sub_category = '{sub_sub_category_name}' ORDER BY price_in ASC"
        elif sort_type == "cenaKgDilstosa":
            sql = f"SELECT * FROM `{sub_category_name}` WHERE sub_sub_category = '{sub_sub_category_name}' ORDER BY price_in DESC"
        else:
            raise ValueError("Ja tu esi seit ticis, tad apsveicu tevi")
    sub_sub_category_info = fetch_data(sql)
    return sub_sub_category_info
