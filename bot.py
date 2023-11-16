import telebot
import pandas as pd
import pyodbc
import tempfile
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from main import BRANDS
from database_actions import loading_new_handler_numbers

bot = telebot.TeleBot(open("bot info.txt").readlines()[0].strip())
flag_add_new_brand = False
new_brand_info = dict()


@bot.message_handler(commands=["start"])
def start_message(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Бот начал работу")


@bot.message_handler(commands=["add_new_brand"])
def add_new_brand(message: telebot.types.Message):
    global flag_add_new_brand
    global new_brand_info
    flag_add_new_brand = True
    new_brand_info = dict()
    markup = InlineKeyboardMarkup()
    for i in range(0, len(BRANDS), 4):
        if i + 2 == len(BRANDS):
            markup.row(InlineKeyboardButton(text=BRANDS[i], callback_data=BRANDS[i]),
                       InlineKeyboardButton(text=BRANDS[i + 1], callback_data=BRANDS[i + 1]))
        elif i + 1 == len(BRANDS):
            markup.row(InlineKeyboardButton(text=BRANDS[i], callback_data=BRANDS[i]))
        elif i + 3 == len(BRANDS):
            markup.row(InlineKeyboardButton(text=BRANDS[i], callback_data=BRANDS[i]),
                       InlineKeyboardButton(text=BRANDS[i + 1], callback_data=BRANDS[i + 1]),
                       InlineKeyboardButton(text=BRANDS[i + 2], callback_data=BRANDS[i + 2]))
        else:
            markup.row(InlineKeyboardButton(text=BRANDS[i], callback_data=BRANDS[i]),
                       InlineKeyboardButton(text=BRANDS[i + 1], callback_data=BRANDS[i + 1]),
                       InlineKeyboardButton(text=BRANDS[i + 2], callback_data=BRANDS[i + 2]),
                       InlineKeyboardButton(text=BRANDS[i + 3], callback_data=BRANDS[i + 3]))
    bot.send_message(message.chat.id, "Выберите название автомобильной марки",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: flag_add_new_brand and len(new_brand_info) == 0)
def getting_brand_name(callback: telebot.types.CallbackQuery):
    brand_name = callback.data
    new_brand_info["brand_name"] = brand_name
    bot.send_message(callback.message.chat.id,
                     "Сейчас вам будет направлено несколько сообщений, на которые необходимо "
                     "ответить числом, показывающим номер столбца с указанными в сообщении данными."
                     " Нумерация начинается с единицы. Если столбцы с указанной информацией "
                     "отсутствуют в данных файлах введите -1.")
    bot.send_message(callback.message.chat.id, "Введите номер столбца, в котором  находится "
                                               "информация об артикуле в файлах данной марки.")


@bot.message_handler(func=lambda mes: mes.text.isdigit and flag_add_new_brand and
                                      len(new_brand_info) == 1)
def getting_article_number(message: telebot.types.Message):
    article_number = message.text
    new_brand_info["article_number"] = article_number
    bot.send_message(message.chat.id, "Введите номер столбца, в котором "
                                      "находится информация о наименовании в файлах данной марки.")


@bot.message_handler(func=lambda mes: mes.text.isdigit and flag_add_new_brand and
                                      len(new_brand_info) == 2)
def getting_part_name_number(message: telebot.types.Message):
    part_name_number = message.text
    new_brand_info["part_name_number"] = part_name_number
    bot.send_message(message.chat.id, "Введите номер столбца, в котором находится информация "
                                      "о закупочной цене в файлах данной марки.")


@bot.message_handler(func=lambda mes: mes.text.isdigit and flag_add_new_brand and
                                      len(new_brand_info) == 3)
def getting_purchase_price_number(message: telebot.types.Message):
    purchase_price_number = message.text
    new_brand_info["purchase_price_number"] = purchase_price_number
    bot.send_message(message.chat.id, "Введите номер столбца, в котором находится информация "
                                      "о розничной цене в файлах данной марки.")


@bot.message_handler(func=lambda mes: mes.text.isdigit and flag_add_new_brand and
                                      len(new_brand_info) == 4)
def getting_retail_price_number(message: telebot.types.Message):
    retail_price_number = message.text
    new_brand_info["retail_price_number"] = retail_price_number
    bot.send_message(message.chat.id, "Введите номер столбца, в котором находится информация "
                                      "о рекомендованной розничной цене в файлах данной марки.")


@bot.message_handler(func=lambda mes: mes.text.isdigit and flag_add_new_brand and
                                      len(new_brand_info) == 5)
def getting_recommended_retail_price_number(message: telebot.types.Message):
    global new_brand_info
    recommended_retail_price_number = message.text
    new_brand_info["recommended_retail_price_number"] = recommended_retail_price_number
    bot.send_message(message.chat.id, "Заполнение информации для обработчика данной марки окончено,"
                                      " спасибо за уделённое время")
    loading_new_handler_numbers(new_brand_info)

    global flag_add_new_brand
    flag_add_new_brand = False
    new_brand_info = dict()


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
