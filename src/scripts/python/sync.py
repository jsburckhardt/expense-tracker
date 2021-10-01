from datetime import datetime
from io import DEFAULT_BUFFER_SIZE
import pandas as pd
import openpyxl
from sqlalchemy import create_engine

sourceFile="Family expenses.xlsm"
outputFile="Family expenses.csv"
outputJSON="Family expenses.json"

book = openpyxl.load_workbook(
    sourceFile, data_only=True, read_only=True
)

dfExpense = pd.read_excel(
    sourceFile,
    sheet_name="Expenses DB",
    skiprows=9,
    usecols="J,Q:U",
)
dfIncome = pd.read_excel(
    sourceFile,
    sheet_name="Income DB",
    skiprows=9,
    usecols="J,Q:U",
)

dfExpense["Amount"] *= -1
dfIncome.rename(columns={"Type ": "Category"}, inplace=True)
dfIncome["Store"] = "NA"
dfIncome["Exclude in WE"] = "NA"
dfResult = dfExpense.append(dfIncome)
dfResult.sort_values(by="Date", inplace=True)
dfResult.rename(columns={"Exclude in WE": "ExcludeWE"}, inplace=True)
dfResult["Date"] = dfResult["Date"].dt.strftime("%Y-%m-%dT00:00:00.000Z")
dfResult["created_at"] = datetime.now().strftime("%Y-%m-%dT00:00:00.000Z")
dfResult["updated_at"] = datetime.now().strftime("%Y-%m-%dT00:00:00.000Z")
cols = [
    "Date",
    "created_at",
    "updated_at",
    "Store",
    "Category",
    "Amount",
    "ExcludeWE",
    "Description",
]
dfResult = dfResult[cols]
print(dfResult)
dfResult.to_csv(outputFile, index=False)


dfResult.to_json(path_or_buf=outputJSON, orient="records")


engine = create_engine(
    "sqlite:////home/ubuntu/repos/go/src/github.com/jsburckhardt/goexpenses/expenses.db",
    echo=False,
)
dfResult.to_sql("expenses", con=engine, if_exists="append", index=False)
