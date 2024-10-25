import xml.etree.ElementTree as ET
from pymongo import MongoClient
from datetime import datetime
import schedule
import time
import sys

# MongoDB setup
if len(sys.argv) > 1:
    file_path = sys.argv[1]
    mongodb_uri = sys.argv[2]
    client = MongoClient(mongodb_uri)

    try:
        client = MongoClient(mongodb_uri)
        # Attempt to access the database to check the connection
        client.admin.command('ping')  # This will raise an exception if the connection fails
        print("MongoDB connection successful.")
    except Exception as e:
        print(f"MongoDB connection string is not valid: {e}")
        print("Exitting...")
        sys.exit(1)  # exits the script if connection with the db fails
else:
    print("Mongodb connection string must be provided.")
    print("Exitting...")
    sys.exit(1)  # executes the script if conn string is not provided
    
db = client['product_database']
collection = db['products']

def parse_xml_to_dict(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    products = []
    
    for product in root.findall("Product"):
        product_data = {
            "stock_code": product.get("ProductId").lower(),
            "name": product.get("Name").capitalize(),
            "images": [image.get("Path") for image in product.find("Images")],
            "price": float(product.find("ProductDetails/ProductDetail[@Name='Price']").get("Value").replace(",", ".")),
            "discounted_price": float(product.find("ProductDetails/ProductDetail[@Name='DiscountedPrice']").get("Value").replace(",", ".")),
            "is_discounted": product.find("ProductDetails/ProductDetail[@Name='Price']").get("Value") != product.find("ProductDetails/ProductDetail[@Name='DiscountedPrice']").get("Value"),
            "product_type": product.find("ProductDetails/ProductDetail[@Name='ProductType']").get("Value"),
            "quantity": int(product.find("ProductDetails/ProductDetail[@Name='Quantity']").get("Value")),
            "color": [product.find("ProductDetails/ProductDetail[@Name='Color']").get("Value").capitalize()],
            "series": product.find("ProductDetails/ProductDetail[@Name='Series']").get("Value"),
            "season": product.find("ProductDetails/ProductDetail[@Name='Season']").get("Value"),
            "description": product.find("Description").text,
            "createdAt": datetime.now(),
            "updatedAt": datetime.now(),
        }
        products.append(product_data)
    print("Done with the parsing.")
    return products

def save_to_mongodb(products):
    for product in products:
        existing_product = collection.find_one({"stock_code": product["stock_code"]})
        if existing_product:
            collection.update_one({"_id": existing_product["_id"]}, {"$set": product})
        else:
            collection.insert_one(product)

def process_products(file_path):
    products = parse_xml_to_dict(file_path)
    save_to_mongodb(products)
    print("Saved to the database.")

schedule.every(1).hour.do(process_products)  # Schedule the task to run periodically

if __name__ == "__main__":
    process_products(file_path)
    while True:
        schedule.run_pending()
        time.sleep(1)
