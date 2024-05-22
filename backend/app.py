from flask import Flask, jsonify, request
from flask_cors import CORS
import db_data

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "HELLO KITTY"

# kategoriju nosaukumi
@app.route('/category')
def get_category():
    category_data = db_data.fetch_category()
    return jsonify(category_data)

# produktu nosaukumi
@app.route('/category/products')
def get_products():
    category_name = request.args.get('category_name')
    # category_name = 'majai-darzam-un-atputai' #testesanai var pielikt vienu vertibu
    products_data = db_data.fetch_sub_category(category_name)
    return jsonify(products_data) 

# informacija par visiem atbilstosajiem produktiem
@app.route('/category/products/info')
def get_info():
    subcategory_name = request.args.get('subcategory_name')
    # subcategory_name = 'taviem-svetkiem' #testesanai var pielikt vienu vertibu
    sort_type = request.args.get('sort_type') #ŠIS VĒL NEKO NEDARA
    print("WHAT IS: ", sort_type)
    product_info_data = db_data.fetch_sub_category_info(subcategory_name, sort_type)
    return jsonify(product_info_data)

# sub sub category uzskaitijums, ja ir
@app.route('/category/sub_category/sub_sub_category')
def get_sub_sub_categories():
    subcategory_name = request.args.get('subcategory_name')
    # subcategory_name = 'augli-un-ogas' #testesanai var pielikt vienu vertibu
    sub_sub_category_data = db_data.fetch_sub_sub_category(subcategory_name)
    return jsonify(sub_sub_category_data)

# informacija par visiem sub sub produktiem, ja ir
@app.route('/category/sub_category/sub_sub_category/info')
def get_sub_sub_category_info():
    subcategory_name = request.args.get('subcategory_name')
    subsubcategory_name = request.args.get('subsubcategory_name')
    sort_type = request.args.get('sort_type')
    # subcategory_name = 'augli-un-ogas' #testesanai var pielikt vienu vertibu
    # subsubcategory_name = 'eksotiskie-augli' #testesanai var pielikt vienu vertibu
    sub_sub_category_data = db_data.fetch_sub_sub_category_info(subcategory_name, subsubcategory_name, sort_type)
    return jsonify(sub_sub_category_data)

if __name__ == '__main__':
    app.run(debug=True)
