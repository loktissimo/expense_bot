from mysql.connector.errors import Error
import telebot
from telebot.types import ReplyKeyboardRemove
from db import query_db
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Texts
message_start_text = "Привет\\!\nДля начала представься, напиши:``` /name Иванов Иван``` "
message_ok_text = "Записывай свои траты. Уже можно."
message_done_text = "Готово! Можешь записывать траты."
message_insert_text = "Записал!"
message_phone_text = "Передай номер, пожалуйста."

# SQL queries
add_user = "INSERT INTO users (telegram_id, name) VALUES (%s, %s)"
add_phone = "UPDATE users SET tel = %s WHERE telegram_id = %s"
check_user_exist = "SELECT * FROM users WHERE telegram_id = %s"
add_expense = "INSERT INTO expense (telegram_id, text, write_date) VALUES (%s, %s, now())"


@bot.message_handler(commands=["start"])
def send_welcome(message):
    id = message.chat.id
    name = query_db(check_user_exist, (id,))
    if name:
        bot.send_message(id, message_ok_text)
    else:
        bot.send_message(id, message_start_text, parse_mode="MarkdownV2")


@bot.message_handler(commands=["name"])
def get_name(message):
    # bot.reply_to(message, "Hello, how are you doing?")
    id = message.chat.id
    text = message.text.lstrip("/name ")
    name = query_db(check_user_exist, (id,))
    if name:
        bot.send_message(id, message_ok_text)
    elif not text:
        bot.send_message(id, message_start_text, parse_mode="MarkdownV2")
    else:
        query_db(add_user, (id, text))

        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        reg_button = telebot.types.KeyboardButton(
            text="Передать номер телефона", request_contact=True)
        markup.add(reg_button)
        bot.send_message(
            message.chat.id, message_phone_text, reply_markup=markup)


@bot.message_handler(content_types=["contact"])
def contact_handler(message):
    id = message.chat.id
    phone = message.contact.phone_number
    query_db(add_phone, (phone, id))
    bot.send_message(
        message.chat.id, message_done_text, reply_markup=ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: True)
def get_all(message):
    id = message.chat.id
    text = message.text
    name = query_db(check_user_exist, (id,))
    if name:
        try:
            query_db(add_expense, (id, text))
            bot.reply_to(message, message_insert_text)
        except Error as e:
            bot.reply_to(message, e)
    else:
        bot.send_message(id, message_start_text, parse_mode="MarkdownV2")


bot.polling()
