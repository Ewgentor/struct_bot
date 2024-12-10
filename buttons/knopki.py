import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup, InlineKeyboardButton,
                           InlineKeyboardMarkup, CallbackQuery, BotCommand)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from environs import Env
from lexicon.lexicon import LEXICON

BUTTONS = {
    'btn_1': '1',
    'btn_2': '2',
    'btn_3': '3',
    'btn_4': '4',
    'btn_5': '5',
}


def create_inline_kb(type: int, width: int,
                     *args: str,
                     last_btn=None,
                     **kwargs: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    for button in args:
        buttons.append(InlineKeyboardButton(
            text=LEXICON[button] if button in LEXICON else button,
            callback_data=button))

    for button, text in kwargs.items():
        buttons.append(InlineKeyboardButton(
            text=text,
            callback_data=button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    if type == 1:
        kb_builder.row(*buttons, width=width)
    elif type == 2:
        kb_builder.row(*buttons[::-1], width=width)
    elif type == 3:
        kb_builder.row(*buttons[:2],width=2)
        kb_builder.row(buttons[-1], width=1)
    elif type == 4:
        kb_builder.row(buttons[0], width=1)
        kb_builder.row(*buttons[1:],width=2)
    else:
        random.shuffle(buttons)
        kb_builder.row(*buttons, width=5)



    if last_btn:
        kb_builder.row(InlineKeyboardButton(
            text=last_btn,
            callback_data='last_btn'
        ))

    return kb_builder.as_markup()