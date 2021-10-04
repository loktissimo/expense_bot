from dotenv import load_dotenv
import os
import requests


load_dotenv('../.env')
BOT_TOKEN = os.environ.get("BOT_TOKEN")


def send_telegramm_message(id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"text": text, "chat_id": id}
    result = requests.post(url, data)
    return result.json()
