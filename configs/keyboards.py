import re
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton, InlineKeyboardButton
from configs.localization import Buttons
from aiogram import types


def cancel_key():
    key = ReplyKeyboardBuilder().add(KeyboardButton(text="Обратно"))
    return key.as_markup()


def start_keyboard():
    keyboard = ReplyKeyboardBuilder()
    for button in Buttons.start_keys:
        keyboard.add(KeyboardButton(text=button))
    keyboard.adjust(len(Buttons.start_keys)//2, True)
    return keyboard.as_markup()

