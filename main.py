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
    print("Получена информация о новом файле")
    file_path = file_info.file_path
    downloaded_file = bot.download_file(file_path)
    print("Файл скачан в бинарном виде с серверов telegram")
    df = pd.read_excel(downloaded_file)
    for index, row in df.iterrows():
        article = row["PART_NO"]
        name = row["PART_NAME_RUS"]
        purchase_price = row["D_ORDER_DNP"]
        retail_price = row["LIST_PRICE"]
        print(article, name, purchase_price, retail_price, sep="; ")
        break


if __name__ == "__main__":
    bot.polling(none_stop=True)
