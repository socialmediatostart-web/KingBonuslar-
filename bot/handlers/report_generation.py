from asyncio import sleep
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType
from bot.filters import UserFilter
from bot.keyboards.callback_datas import open_user_callback, user_group_display_dict, set_user_negative_callback, \
    set_user_positive_callback, set_user_neutral_callback, set_user_vip_callback, set_user_all_callback, \
    block_user_callback, unblock_user_callback, open_users_per_group_callback, group_display_dict, users_page_callback
from bot.keyboards.default import cancel_keyboard, main_menu_keyboard, manage_keyboard
from bot.keyboards.inline import profile_keyboard, user_keyboard, open_users_per_group_keyboard, \
    users_navigation_keyboard
from bot.loader import dp, bot
from bot.states import UpdateSiteID, BlockUser, UnblockUser, ViewUser
from common.constants import DefaultKeyboardButtons, CallbackQueryTypes, DefaultInlineButtons, Groups
from common.exceptions import UserAlreadyNegativeError, UserAlreadyPositiveError, UserAlreadyNeutralError, \
    UserAlreadyVipError, UserAlreadyAllError, UserAlreadyBlockedError
from config import COMMUNITY_URL, REGISTRATION_URL, USERS_PER_PAGE
from logics import UserLogics
from models import User
from html import escape as html_escape


