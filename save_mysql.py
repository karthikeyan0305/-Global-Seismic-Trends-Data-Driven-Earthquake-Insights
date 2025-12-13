# save_mysql.py
from sqlalchemy import create_engine, text
from config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB, TABLE_NAME
import pandas as pd

def get_engine():
    url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    engine = create_engine(url)
    return engine

def save_dataframe(df):
    """
    Save DataFrame to MySQL table. Creates db/table if not exists (simple approach).
    """
    engine = get_engine()
    # to_sql will create table if not exists; use if_exists='replace' or 'append' as needed
    df.to_sql(TABLE_NAME, engine, if_exists="replace", index=False, chunksize=1000)
    return True
