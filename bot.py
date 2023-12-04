import telebot
import pandas as pd
import pyodbc
import tempfile
from typing import Union
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from main import BRANDS, QUESTIONS_SYSTEM
from database_actions import loading_new_handler_numbers, check_current_document, \
    loading_new_handler_templates, get_all_handlers_names, check_new_brand_name
from parsing_files import parsing
import urllib3
import asyncio
from telethon import TelegramClient

bot = telebot.TeleBot(open("bot info.txt").readlines()[0].strip())
flag_add_new_brand: bool = False
flag_add_new_brand_plus: bool = False
new_brand_info: dict[str, str] = dict()
new_brand_info_plus: dict[str, str] = dict()
current_DF: Union[pd.DataFrame, None] = None
columns_available_choose: list[str] = list()
first_line_keys: list[str] = list()
first_line_values: list[str] = list()


def make_output_with_first_line():
    keys: list[str] = first_line_keys
    values: list[str] = first_line_values
    output, ind = "", 0
    for key in keys:
        elem = values[key]
        output += keys[ind] + "-" * 5
        output += str(elem) + "\n"
        ind += 1
    return output


def make_markup_for_info_plus() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    for i in range(0, len(columns_available_choose) // 2):
        text1 = columns_available_choose[2 * i]
        text2 = columns_available_choose[2 * i + 1]
        markup.row(InlineKeyboardButton(text=text1, callback_data=text1),
                   InlineKeyboardButton(text=text2, callback_data=text2))
    if len(columns_available_choose) % 2 != 0:
        markup.add(InlineKeyboardButton(text=columns_available_choose[-1],
                                        callback_data=columns_available_choose[-1]))
    return markup


@bot.message_handler(commands=["start"])
def start_message(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Отправьте прайс-лист боту")


# начало добавления обработчика для нового бренда
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


# получение названия бренда, для которого создаётся обработчик
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


# получение номера столбца с артиклем детали
@bot.message_handler(func=lambda mes: mes.text.isdigit and flag_add_new_brand and
                                      len(new_brand_info) == 1)
def getting_article_number(message: telebot.types.Message):
    article_number = message.text
    new_brand_info["article_number"] = article_number
    bot.send_message(message.chat.id, "Введите номер столбца, в котором "
                                      "находится информация о наименовании в файлах данной марки.")


# получение номера столбца с названием детали
@bot.message_handler(func=lambda mes: mes.text.isdigit and flag_add_new_brand and
                                      len(new_brand_info) == 2)
def getting_part_name_number(message: telebot.types.Message):
    part_name_number = message.text
    new_brand_info["part_name_number"] = part_name_number
    bot.send_message(message.chat.id, "Введите номер столбца, в котором находится информация "
                                      "о закупочной цене в файлах данной марки.")


# получение номера столбца с оптовой ценой детали
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


# получение номера столбца с рекомендованной розничной ценой
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
def handle_document(message: telebot.types.Message):
    file_info = bot.get_file(message.document.file_id)
    print("Получена информация о новом файле")
    file_path = file_info.file_path
    bot.send_message(message.chat.id, "Файл получен, сейчас начнётся его обработка, это может "
                                      "занять некоторое время.")
    downloaded_file = bot.download_file(file_path)
    print("Файл скачан в бинарном виде с серверов telegram")
    df = None
    if file_path.lower().endswith(".xlsb") or file_path.lower().endswith(".xlsx") or \
            file_path.lower().endswith(".xls"):
        # excel file
        df = pd.read_excel(downloaded_file)
        print("Файл обработан успешно")
    elif file_path.lower().endswith(".mdb") or file_path.lower().endswith(".accdb"):
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
        bot.send_message(message.chat.id, "Прислан файл неверного расширения")
        return 0
    if df is None:
        return 0

    checking_result = check_current_document(df)  # проверка - есть ли этот файл в шаблонах
    if not checking_result:
        markup1 = InlineKeyboardMarkup()
        sp = get_all_handlers_names()
        st = "Бренд для файла:"
        if len(sp) % 2 != 0:
            markup1.row(InlineKeyboardButton(text=sp[0], callback_data=st + sp[0]))
            del sp[0]
        for ind in range(0, len(sp), 2):
            markup1.row(InlineKeyboardButton(text=sp[ind], callback_data=st + sp[ind]),
                        InlineKeyboardButton(text=sp[ind + 1], callback_data=st + sp[ind + 1]))
        markup1.row(InlineKeyboardButton(text="Добавить новый обработчик",
                                         callback_data="Добавить новый обработчик"))
        bot.send_message(message.chat.id, "Не найдено шаблонов, под которые мог бы подойти данный"
                                          " файл. Выберите бренд вручную или добавьте новый "
                                          "обработчик.", reply_markup=markup1)
    else:
        markup2 = InlineKeyboardMarkup()
        st1 = QUESTIONS_SYSTEM["start"].format("1") + checking_result
        st2 = QUESTIONS_SYSTEM["start"].format("1") + QUESTIONS_SYSTEM[1]["answers"][1]
        markup2.row(InlineKeyboardButton(text=QUESTIONS_SYSTEM[1]["answers"][0],
                                         callback_data=st1),  # да
                    InlineKeyboardButton(text=QUESTIONS_SYSTEM[1]["answers"][1],
                                         callback_data=st2))  # нет
        bot.send_message(message.chat.id, QUESTIONS_SYSTEM[1]["text"].format(checking_result),
                         reply_markup=markup2)
    global current_DF
    current_DF = df


# пользователь прислал файл, автоматическое определение шаблона сработало верно
@bot.callback_query_handler(func=lambda callback:
                            callback.data.startswith(QUESTIONS_SYSTEM["start"].format("1")) and
                            not callback.data.endswith(QUESTIONS_SYSTEM[1]["answers"][1]))
def template_was_founded(callback: telebot.types.CallbackQuery):
    bot.send_message(callback.message.chat.id, f"Обработка и загрузка информации в базу данных "
                                               f"файла от бренда {callback.data.split(';')[1]} "
                                               f"запущена.")
    asyncio.run(parsing(current_DF, callback.data.split(";")[1]))


# пользователь прислал файл, но найденный шаблон оказался неверным
@bot.callback_query_handler(func=lambda callback:
                            callback.data.startswith(QUESTIONS_SYSTEM["start"].format("1")) and
                            callback.data.endswith(QUESTIONS_SYSTEM[1]["answers"][1]))
def founded_template_incorrect(callback: telebot.types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    sp = get_all_handlers_names()
    st = "Бренд для файла:"
    if len(sp) % 2 != 0:
        markup.row(InlineKeyboardButton(text=sp[0], callback_data=st + sp[0]))
        del sp[0]
    for ind in range(0, len(sp), 2):
        markup.row(InlineKeyboardButton(text=sp[ind], callback_data=st + sp[ind]),
                   InlineKeyboardButton(text=sp[ind + 1], callback_data=st + sp[ind + 1]))
    markup.row(InlineKeyboardButton(text="Добавить новый обработчик",
                                    callback_data="Добавить новый обработчик"))
    bot.send_message(callback.message.chat.id,
                     "Найденный автоматически шаблон оказался неверным. Выберите бренд "
                     "вручную или добавьте новый обработчик.", reply_markup=markup)


# пользователь прислал файл, но под него не было найдено шаблонов: пользователь выбирает сделать
# новый обработчик или выбрать уже созданный вручную
@bot.callback_query_handler(func=lambda callback: callback.data == "Добавить новый обработчик" or
                                                  callback.data.startswith("Бренд для файла:"))
def manually_selecting_brand_or_adding_new(callback: telebot.types.CallbackQuery):
    if callback.data == "Добавить новый обработчик":
        # для отправленного файла нет созданных обработчиков
        global columns_available_choose  # столбцы, которые можно выбрать
        columns_available_choose = current_DF.columns.values.tolist()
        columns_available_choose.append("Отсутствует")
        global first_line_keys, first_line_values
        first_line_keys = list(list(current_DF.iterrows())[0][1].keys())
        first_line_values = list(current_DF.iterrows())[0][1]
        bot.send_message(callback.message.chat.id,
                         f"Введите <b>'название бренда'</b>, для которого добавляется обработчик.",
                         parse_mode="html")
        global flag_add_new_brand_plus
        flag_add_new_brand_plus = True
    elif callback.data.startswith("Бренд для файла:"):
        # пользователь выбрал бренд, файл которого он отправил
        brand_name = callback.data.split(":")
        bot.send_message(callback.message.chat.id, f"Обработка и загрузка информации в базу данных "
                                                   f"файла от бренда {brand_name[1]} "
                                                   f"запущена.")
        asyncio.run(parsing(current_DF, brand_name[1]))


# получение названия бренда, для которого создаётся обработчик
@bot.message_handler(func=lambda mes: flag_add_new_brand_plus and len(new_brand_info_plus) == 0)
def getting_brand_name_plus(message: telebot.types.Message):
    brand_name = message.text
    if check_new_brand_name(brand_name):
        new_brand_info_plus["brand_name"] = brand_name
        bot.send_message(message.chat.id, "Название бренда введено корректно, сейчас вам будет "
                                          "предоставлена информация о названиях столбцов в "
                                          "отправленном вами файле, а также об информации в первой "
                                          "строке. На основе этих вводных вам необходимо будет "
                                          "ответить на несколько вопросов с возможностью "
                                          "выбора ответа.")
        mark = make_markup_for_info_plus()
        output = make_output_with_first_line()
        bot.send_message(message.chat.id, "Выберите столбец, в котором находится информация об "
                         "<b>'артикле товара'</b>.\n\n" + output,
                         reply_markup=mark, parse_mode="html")
    else:
        bot.send_message(message.chat.id, "Такое название бренда уже занято, "
                                          "попробуйте использовать другое.")


@bot.callback_query_handler(func=lambda cal: flag_add_new_brand_plus and
                                             len(new_brand_info_plus) == 1)
def getting_article_plus(callback: telebot.types.CallbackQuery):
    column_article = callback.data
    new_brand_info_plus["article"] = column_article
    if column_article != "Отсутствует":
        columns_available_choose.remove(column_article)
        first_line_keys.remove(column_article)
    mark = make_markup_for_info_plus()
    bot.send_message(callback.message.chat.id,
                     "Выберите столбец, в котором находится информация о <b>'наименовании товара'"
                     "</b>.\n\n" + make_output_with_first_line(),
                     reply_markup=mark, parse_mode="HTML")


@bot.callback_query_handler(func=lambda cal: flag_add_new_brand_plus and
                                             len(new_brand_info_plus) == 2)
def getting_part_name_plus(callback: telebot.types.CallbackQuery):
    column_part_name = callback.data
    new_brand_info_plus["part_name"] = column_part_name
    if column_part_name != "Отсутствует":
        columns_available_choose.remove(column_part_name)
        first_line_keys.remove(column_part_name)
    mark = make_markup_for_info_plus()
    bot.send_message(callback.message.chat.id, f"Выберите столбец, в котором находится информация "
                     f"об <b>'оптовой цене товара'</b>.\n\n{make_output_with_first_line()}",
                     reply_markup=mark, parse_mode="HTML")


@bot.callback_query_handler(func=lambda cal: flag_add_new_brand_plus and
                                             len(new_brand_info_plus) == 3)
def getting_purchase_price_plus(callback: telebot.types.CallbackQuery):
    column_purchase_price = callback.data
    new_brand_info_plus["purchase_price"] = column_purchase_price
    if column_purchase_price != "Отсутствует":
        columns_available_choose.remove(column_purchase_price)
        first_line_keys.remove(column_purchase_price)
    mark = make_markup_for_info_plus()
    bot.send_message(callback.message.chat.id, f"Выберите столбец, в котором находится информация "
                     f"о <b>'розничной цене товара'</b>.\n\n{make_output_with_first_line()}",
                     reply_markup=mark, parse_mode="HTML")


@bot.callback_query_handler(func=lambda cal: flag_add_new_brand_plus and
                                             len(new_brand_info_plus) == 4)
def getting_retail_price_plus(callback: telebot.types.CallbackQuery):
    column_retail_price = callback.data
    new_brand_info_plus["retail_price"] = column_retail_price
    if column_retail_price != "Отсутствует":
        columns_available_choose.remove(column_retail_price)
        first_line_keys.remove(column_retail_price)
    mark = make_markup_for_info_plus()
    bot.send_message(callback.message.chat.id, f"Выберите столбец, в котором находится информация "
                     f"о <b>'рекомендованной розничной цене товара'</b>.\n\n"
                     f"{make_output_with_first_line()}",
                     reply_markup=mark, parse_mode="HTML")


@bot.callback_query_handler(func=lambda cal: flag_add_new_brand_plus and
                                             len(new_brand_info_plus) == 5)
def getting_recommended_retail_price_plus(callback: telebot.types.CallbackQuery):
    global new_brand_info_plus
    column_recommended_retail_price = callback.data
    new_brand_info_plus["recommended_retail_price"] = column_recommended_retail_price
    if column_recommended_retail_price != "Отсутствует":
        columns_available_choose.remove(column_recommended_retail_price)
        first_line_keys.remove(column_recommended_retail_price)
    bot.send_message(callback.message.chat.id, f"Получена вся необходимая информация, спасибо за "
                                               f"уделённое время.",
                     parse_mode="HTML")
    result = loading_new_handler_templates(new_brand_info_plus, current_DF)
    if result:
        asyncio.run(parsing(current_DF, new_brand_info_plus["brand_name"]))
    global flag_add_new_brand_plus
    flag_add_new_brand_plus = False
    new_brand_info_plus = dict()


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
