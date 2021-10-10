# from typing import List, Optional
from pydantic import BaseModel
from datetime import date


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
