import telebot
import db
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Hello, how are you doing?")
    id = message.chat.id
    text = message.text
    db.write_db(db.add_user, (id, text))


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.polling()
