import telebot
import json
from dotenv import dotenv_values

bot = telebot.TeleBot(dotenv_values(".env")['TOKEN'], parse_mode=None)
baristas = dict()


@bot.message_handler(commands=['code'])
def checking_code(message):
    try:
        code = message.text.split()[1]
        if code in baristas and message.chat.id not in baristas[code]:
            baristas[code].append(message.chat.id)
            update_baristas_file()
            bot.send_message(message.chat.id, "Теперь вы бариста")

    except IndexError:
        bot.send_message(message.chat.id, "Отсутствует код кофейни")


def update_baristas_file():
    with open('baristas.txt', 'w') as file:
        file.write(json.dumps(baristas))


def load_baristas_file():
    global baristas
    with open('baristas.txt', 'r') as file:
        baristas = json.loads(file.read())


load_baristas_file()
bot.infinity_polling()
