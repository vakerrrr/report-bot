from ast import increment_lineno

from aiogram.types import KeyboardButton, InlineKeyboardMarkup
from classes.text import POINT_PLANS
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardButton

def points_kb():
    builder = ReplyKeyboardBuilder()
    for point in POINT_PLANS.keys():
        builder.add(KeyboardButton(text=point))
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)

def easter():
    inline_url_list = [
        [InlineKeyboardButton(text='GitHub', url='https://github.com/vakerrrr')],
        [InlineKeyboardButton(text='hh.ru', url='https://novosibirsk.hh.ru/resume/32600264ff0d70ee340039ed1f6a6161786450')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_url_list)