from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import types
from bot.keyboards.default import main_menu_keyboard
from bot.loader import dp
from common.constants import CallbackQueryTypes, DefaultKeyboardButtons


@dp.message_handler(Text(DefaultKeyboardButtons.Cancel.value), state="*")
@dp.callback_query_handler(text=CallbackQueryTypes.Cancel.value, state='*')
async def cancel_from_callback(update: types.Message or types.CallbackQuery, state: FSMContext):
    if state:
        await state.finish()

    if type(update) == types.Message:
        message = update
    elif type(update) == types.CallbackQuery:
        message = update.message
    else:
        return

    await message.answer("İşlem iptal edildi", reply_markup=main_menu_keyboard())
    await message.delete()


async def cancel_from_keyboard(message: types.Message, state: FSMContext):
    if state:
        await state.finish()

    await message.answer("İşlem iptal edildi", reply_markup=main_menu_keyboard())
