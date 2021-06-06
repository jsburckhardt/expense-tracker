import pandas as pd
import openpyxl

# import excel
# import datetime as dt

book = openpyxl.load_workbook(
    "familyExpenses.xlsm", data_only=True, read_only=True
)

dfExpense = pd.read_excel(
    "familyExpenses.xlsm",
    sheet_name="Expenses DB",
    skiprows=9,
    usecols="J,Q:U",
)
dfIncome = pd.read_excel(
    "familyExpenses.xlsm",
    sheet_name="Income DB",
    skiprows=9,
    usecols="J,Q:U",
)

dfExpense["Amount"] *= -1
dfIncome.rename(columns={"Type ": "Category"}, inplace=True)
dfResult = dfExpense.append(dfIncome)
dfResult.sort_values(by="Date", inplace=True)
dfResult.rename(columns={"Exclude in WE": "ExcludeWE"}, inplace=True)
print(dfResult)
dfResult.to_csv(r"familyExpense.csv", index=False)
