import pandas as pd
import pymongo
from urllib.parse import quote_plus
from extract import fetch_stock_data
import certifi

password = "Paulpogba6@"
encoded_password = quote_plus(password)

mongo_url = f"mongodb+srv://kiplangat_db_user:{encoded_password}@cluster0.rowy3ve.mongodb.net/?appName=Cluster0"
db_name = "stock_data_db"
collection_name = "stock_prices"

client = pymongo.MongoClient(mongo_url, tlsCAFile=certifi.where())
db = client[db_name]
collection = db[collection_name]


def load_to_mongo():
    df = fetch_stock_data()
    if not df.empty:
        records = df.to_dict(orient='records')
        collection.insert_many(records)
        print(f"Loaded {len(records)} records into MongoDB")
        
    else:
        print("No data to load into MongoDB")
        
if __name__ == "__main__":
    load_to_mongo()
  
