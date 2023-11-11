import telebot
import peewee as pw
import pandas as pd


db = pw.SqliteDatabase("db.sqlite3")
bot = telebot.TeleBot(open("bot info.txt").readlines()[0].strip())


@bot.message_handler(commands=["start"])
def start_message(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Бот начал работу")


@bot.message_handler(commands=["add_new_brand"])
def add_new_brand(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Введите название автомобильной марки")


if __name__ == "__main__":
    bot.polling(none_stop=True)
