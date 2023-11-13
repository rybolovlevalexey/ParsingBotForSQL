import telebot
import peewee as pw
import pandas as pd
import pyodbc
import tempfile


db = pw.SqliteDatabase("db.sqlite3")
bot = telebot.TeleBot(open("bot info.txt").readlines()[0].strip())


@bot.message_handler(commands=["start"])
def start_message(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Бот начал работу")


@bot.message_handler(commands=["add_new_brand"])
def add_new_brand(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Введите название автомобильной марки")


@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    print("Получена информация о новом файле")
    file_path = file_info.file_path
    downloaded_file = bot.download_file(file_path)
    print("Файл скачан в бинарном виде с серверов telegram")
    if file_path.endswith(".xlsb") or file_path.endswith(".xlsx") or file_path.endswith(".xls"):
        # excel file
        df = pd.read_excel(downloaded_file)
        print("Файл обработан успешно")
        for index, row in df.iterrows():
            article = row["PART_NO"].strip()
            name = row["PART_NAME_RUS"].strip()
            purchase_price = row["D_ORDER_DNP"].strip()
            retail_price = row["LIST_PRICE"].strip()
            print(article, name, purchase_price, retail_price, sep="; ")
            break
    elif file_path.endswith(".mdb") or file_path.endswith(".accdb"):
        # access file
        suf = ".mdb" if file_path.endswith(".mdb") else ".accdb"
        temp_file = tempfile.NamedTemporaryFile(suffix=suf, delete=False)
        temp_file.write(downloaded_file)
        temp_file.close()

        conn_str = (
                r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                r'DBQ=' + temp_file.name + ';'
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        tables = [table_info.table_name for table_info in cursor.tables(tableType='TABLE')]
        if len(tables) == 1:
            query = 'SELECT * FROM ' + tables[0]
            df = pd.read_sql(query, conn)
            print("ok")
            conn.close()
            temp_file.close()
        else:
            print("Передан файл с некорректным количеством таблиц")
    else:
        print("Прислан файл неверного расширения")


if __name__ == "__main__":
    bot.polling(none_stop=True)
