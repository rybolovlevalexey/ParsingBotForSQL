import pandas as pd
import pyodbc
import tempfile
import pyperclip


def func_test_access():
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


BRANDS = sorted(['Terios', 'Great Wall', 'Nissan', 'KIA', 'Subaru', 'BYD', 'KJ',
                 'Марка не опознана',
                 'MOSKVICH', 'Suzuki', 'SOLLERS', 'Ssang yong', 'Прицеп', 'CHEVROLET',
                 'UAZ', 'Мотоцикл', 'INFINITI', 'Skoda', 'BMW', 'HARLEY DAVIDSON',
                 'МОСКВИЧ', 'RENAULT', 'HONDA', 'FORD', 'CHANGAN', 'MITSUBISHI',
                 'Tesla', 'Катер', 'CHRYSLER', 'Audi', 'DAEWOO', 'Ferrari', 'DODGE',
                 'GAC', 'Fiat', 'CHERY', 'LIFAN', 'HAVAL', 'ГАЗ', 'ZAZ', 'SKODA', 'Citroen',
                 'HYUNDAI',
                 'Lexus', 'JEEP', 'LADA', 'Daihatsu', 'OPEL', 'OMODA', 'Maserati', 'KAIYI', 'ВАЗ',
                 'MERCEDES-BENZ', 'Datsun', 'УАЗ', 'MAZDA', 'JETOUR', 'HUSQVARNA',
                 'Mercedes', 'ЗАЗ', 'Zeekr', 'RENO', 'АФ', 'GENESIS',
                 'MINI COOPER', 'RAVON', 'Volkswagen', 'JAGUAR', 'VOGE', 'Volga', 'TOYOTA', 'Seat',
                 'GEELY', 'Volvo', 'Land Rover', 'CADILLAC', 'ГАС', 'JAECOO', 'Vortex',
                 'КВАДРОЦИКЛ', 'Bentley', 'KTM', 'JETTA', 'Peugeot', 'Avatr', 'Porsche', 'Alfa'])

QUESTIONS_SYSTEM = {
    "start": "QUES_SYS{0};",
    1: {"text": "Данный файл подходит под шаблон бренда {0}. Указанный файл от этого бренда?",
        "answers": ["Да", "Нет"]},
    2: {},
    3: {}
}
