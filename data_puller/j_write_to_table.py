import pymysql
import json
from collections import defaultdict
import os

def load_json_data(filepath):

    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def connect_to_database(host, user, password, database):

    return pymysql.connect(host=host, user=user, password=password, db=database)

def create_database_tables(cursor, data, all_columns):

    categories = set()
    
    for entry in data:
        category_key = entry['sub_category']
        categories.add(category_key)

    for category in categories:

        table_name = f"{category}".replace("-", "_").replace(" ", "_")
        columns = [col for col in all_columns if col != 'measurment_with_discount']
        column_definitions = ', '.join([f"`{column}` VARCHAR(255)" for column in columns])
        create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({column_definitions});"
        cursor.execute(create_table_query)

def insert_data_into_tables(conn, cursor, data, all_columns):
    for entry in data:
        category_key = entry['sub_category']
        table_name = f"{category_key}".replace("-", "_").replace(" ", "_")
        columns = [col for col in all_columns if col != 'measurment_with_discount']
        placeholders = ', '.join(['%s' for _ in columns])
        insert_query = f"INSERT INTO `{table_name}` ({', '.join([f'`{column}`' for column in columns])}) VALUES ({placeholders});"

        print(table_name)

        rows = [tuple(entry.get(column, None) for column in columns)]
        cursor.executemany(insert_query, rows)
        conn.commit()

if __name__ == '__main__':

    data = load_json_data('updated_maxima_products.json')

    conn = connect_to_database('*****', '*****', '*****', '*****')

    cursor = conn.cursor()

    all_columns = {
        'category', 'sub_category', 'sub_sub_category', 'retail_store', 'link_name', 'link', 'image',
        'name', 'price_regular', 'price_in', 'price_regular_with_discount', 'price_in_with_discount',
        'price_regular_with_discount_card', 'price_in_with_discount_card', 'measurment', 'measurment_in'
    }

    create_database_tables(cursor, data, all_columns)

    insert_data_into_tables(conn, cursor, data, all_columns)

    cursor.close()
    conn.close()