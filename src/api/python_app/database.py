from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib
from os import getenv
from dotenv import load_dotenv

load_dotenv()
API_KEY = getenv("API_KEY")
API_KEY_NAME = "access_token"
password = getenv("MSSQL_PASSWORD")
server = getenv("MSSQL_SERVER")
database = getenv("MSSQL_DATABASE")
username = getenv("MSSQL_USERNAME")


driver = "{ODBC Driver 17 for SQL Server}"
conn = f"""Driver={driver};Server=tcp:{server},1433;Database={database};
Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"""
params = urllib.parse.quote_plus(conn)
conn_str = "mssql+pyodbc:///?autocommit=true&odbc_connect={}".format(params)
engine = create_engine(conn_str, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
