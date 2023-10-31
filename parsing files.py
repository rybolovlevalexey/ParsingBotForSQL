import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mssql+pyodbc:///?odbc_connect=%s' % (
    'Driver={Microsoft Access Driver (*.accdb)};'
    'Dbq=C:/TimetableParserBot_project/files with costs/Dealers price-list OEM 01.01.2023.accdb;'))

df = pd.read_sql_table("files with costs/Dealers price-list OEM 01.01.2023.accdb", engine)

engine = create_engine("mssql+pyodbc:///?odbc_connect='Driver={Microsoft Access Driver (*.accdb)};Dbq={your_db_path};Uid={your_user_name};Pwd={your_password}'")
df = pd.read_sql_query("SELECT * FROM my_table", engine)
print(df.head())
print(df.tail())