import telebot
from telebot.types import *
from models.types import *
from typing import Callable
import logging
from utils.select_menu import SelectMenu

logger = logging.getLogger('telegram')


class TaskEditMenu:
    def __init__(self, bot: telebot.TeleBot, user: User, menu: Callable[[Message], None], mode: str):
        self.bot = bot
        self.menu = menu
        self.mode = mode
        self.user = user

    def start_choice(self, message):
        logger.info("Начинаем выбор тасков")

        select_menu = SelectMenu(self.bot, self.user.tasks, self.menu,
                                 self.delete_task if self.mode == "delete" else self.done_task)
        select_menu.display(message)

    def delete_task(self, message, task):
        logger.info("Удаляем таск {}".format(task))

        self.user.tasks.remove(task)
        self.bot.send_message(message.chat.id,
                              "Успешно удалил таск! 💸",
                              parse_mode="Markdown")
        self.menu(message)

    def done_task(self, message, task):
        logger.info("Заканчиваем таск {}".format(task))

        self.user.end_task(task)
        self.bot.send_message(message.chat.id,
                              "⭐ Поздравляю! ⭐\nЗакрываю таск и передаю тебе твои деньги! 💵 💵 💵",
                              parse_mode="Markdown")
        self.menu(message)
