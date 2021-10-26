import pandas as pd
from pymongo import MongoClient
# Load csv dataset
# data = pd.read_csv('Family expenses.csv')
from datetime import datetime
from io import DEFAULT_BUFFER_SIZE
import pandas as pd
import openpyxl
from sqlalchemy import create_engine

sourceFile="Family expenses.xlsm"

book = openpyxl.load_workbook(
    sourceFile, data_only=True, read_only=True
)
dfExpense = pd.read_excel(
    sourceFile,
    sheet_name="Expenses DB",
    skiprows=9,
    usecols="J,Q:U",
)

dfExpense["Amount"] *= -1
dfIncome.rename(columns={"Type ": "Category"}, inplace=True)




# Connect to MongoDB
client =  MongoClient("mongodb://sysadmin:syspassword@localhost:27017/expensedb")
db = client.get_default_database()
collection = db['expenses']
data.reset_index(inplace=True)
data_dict = data.to_dict("records")
# Insert collection
collection.insert_many(data_dict)