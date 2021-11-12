import json
import telebot
import argparse
from dotenv import dotenv_values

bot = telebot.TeleBot(dotenv_values(".env")['TOKEN'], parse_mode=None)

parser = argparse.ArgumentParser(description='Данные по заказу')
parser.add_argument("--coffee_house_id", type=str, required=True, help='ID кофейни')
parser.add_argument("--order_content", type=str, required=True, help='Содержание заказа')
parser.add_argument("--time", type=str, required=True, help='К какому времени приготовить')
parser.add_argument("--order_number", type=int, required=True, help='Номер заказа')
parser.add_argument("--phone_number", type=str, help='Номер толефона покупателя')
parser.add_argument("--mail", type=str, required=True, help='Почта покупателя')
args = parser.parse_args()

message = f'<b>Заказ №{args.order_number}</b>\n'
message += f'<i>Содержание:</i> {args.order_content}\n'
message += f'<i>Приготовить к:</i> {args.time}\n'
if args.phone_number:
    message += f'<i>Телефон покупателя:</i> {args.phone_number}\n'
if args.mail:
    message += f'<i>Почта покупателя:</i> {args.mail}\n'

with open('baristas.txt', 'r') as file:
    baristas = json.loads(file.read())

if args.coffee_house_id in baristas:
    for i in baristas[args.coffee_house_id]:
        bot.send_message(chat_id=i, text=message, parse_mode='HTML')
