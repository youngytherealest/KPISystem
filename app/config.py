from dotenv import load_dotenv
from pathlib import Path

import pyodbc
import os

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

server = os.getenv('SQL_HOST')
database = os.getenv('SQL_DATABASE')
username = os.getenv('SQL_USERNAME')
password = os.getenv('SQL_PASSWORD')

def create_connection():
    conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};CHARSET=UTF8')
    return conn