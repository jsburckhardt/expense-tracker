from sqlalchemy import Column
from sqlalchemy.dialects.mssql import VARCHAR, DATE, BIT, FLOAT
from sqlalchemy_utils import UUIDType
import uuid

# from .database import Base
from database import Base


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
