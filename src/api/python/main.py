# import os  # from os import getenv
from sqlalchemy.sql.expression import desc
from sqlalchemy.sql import text

# from sqlalchemy.sql.sqltypes import VARCHAR
from sqlalchemy_utils import UUIDType
from typing import List, Optional
from fastapi import Security, Depends, FastAPI, status, HTTPException
from fastapi.security.api_key import APIKeyHeader, APIKey
from pydantic import BaseModel
from datetime import date
from pydantic.types import UUID4
from sqlalchemy.orm import Session
import uuid
from uuid import uuid4
from os import getenv
from dotenv import load_dotenv

load_dotenv()
API_KEY = getenv("API_KEY")
API_KEY_NAME = "access_token"
password = getenv("MSSQL_PASSWORD")
server = getenv("MSSQL_SERVER")
database = getenv("MSSQL_DATABASE")
username = getenv("MSSQL_USERNAME")

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib

driver = "{ODBC Driver 17 for SQL Server}"
conn = f"""Driver={driver};Server=tcp:{server},1433;Database={database};
Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"""
params = urllib.parse.quote_plus(conn)
conn_str = "mssql+pyodbc:///?autocommit=true&odbc_connect={}".format(params)
engine = create_engine(conn_str, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
# FROM DATABASE.PY ############################

# FROM MODELS ---------######## FROM MODELS ---------######## FROM MODELS ---------#######
from sqlalchemy import Column
from sqlalchemy.dialects.mssql import VARCHAR, DATE, BIT, FLOAT


class ModelsRecord(Base):
    __tablename__ = "records"
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    created = Column(DATE, nullable=False)
    updated = Column(DATE, nullable=False)
    amount = Column(FLOAT, nullable=False)
    store = Column(VARCHAR, nullable=False)
    category = Column(VARCHAR, nullable=False)
    weeklyexpense = Column(BIT, nullable=False)
    description = Column(VARCHAR, nullable=False)


# FROM MODELS ---------#######
Base.metadata.create_all(bind=engine)


class SchemaRecord(BaseModel):
    created: date
    updated: date
    amount: float
    store: str
    category: str
    weeklyexpense: bool
    description: str

    class Config:
        orm_mode = True


class SchemaRecordReturn(BaseModel):
    id: str
    created: date
    updated: date
    amount: float
    store: str
    category: str
    weeklyexpense: bool
    description: str

    class Config:
        orm_mode = True


# dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )


# Start server
app = FastAPI()


@app.get("/")
async def root():
    return "Welcome world"


@app.get(
    "/api/v1/records",
    status_code=status.HTTP_200_OK,
    response_model=List[SchemaRecord],
)
def get_records(
    db: Session = Depends(get_db),
    page: int = 0,
    limit: int = 100,
    api_key: APIKey = Depends(get_api_key),
):

    return (
        db.query(ModelsRecord)
        .order_by((ModelsRecord.created).desc())
        .offset(page * limit)
        .limit(limit)
        .all()
    )


@app.post(
    "/api/v1/records",
    status_code=status.HTTP_201_CREATED,
    response_model=SchemaRecord,
)
def create_record(
    record: SchemaRecord,
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(get_api_key),
):
    db_record = ModelsRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


@app.post(
    "/api/v1/records/multiple",
    status_code=status.HTTP_201_CREATED,
    response_model=List[SchemaRecord],
)
def create_record(
    records: List[SchemaRecord],
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(get_api_key),
):
    list_of_records = []
    for record in records:
        list_of_records.append(ModelsRecord(**record.dict()))

    db.bulk_save_objects(list_of_records)
    return records


@app.get(
    "/api/v1/something",
    status_code=status.HTTP_200_OK,
    response_model=List[SchemaRecordReturn],
)
def get_records_again(
    db: Session = Depends(get_db),
    page: int = 0,
    limit: int = 100,
    from_created_date: Optional[date] = None,
    to_created_date: Optional[date] = None,
    from_amount: Optional[float] = None,
    to_amount: Optional[float] = None,
    stores: Optional[str] = None,
    categories: Optional[str] = None,
    weekly_expenses: Optional[bool] = None,
    api_key: APIKey = Depends(get_api_key),
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
    for record in records:
        temp_record = SchemaRecordReturn(
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
