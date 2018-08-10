import telebot
from telebot.types import *
from typing import Callable, List


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    tmp = []

    for i in range(0, len(l), n):
        tmp.append(l[i:i + n])

    return tmp


class SelectMenu:
    def __init__(self, bot: telebot.TeleBot, all_choices: List,
                 back_func: Callable,
                 on_choice: Callable, to_show: int = 4):
        self.bot = bot
        self.back_func = back_func
        self.on_choice = on_choice
        self.all_choices = all_choices
        all_choices = list(enumerate(all_choices))

        self.pages = chunks(all_choices, to_show)
        self.page = 0

    @property
    def at_first(self):
        return self.page == 0

    @property
    def at_last(self):
        return self.page + 1 == len(self.pages)

    @property
    def current_page(self):
        return self.pages[self.page]

    def display(self, message):
        choice_from = self.pages[self.page]

        markup = ReplyKeyboardMarkup(row_width=2)

        for index, item in choice_from:
            markup.add(KeyboardButton(text="{}) {}".format(index + 1, item)))

        if not self.at_last:
            markup.row(KeyboardButton("Назад"), KeyboardButton("Вперед"))
        else:
            markup.add(KeyboardButton("Назад"))

        self.bot.send_message(message.chat.id, "Выберете...", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.react)

    def react(self, message):
        for index, item in self.current_page:
            if message.text == "{}) {}".format(index + 1, item):
                self.on_choice(message, item)
                return

        if message.text == "Вперед" and not self.at_last:
            self.page += 1
            self.display(message)

        elif message.text == "Назад":
            if not self.at_first:
                self.page -= 1
                self.display(message)
            else:
                self.back_func(message)
