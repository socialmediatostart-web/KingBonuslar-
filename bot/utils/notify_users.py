from typing import List
from aiogram import Dispatcher
from aiogram.utils.exceptions import BotBlocked
# from bot.keyboards.inline import market_main_keyboard
# from common.constants import DATETIME_FORMAT
# from common.utils import get_current_datetime
# from logics import BonusLogics
from models import User  # , Bonus


async def send_to_list(dp: Dispatcher, users: List[User], text: str):
    for user in users:
        try:
            await dp.bot.send_message(
                text=text,
                chat_id=user.chat_id
            )
        except BotBlocked:
            user.is_active = False
            user.save(only=(User.is_active,))


# async def send_bonus(dp: Dispatcher, user: User, bonus: Bonus):
#     is_bonus_exists = bool(BonusLogics().get_list())
#
#     await dp.bot.send_message(
#         chat_id=user.chat_id,
#         text=f"<b>{bonus.name}</b>\n"
#              f"<p>{bonus.description}</p>\n"
#              f"<i>Ставки принимаются до {market.expire_at.strftime(DATETIME_FORMAT)}</i>",
#         reply_markup=market_main_keyboard(
#             market_id=market.id,
#             can_create=market.expire_at > get_current_datetime() and (not is_bet_exists or user.is_manager),
#             can_manage=user.is_manager
#         ),
#         disable_web_page_preview=True
#     )
