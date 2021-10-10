from typing import List, Optional
from fastapi import Security, Depends, FastAPI, status, HTTPException
from fastapi.security.api_key import APIKeyHeader, APIKey
from datetime import date
from sqlalchemy.orm import Session
import models
import schemas
import crud
from database import SessionLocal, engine
from os import getenv
from dotenv import load_dotenv

models.Base.metadata.create_all(bind=engine)


load_dotenv()
API_KEY = getenv("API_KEY")
API_KEY_NAME = "access_token"

# Dependency
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


app = FastAPI()


@app.get("/")
async def root():
    return "Welcome world"


@app.post(
    "/api/v1/records",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.SchemaRecord,
    tags=["records"],
)
def create_record(
    record: schemas.SchemaRecord,
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(get_api_key),
):
    db_record = models.ModelsRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


@app.post(
    "/api/v1/records/multiple",
    status_code=status.HTTP_201_CREATED,
    response_model=List[schemas.SchemaRecord],
    tags=["records"],
)
def create_record(
    records: List[schemas.SchemaRecord],
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(get_api_key),
):
    list_of_records = []
    for record in records:
        list_of_records.append(models.ModelsRecord(**record.dict()))

    db.bulk_save_objects(list_of_records)
    return records


@app.get(
    "/api/v1/records",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.SchemaRecordReturn],
    tags=["records"],
)
def get_records(
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
    return crud.get_records(
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
    )


@app.delete(
    "/api/v1/records",
    status_code=status.HTTP_200_OK,
    # response_model=List[schemas.SchemaRecordReturn],
    tags=["records"],
)
def delete_records(
    db: Session = Depends(get_db),
    id: str = 0,
    api_key: APIKey = Depends(get_api_key),
):
    crud.delete_records(
        db,
        id,
    )
    return {}


# def create_record(
#     records: List[schemas.SchemaRecord],
#     db: Session = Depends(get_db),
#     api_key: APIKey = Depends(get_api_key),
# ):
#     list_of_records = []
#     for record in records:
#         list_of_records.append(models.ModelsRecord(**record.dict()))

#     db.bulk_save_objects(list_of_records)
#     return records


@app.get(
    "/api/v1/summary",
    status_code=status.HTTP_200_OK,
    # response_model=List[schemas.SchemaRecordReturn],
    tags=["summary"],
)
def get_summary(
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
    # income/outcome
    # perirod, daily/monthly/yearly
    api_key: APIKey = Depends(get_api_key),
):
    return crud.get_summary(
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
    )
