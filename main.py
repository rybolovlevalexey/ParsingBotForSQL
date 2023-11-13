import pandas as pd
import pyodbc
import tempfile

file_path = "files with costs/Dealers price-list OEM 01.01.2023.accdb"
with open(file_path, 'rb') as f:
    downloaded_file = f.read()

suf = ".mdb" if file_path.endswith(".mdb") else ".accdb"
temp_file = tempfile.NamedTemporaryFile(suffix=suf, delete=False)
temp_file.write(downloaded_file)
temp_file.close()
print("Создан временный файл")
conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=' + temp_file.name + ';'
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
tables = [table_info.table_name for table_info in cursor.tables(tableType='TABLE')]
if len(tables) == 1:
    print(tables[0])
    query = 'SELECT * FROM ' + tables[0]
    print("here")
    df = pd.read_sql(query, conn)
    print("ok")
    conn.close()
    temp_file.close()