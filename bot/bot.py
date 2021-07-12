import telebot
from db import query_db
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


# SQL queries
add_user = "INSERT INTO users (telegram_id, name) VALUES (%s, %s)"
check_user_exist = "SELECT * FROM users WHERE telegram_id = %s"
add_expense = "INSERT INTO expense (telegram_id, text) VALUES (%s, %s)"


@bot.message_handler(commands=["start"])
def send_welcome(message):
    # bot.reply_to(message, "Hello, how are you doing?")
    id = message.chat.id
    text = message.text
    if query_db(check_user_exist, (id,)):
        bot.send_message(id, "Записывай свои траты. Уже можно.")
    else:
        text = "Привет\\!\nДля начала представься, напиши:``` /name Иванов Иван ``` "
        bot.send_message(id, text, parse_mode="MarkdownV2")


@bot.message_handler(commands=["name"])
def get_name(message):
    # bot.reply_to(message, "Hello, how are you doing?")
    id = message.chat.id
    text = message.text
    name = query_db(check_user_exist, (id,))
    if name:
        bot.send_message(id, "Записывай свои траты. Уже можно.")
    else:
        query_db(add_user, (id, text.lstrip("/name ")))
        bot.send_message(
            id, "Отлично\\! Можно записывать траты\\.", parse_mode="MarkdownV2",
            request_contact=True
        )


@bot.message_handler(commands=["reg"])
def register(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True, row_width=1)
    reg_button = telebot.types.KeyboardButton(
        text="Зарегистрироваться", request_contact=True
    )
    keyboard.add(reg_button)
    bot.send_message(
        message.chat.id, "You should share your phone number", reply_markup=keyboard
    )


@bot.message_handler(content_types=["contact"])
def contact_handler(message):
    print(message.contact)


@bot.message_handler(func=lambda message: True)
def get_all(message):
    id = message.chat.id
    text = message.text
    name = query_db(check_user_exist, (id,))
    if name:
        query_db(add_expense, (id, text))
        bot.reply_to(message, "Записал!")
    else:
        text = "Привет\\!\nДля начала представься, напиши:``` /name Иванов Иван ``` "
        bot.send_message(id, text, parse_mode="MarkdownV2")


bot.polling()
