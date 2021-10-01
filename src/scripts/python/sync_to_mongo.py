import pandas as pd
from pymongo import MongoClient
# Load csv dataset
data = pd.read_csv('Family expenses.csv')
# Connect to MongoDB
client =  MongoClient("mongodb://127.0.0.1:27017/expensedb")
db = client.get_default_database()
collection = db['expenses']
data.reset_index(inplace=True)
data_dict = data.to_dict("records")
# Insert collection
collection.insert_many(data_dict)