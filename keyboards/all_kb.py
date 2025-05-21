from aiogram.types import KeyboardButton
from classes.text import POINT_PLANS
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def points_kb():
    builder = ReplyKeyboardBuilder()
    for point in POINT_PLANS.keys():
        builder.add(KeyboardButton(text=point))
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)