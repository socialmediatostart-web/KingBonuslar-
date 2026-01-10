from datetime import timedelta
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, Text
from bot.keyboards.default import main_menu_keyboard
from bot.keyboards.inline import bonus_transfer_inline_button_keyboard
from bot.loader import dp
from common.constants import DefaultKeyboardButtons
from config import SUPPORT_URL


def format_seconds(seconds):
    time = timedelta(seconds=seconds)
    days = time.days
    hours, remainder = divmod(time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{f'{days} days, ' if days > 0 else ''}" + \
           f"{f'{hours} hours, ' if hours > 0 else ''}" + \
           f"{f'{minutes} minutes, and {seconds}' + ' seconds'}"


@dp.message_handler(CommandHelp())
@dp.message_handler(Text(DefaultKeyboardButtons.Help.value))
async def process_faq(message: types.Message):
    await message.answer(f"Destek al 👉 <a href='{SUPPORT_URL}'>DESTEK BOTU</a>",
                         disable_web_page_preview=True,
                         reply_markup=main_menu_keyboard())


@dp.message_handler(Text(DefaultKeyboardButtons.BonusTransfer.value))
async def process_bonus_transfer(message: types.Message):
    await message.answer("Açık 👉",
                         reply_markup=bonus_transfer_inline_button_keyboard())
