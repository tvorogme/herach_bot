import telebot
from telebot.types import *
from models.types import *
from typing import Callable
import logging

logger = logging.getLogger('telegram')


class Bounty:
    def __init__(self, user: User, bot: telebot.TeleBot, menu: Callable[[Message], None]):
        self.bot = bot
        self.user = user
        self.menu = menu

        self.title: str = ""

    def add_task_handler(self, message: Message) -> None:
        if message.text == "Назад":
            logger.info("Go Back from Bounty.add_task_handler by {}".format(message.chat.id))
            self.menu(message)
        elif message.text:
            logger.info("Add title for task ({}) by {}".format(message.text, message.chat.id))
            self.title = message.text
            self.add_task_bounty(message)

    def add_task(self, message: Message) -> None:
        logger.info("Add Task by {}".format(message.chat.id))

        markup = ReplyKeyboardMarkup(row_width=2)
        markup.add(KeyboardButton("Назад"))

        self.bot.send_message(message.chat.id,
                              "Так-так, неужели новое задание завезли? ✨\nИ что за таск?".format(
                                  self.user.score),
                              parse_mode="Markdown", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.add_task_handler)

    def add_task_bounty_handler(self, message: Message) -> None:

        if message.text and message.text.isdigit():
            new_task = Task(self.title, int(message.text))
            self.user.add_task(new_task)

            self.bot.send_message(message.chat.id, "Жду не дождусь, когда ты закончишь делать эту хренатень. 🚀",
                                  parse_mode="Markdown")
            self.menu(message)

    def add_task_bounty(self, message: Message) -> None:
        logger.info("Add Bounty for task by {}".format(message.chat.id))

        markup = ReplyKeyboardMarkup(row_width=2)
        markup.add(KeyboardButton("Назад"))

        self.bot.send_message(message.chat.id,
                              "💰 И сколько ты получишь когда выполнишь его?\nСложность от 0 до 10. 🏇".format(
                                  self.user.score),
                              parse_mode="Markdown", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.add_task_bounty_handler)
