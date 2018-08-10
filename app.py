import telebot
from telebot.types import *
from telebot import apihelper
import logging
from utils.threadering import threaded
import dill
from time import sleep
from collections import defaultdict
from models.types import *
import os
from modules.bounty import Bounty
import atexit

bot = telebot.TeleBot("631678522:AAFC8T_f7C_WsXfnK4-jkKeKF2JwuJX4ADM")

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)

logger = logging.getLogger('telegram')
logger.setLevel(logging.DEBUG)

if 'data.pck' in os.listdir("./"):
    data = dill.load(open("data.pck", "rb"))
else:
    data = defaultdict(lambda: User())


@threaded
def dump_bd_every_ten_secs():
    dump_every = 60 * 100
    logger.info("Dump data every {}sec.".format(dump_every))

    while True:
        logger.debug("Dumped.")
        dill.dump(data, open("data.pck", "wb"))
        sleep(dump_every)


def main_menu(message: Message) -> None:
    logger.info("Main menu by {}".format(message.chat.id))
    user = data[message.chat.id]

    first_button = 'Завершить задание ✔'
    second_button = 'Добавить задание ✏'
    third_button = 'Статистика 🚩'
    fourth_button = 'Удалить таск 🚧'

    markup = ReplyKeyboardMarkup(row_width=2)
    markup.add(KeyboardButton(first_button))
    markup.add(KeyboardButton(second_button))
    markup.row(KeyboardButton(third_button), KeyboardButton(fourth_button))

    bot.send_message(message.chat.id,
                     "✌ Хорошего дня!\n😉 Твой счёт *{}Ť*.\nДобавляй и заканчивай таски чтобы получить больше.".format(
                         user.score),
                     parse_mode="Markdown", reply_markup=markup)

    def main_menu_button(message: Message) -> None:
        logger.info("{} by {}".format(message.text, message.chat.id))

        if message.text == first_button:
            pass

        elif message.text == second_button:
            bounty_menu = Bounty(user, bot, main_menu)
            bounty_menu.add_task(message)

        elif message.text == third_button:
            pass

    bot.register_next_step_handler(message, main_menu_button)


@bot.message_handler(commands=["start"])
def intro(message: Message) -> None:
    logger.debug("/start by {}".format(message.chat.id))

    if message.chat.id == 148363699:
        main_menu(message)
    else:
        bot.send_message(message, "Email me. tvorog@tvorog.me")


@bot.message_handler(func=lambda message: True)
def to_main_menu(message: Message) -> None:
    logger.info("To main menu by {}".format(message.chat.id))

    if message.chat.id in data:
        main_menu(message)


if __name__ == "__main__":
    logger.info("Start application")
    apihelper.proxy = {'https': 'socks5://127.0.0.1:9050'}

    # dump_bd_every_ten_secs()
    atexit.register(lambda: dill.dump(data, open("data.pck", "wb")))

    bot.polling(none_stop=True, timeout=120)
