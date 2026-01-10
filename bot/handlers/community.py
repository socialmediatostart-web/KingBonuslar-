from aiogram import types
from aiogram.dispatcher.filters import Text
from bot.keyboards.inline import community_keyboard
from bot.loader import dp
from common.constants import DefaultKeyboardButtons
from config import COMMUNITY_URL


@dp.message_handler(Text(DefaultKeyboardButtons.Community.value))
async def community(message: types.Message):
    await message.answer("Sonuçlar, promosyonlar, haberler ve tüm gelişmeler — hepsi kanalımızda!",
                         reply_markup=community_keyboard(COMMUNITY_URL))
