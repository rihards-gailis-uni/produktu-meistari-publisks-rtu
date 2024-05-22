import pymysql
import json

def connect_to_database(host, user, password, database):

    return pymysql.connect(host=host, user=user, password=password, db=database)

def fetch_all_tables(cursor):

    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    return tables

def fetch_rows_from_table(cursor, table):

    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    return rows

def convert_row_to_json(row, column_names):

    return dict(zip(column_names, row))

def create_table(cursor, table_name):

    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (value VARCHAR(255))")

def insert_data_into_table(cursor, table_name, data):

    cursor.executemany(f"INSERT INTO {table_name} (value) VALUES (%s)", data)

#####################################

conn = connect_to_database('*****', '*****', '*****', '*****')
cursor = conn.cursor()

tables = fetch_all_tables(cursor)
all_rows = []

category = []
sub_category = []
sub_sub_category = [] 

for table in tables:

    cursor.execute(f"DESCRIBE {table}")
    column_names = [column[0] for column in cursor.fetchall()]
    rows = fetch_rows_from_table(cursor, table)

    for row in rows:

        row_json = convert_row_to_json(row, column_names)

        if row_json.get("category") not in category:
            category.append(row_json.get("category"))
        if row_json.get("sub_category") not in sub_category:
            sub_category.append(row_json.get("sub_category"))               
        if row_json.get("sub_sub_category") not in sub_sub_category:
            sub_sub_category.append(row_json.get("sub_sub_category"))

        print(row)

        all_rows.append(row_json)

print("done")

create_table(cursor, 'category')
create_table(cursor, 'sub_categories')
create_table(cursor, 'sub_sub_categories')

insert_data_into_table(cursor, 'category', [(item,) for item in category])
insert_data_into_table(cursor, 'sub_categories', [(item,) for item in sub_category])
insert_data_into_table(cursor, 'sub_sub_categories', [(item,) for item in sub_sub_category])

conn.commit() 

cursor.close()
conn.close()
