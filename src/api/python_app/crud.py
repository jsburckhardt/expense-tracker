from typing import Optional
from pandas.io import json
from sqlalchemy.orm import Session
from datetime import date
import schemas
import pandas as pd
import json


def get_records(
    db: Session,
    page: int,
    limit: int,
    from_created_date: Optional[date] = None,
    to_created_date: Optional[date] = None,
    from_amount: Optional[float] = None,
    to_amount: Optional[float] = None,
    stores: Optional[str] = None,
    categories: Optional[str] = None,
    weekly_expenses: Optional[bool] = None,
    df: Optional[bool] = False,
):
    statement = "SELECT * FROM records WHERE 1 = 1"
    count_statement = (
        "SELECT COUNT(*) AS records_count FROM records WHERE 1 = 1"
    )
    params = {}
    results = []

    if from_created_date != None:
        statement += " and created >= :from_created_date"
        count_statement += " and created >= :from_created_date"
        params["from_created_date"] = from_created_date

    if to_created_date != None:
        statement += " and created < :to_created_date"
        count_statement += " and created < :to_created_date"
        params["to_created_date"] = to_created_date

    if from_amount != None:
        statement += " and amount >= :from_amount"
        count_statement += " and amount >= :from_amount"
        params["from_amount"] = from_amount

    if to_amount != None:
        statement += " and amount < :to_amount"
        count_statement += " and amount < :to_amount"
        params["to_amount"] = to_amount

    if stores != None:
        query_parameters = {}
        counter = 1
        stores_array = stores.split(",")
        for store in stores_array:
            query_parameters["store" + str(counter)] = store
            counter += 1

        statement += (
            " and store IN(:" + ",:".join(query_parameters.keys()) + ")"
        )
        count_statement += (
            " and store IN(:" + ",:".join(query_parameters.keys()) + ")"
        )
        params.update(query_parameters)

    if categories != None:
        query_parameters = {}
        counter = 1
        categories_array = categories.split(",")
        for category in categories_array:
            query_parameters["category" + str(counter)] = category
            counter += 1

        statement += (
            " and category IN(:" + ",:".join(query_parameters.keys()) + ")"
        )
        count_statement += (
            " and category IN(:" + ",:".join(query_parameters.keys()) + ")"
        )
        params.update(query_parameters)

    if weekly_expenses != None:
        statement += " and weeklyexpense = :weekly_expense"
        count_statement += " and weeklyexpense = :weekly_expense"
        if weekly_expenses:
            params["weekly_expense"] = 1
        else:
            params["weekly_expense"] = 0

    # add the pagination and order
    statement += " ORDER BY created DESC OFFSET :offset rows fetch next :limit rows only"
    params["offset"] = page * limit
    params["limit"] = limit

    records = db.execute(statement, params)
    if df:
        return records
    for record in records:
        temp_record = schemas.SchemaRecordReturn(
            id=record[0],
            created=record[1],
            updated=record[2],
            amount=record[3],
            store=record[4],
            category=record[5],
            weeklyexpense=record[6],
            description=record[7],
        )
        results.append(temp_record)
    return results


def delete_records(db: Session, id: str):
    statement = "DELETE FROM records WHERE id = :id"
    params = {}
    params["id"] = id
    return db.execute(statement, params)


def get_summary(
    db: Session,
    page: int,
    limit: int,
    from_created_date: Optional[date] = None,
    to_created_date: Optional[date] = None,
    from_amount: Optional[float] = None,
    to_amount: Optional[float] = None,
    stores: Optional[str] = None,
    categories: Optional[str] = None,
    weekly_expenses: Optional[bool] = None,
):
    records = get_records(
        db,
        page,
        limit,
        from_created_date,
        to_created_date,
        from_amount,
        to_amount,
        stores,
        categories,
        weekly_expenses,
        df=True,
    )
    cols = [
        "id",
        "created",
        "updated",
        "amount",
        "store",
        "category",
        "weeklyexpense",
        "description",
    ]

    df = pd.DataFrame(records.all(), columns=cols)
    dfs = df[["created", "amount"]]
    return dfs.groupby("created").sum().to_dict()


def get_categories(
    db: Session,
    page: int,
    limit: int,
):
    statement = "SELECT * FROM categories WHERE 1 = 1"
    count_statement = (
        "SELECT COUNT(*) AS categories_count FROM categories WHERE 1 = 1"
    )
    params = {}
    results = []

    statement += " ORDER BY categoryName OFFSET :offset rows fetch next :limit rows only"
    params["offset"] = page * limit
    params["limit"] = limit

    categories = db.execute(statement, params)

    for category in categories:
        results.append(category["categoryName"])

    return results


def get_stores(
    db: Session,
    page: int,
    limit: int,
):
    statement = "SELECT * FROM stores WHERE 1 = 1"
    count_statement = "SELECT COUNT(*) AS stores_count FROM stores WHERE 1 = 1"
    params = {}
    results = []

    statement += (
        " ORDER BY storeName OFFSET :offset rows fetch next :limit rows only"
    )
    params["offset"] = page * limit
    params["limit"] = limit

    stores = db.execute(statement, params)

    for store in stores:
        results.append(store["storeName"])

    return results
