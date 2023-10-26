import openpyxl
import io
import telebot
import peewee as pw
import pandas as pd


db = pw.SqliteDatabase("db.sqlite3")  # база данных с пользователями и ссылками на группы
bot = telebot.TeleBot(open("bot info.txt").readlines()[0].strip())


@bot.message_handler(commands=["start"])
def start_message(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Бот начал работу")


@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    file_path = file_info.file_path
    downloaded_file = bot.download_file(file_path)

    # Сохранение файла на диск
    file = open("bin_file", "wb")
    file.write(downloaded_file)

    func1()


def func(file_name: str):
    f = open("bin_file", "rb")
    binary_data = f.read()
    bytes_io = io.BytesIO(binary_data)

    workbook = openpyxl.load_workbook(bytes_io)
    workbook.save(file_name)


def func1():
    # Открытие бинарного файла и чтение его содержимого
    with open("bin_file", 'rb') as f:
        binary_data = f.read()

    # Преобразование бинарных данных в объект BytesIO
    bytes_io = io.BytesIO(binary_data)

    # Чтение данных из Excel файла в DataFrame
    df = pd.read_excel(bytes_io)

    # Сохранение DataFrame в Excel файл
    df.to_excel("excel_file.xlsb", index=False)


if __name__ == "__main__":
    bot.polling(none_stop=True)
