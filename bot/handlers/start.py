from asyncio import sleep
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ChatActions
from bot.states import UpdateSiteID
from common.constants import BuiltInReferralSources, DefaultKeyboardButtons, DefaultInlineButtons
from logics import UserLogics
from models import User
from bot.loader import dp, bot
from bot.keyboards.default import main_menu_keyboard, cancel_keyboard
from config import COMMUNITY_URL, REGISTRATION_URL, BOT_ADMINS, BONUS_TRANSFER_URL
from bot.keyboards.inline import message_inline_button_keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


@dp.message_handler(CommandStart())
async def process_start(message: types.Message):
    user = UserLogics().get_by_chat_id(message.from_user.id)
    if not user:
        referral_source = referral_user_id = None
        if arg := message.get_args():
            referral = UserLogics().get_by_id(arg.strip())
            if referral:
                referral_source = BuiltInReferralSources.User.value
                referral_user_id = referral.id
            else:
                referral_source = arg

        UserLogics().create(
            chat_id=message.from_user.id,
            username=message.from_user.username,
            nickname=message.from_user.username or message.from_user.first_name or message.from_user.id,
            site_id='',
            referral_source=referral_source,
            referral_user_id=referral_user_id,
            is_manager=bool(message.from_user.id in BOT_ADMINS)
        )  
        user = UserLogics().get_by_chat_id(message.from_user.id)

    await message.answer_photo(
        photo='https://i.pinimg.com/736x/67/fd/14/67fd14e8656002eeebbb1c139bc76d98.jpg',
        caption=(
            "🔥 Hazır mısın?\n\n"
            "Telegram’daki en hızlı oyunlarda anında kazan, sürprizleri keşfet! 🎯\n"
        ),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                text=DefaultInlineButtons.LearMore.value,
                web_app=WebAppInfo(url=BONUS_TRANSFER_URL)
            )
        )
    )
    reply_keyboard = main_menu_keyboard()
    await message.answer(
        text="Ana menüye hoş geldiniz! 🎉",
        reply_markup=reply_keyboard
    )
    
    await message.answer_chat_action(ChatActions.TYPING)
    await sleep(0.2)
