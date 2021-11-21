import json
import telebot
from order import Order
from dotenv import dotenv_values


class SendingOrderBot:
    order: Order
    bot: telebot.TeleBot

    def __init__(self, order: Order):
        self.order = order
        self.bot = telebot.TeleBot(dotenv_values(".env")['TOKEN'], parse_mode=None)

    def __str__(self):
        message = f'<b>Заказ №{self.order.order_number}</b>\n'
        message += f'<i>Содержание:</i> {self.order.order_content}\n'
        message += f'<i>Приготовить к:</i> {self.order.time.strftime("%H:%M")}\n'
        if self.order.phone_number:
            message += f'<i>Телефон покупателя:</i> +7{self.order.phone_number}\n'
        if self.order.email:
            message += f'<i>Почта покупателя:</i> {self.order.email}\n'

        return message

    def send_message(self):
        with open('baristas.txt', 'r') as file:
            baristas = json.loads(file.read())

        if self.order.coffee_house_id in baristas:
            self.bot.send_message(chat_id=baristas[self.order.coffee_house_id], text=str(self), parse_mode='HTML')
            # for i in baristas[self.order.coffee_house_id]:
            #     self.bot.send_message(chat_id=i, text=str(self), parse_mode='HTML')
