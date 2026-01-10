from asyncio import sleep
from aiogram import types
from aiogram.dispatcher.filters import Text
from bot.filters import UserFilter
from bot.keyboards.callback_datas import group_display_dict, request_bonus_callback, bonus_already_requested_callback, \
    cancel_bonus_request_callback, approve_bonus_request_callback, activate_bonus_request_callback, \
    bonus_requests_page_callback, activate_br_cancel_callback, activate_br_approve_callback, cancel_br_cancel_callback, \
    cancel_br_approve_callback, approve_br_approve_callback, approve_br_cancel_callback, refresh_bonus_request_callback, \
    cancel_br_approve_opt_callback
from bot.keyboards.default import main_menu_keyboard, manage_keyboard
from bot.keyboards.inline import bonus_request_keyboard, bonus_requests_navigation_keyboard, \
    activate_bonus_request_confirmation_keyboard, \
    approve_bonus_request_confirmation_keyboard, cancel_bonus_request_options_keyboard
from bot.loader import dp, bot
from common.constants import DATETIME_FORMAT, DefaultKeyboardButtons, \
    BonusRequestStatuses, bonus_request_icon_dict, DefaultInlineButtons, BonusRequestRejectReasons
from common.exceptions import BonusAlreadyApprovedError, BonusAlreadyActivatedError, BonusAlreadyCanceledError
from config import REGISTRATION_URL, COMMUNITY_URL, BONUS_REQUESTS_PER_PAGE
from logics import UserLogics, BonusRequestLogics, BonusLogics


async def _send_bonus_request_info(user_id: str, bonus_request_id: str, bonus_id: str):
    user = UserLogics.get_by_id(user_id)
    bonus_request = BonusRequestLogics.get_by_id(bonus_request_id)
    bonus = BonusLogics.get_by_id(bonus_id)

    user_subscribed = await UserLogics().is_subscriber(bot=bot, chat_id=bonus_request.user.chat_id)
    bonus_user = UserLogics().get_by_id(bonus_request.user_id)

    if user.is_manager:
        bonus_group_icon = group_display_dict.get(bonus.group, bonus.group)
        user_group_icon = group_display_dict.get(bonus_user.group, bonus_user.group)

        subscribed_text = '🟢 <b>Subscribed</b>' if user_subscribed else '🔴 <b>Not subscribed</b>'

        request_creation_date = f'<i>{bonus_request.created_at.strftime(DATETIME_FORMAT)}</i>'

        request_text_data = f"<b>📝 Request:</b> <i>{request_creation_date}</i>" \
                            f"\n<b>Status:</b> {bonus_request_icon_dict.get(bonus_request.status)}" + \
                            f"\n\n<b>{bonus_group_icon[0]} Bonus ID</b>: {bonus_id}" + \
                            f"\n<b>📄 Bonus text</b>: \n{bonus.description}" + \
                            f"\n<b>{user_group_icon[0]} User ID</b>: {bonus_user.chat_id}" + \
                            f"\n<b>🃏 Site ID </b>: {bonus_user.site_id if bonus_user.site_id else 'No site ID provided!'} " \
                            f"\n{subscribed_text}"

    else:
        request_text_data = f"<b>🚀 Talep durumu: {bonus_request_icon_dict.get(bonus_request.status)}</b>" \
                            f"\n\n<b>🎁 Bonus</b>: \n{bonus.description}"

    if bonus.photo_url:
        await bot.send_photo(
            chat_id=int(user.chat_id),
            photo=bonus.photo_url,
            caption=request_text_data,
            parse_mode="HTML",
            reply_markup=bonus_request_keyboard(
                bonus_request_id=bonus_request_id,
                is_manager=user.is_manager,
                request_is_active=bonus_request.status == BonusRequestStatuses.Active.value,
                user_id=bonus_request.user_id,
                bonus_id=bonus_id)
        )

    else:
        await bot.send_message(
            chat_id=int(user.chat_id),
            text=request_text_data,
            reply_markup=bonus_request_keyboard(
                bonus_request_id=bonus_request_id,
                is_manager=user.is_manager,
                request_is_active=bonus_request.status == BonusRequestStatuses.Active.value,
                user_id=bonus_request.user_id,
                bonus_id=bonus_id
            )
        )


@dp.callback_query_handler(bonus_already_requested_callback.filter(), UserFilter())
async def process_bonus_already_requested(call: types.CallbackQuery, callback_data: dict):

    await call.message.answer(text=f"Bu bonus için zaten bir talep mevcut 🏁" +
                                   f"\nDurumu {DefaultKeyboardButtons.BonusRequests.value} sekmesinden kontrol et")
    bonus_id = callback_data.get('bonus_id')
    bonus = BonusLogics().get_by_id(bonus_id)
    user = UserLogics().get_by_chat_id(call.from_user.id)

    bonus_request = BonusRequestLogics.get_list(user_id=user.id,
                                                bonus_id=bonus.id)[0]

    await sleep(0.2)
    await call.message.delete()
    await _send_bonus_request_info(user_id=bonus_request.user_id,
                                   bonus_id=bonus_request.bonus_id,
                                   bonus_request_id=bonus_request.id)


@dp.callback_query_handler(bonus_requests_page_callback.filter())
async def process_bonus_requests_pagination(call: types.CallbackQuery, callback_data: dict):
    page = int(callback_data["page"])
    user = UserLogics().get_by_chat_id(call.from_user.id)
    await send_bonus_requests_page(call=call, user=user, page=page)
    await call.answer()


async def send_bonus_requests_page(message=None, call=None, user=None, page=1):
    bonus_requests, total = get_paginated_bonus_requests(user, page)

    if not bonus_requests:
        await (call.message if call else message).answer(
            text=f"Mevcut bonusları {DefaultKeyboardButtons.Bonuses.value} bölümünde kontrol et"
        )
        return

    for request in bonus_requests:
        await _send_bonus_request_info(
            user_id=request.user_id,
            bonus_id=request.bonus_id,
            bonus_request_id=request.id)
        await sleep(0.2)

    await (call.message if call else message).answer(
        text=f"Sayfa {page}",
        reply_markup=bonus_requests_navigation_keyboard(page=page, total=total)
    )


@dp.message_handler(Text(DefaultKeyboardButtons.BonusRequests.value), UserFilter())
async def process_open_my_bonus_requests(message: types.Message):
    user = UserLogics().get_by_chat_id(message.from_user.id)
    await send_bonus_requests_page(message=message, user=user, page=1)


def get_paginated_bonus_requests(user, page: int):
    all_requests = BonusRequestLogics.get_list(user_id=user.id)
    total = len(all_requests)
    start = (page - 1) * BONUS_REQUESTS_PER_PAGE
    end = start + BONUS_REQUESTS_PER_PAGE
    return all_requests[start:end], total


@dp.callback_query_handler(refresh_bonus_request_callback.filter(), UserFilter())
async def process_refresh_bonus_request(call: types.CallbackQuery, callback_data: dict):
    bonus_request_id = callback_data.get('bonus_request_id')
    bonus_request = BonusRequestLogics.get_by_id(bonus_request_id)

    await sleep(0.2)
    await call.message.delete()
    await _send_bonus_request_info(user_id=bonus_request.user_id,
                                   bonus_id=bonus_request.bonus_id,
                                   bonus_request_id=bonus_request.id)


@dp.callback_query_handler(activate_bonus_request_callback.filter(), UserFilter(only_managers=True))
async def process_activate_bonus_request(call: types.CallbackQuery, callback_data: dict):
    await call.message.delete()
    bonus_request_id = callback_data.get('bonus_request_id')
    await call.message.answer(f"Are you sure you want to activate the request? 👉",
                              reply_markup=activate_bonus_request_confirmation_keyboard(bonus_request_id=bonus_request_id))


@dp.callback_query_handler(activate_br_approve_callback.filter(), UserFilter(only_managers=True))
async def process_activate_br_approve(call: types.CallbackQuery, callback_data: dict):
    bonus_request_id = callback_data.get('bonus_request_id')
    bonus_request = BonusRequestLogics.get_by_id(bonus_request_id)
    user = UserLogics().get_by_chat_id(call.from_user.id)
    try:
        BonusRequestLogics.activate(bonus_request)
        await call.message.answer(
            f'The request has been activated 🥳',
            reply_markup=manage_keyboard())

    except (BonusAlreadyActivatedError,):
        await call.message.answer(
            f"Ups, the request is already activated 🤭",
            reply_markup=manage_keyboard())

    await call.message.delete()
    await sleep(0.2)
    await _send_bonus_request_info(user_id=user.id,
                                   bonus_id=bonus_request.bonus_id,
                                   bonus_request_id=bonus_request.id)


@dp.callback_query_handler(activate_br_cancel_callback.filter(), UserFilter(only_managers=True))
async def process_activate_br_cancel(call: types.CallbackQuery, callback_data: dict):
    bonus_request_id = callback_data.get('bonus_request_id')
    bonus_request = BonusRequestLogics.get_by_id(bonus_request_id)
    user = UserLogics().get_by_chat_id(call.from_user.id)
    await call.message.answer(
        f"Huh, the request was not activated 😌",
        reply_markup=manage_keyboard())
    await call.message.delete()
    await sleep(0.2)
    await _send_bonus_request_info(user_id=user.id,
                                   bonus_id=bonus_request.bonus_id,
                                   bonus_request_id=bonus_request.id)


@dp.callback_query_handler(cancel_bonus_request_callback.filter(), UserFilter(only_managers=True))
async def process_cancel_bonus_request(call: types.CallbackQuery, callback_data: dict):
    await call.message.delete()
    bonus_request_id = callback_data.get('bonus_request_id')
    await call.message.answer(
        f"Select reject reason to cancel the request? 👉",
        reply_markup=cancel_bonus_request_options_keyboard(bonus_request_id=bonus_request_id))


@dp.callback_query_handler(cancel_br_approve_callback.filter(), UserFilter(only_managers=True))
async def process_cancel_br_approve(call: types.CallbackQuery, callback_data: dict):
    bonus_request_id = callback_data.get('bonus_request_id')
    bonus_request = BonusRequestLogics.get_by_id(bonus_request_id)
    user = UserLogics().get_by_chat_id(call.from_user.id)
    user_chat_id = bonus_request.user.chat_id
    try:
        BonusRequestLogics.cancel(bonus_request)
        await call.message.answer(
            f'The request has been canceled 🥳',
            reply_markup=manage_keyboard())

        await bot.send_message(chat_id=int(user_chat_id),
                               text=f"⚠️ Bonus talebinin durumu: {bonus_request_icon_dict.get(BonusRequestStatuses.Canceled.value)}")

    except (BonusAlreadyCanceledError,):
        await call.message.answer(
            f"Ups, the request is already canceled 🤭",
            reply_markup=manage_keyboard())

    await call.message.delete()
    await sleep(0.2)
    await _send_bonus_request_info(user_id=user.id,
                                   bonus_id=bonus_request.bonus_id,
                                   bonus_request_id=bonus_request.id)


@dp.callback_query_handler(cancel_br_approve_opt_callback.filter(), UserFilter(only_managers=True))
async def process_cancel_br_approve_opt(call: types.CallbackQuery, callback_data: dict):
    bonus_request_id = callback_data.get('bonus_request_id')
    reject_reason = callback_data.get('reject_reason')
    bonus_request = BonusRequestLogics.get_by_id(bonus_request_id)
    user = UserLogics().get_by_chat_id(call.from_user.id)
    user_chat_id = bonus_request.user.chat_id
    try:
        BonusRequestLogics.cancel(bonus_request)
        await call.message.answer(
            f'The request has been canceled 🥳',
            reply_markup=manage_keyboard())

        await bot.send_message(chat_id=int(user_chat_id),
                               text=f"⚠️ Bonus talebinin durumu: {bonus_request_icon_dict.get(BonusRequestStatuses.Canceled.value)}"
                                    f"\n<i>{BonusRequestRejectReasons.get(reject_reason)}</i>")

    except (BonusAlreadyCanceledError,):
        await call.message.answer(
            f"Ups, the request is already canceled 🤭",
            reply_markup=manage_keyboard())

    await call.message.delete()
    await sleep(0.2)
    await _send_bonus_request_info(user_id=user.id,
                                   bonus_id=bonus_request.bonus_id,
                                   bonus_request_id=bonus_request.id)


@dp.callback_query_handler(cancel_br_cancel_callback.filter(), UserFilter(only_managers=True))
async def process_cancel_br_cancel(call: types.CallbackQuery, callback_data: dict):
    bonus_request_id = callback_data.get('bonus_request_id')
    bonus_request = BonusRequestLogics.get_by_id(bonus_request_id)
    user = UserLogics().get_by_chat_id(call.from_user.id)
    await call.message.answer(
                f"Huh, the request was not canceled 😌",
                reply_markup=manage_keyboard())
    await call.message.delete()
    await sleep(0.2)
    await _send_bonus_request_info(user_id=user.id,
                                   bonus_id=bonus_request.bonus_id,
                                   bonus_request_id=bonus_request.id)


@dp.callback_query_handler(approve_bonus_request_callback.filter(), UserFilter(only_managers=True))
async def process_approve_bonus_request(call: types.CallbackQuery, callback_data: dict):
    await call.message.delete()
    bonus_request_id = callback_data.get('bonus_request_id')
    await call.message.answer(f"Are you sure you want to approve the request? 👉",
                              reply_markup=approve_bonus_request_confirmation_keyboard(bonus_request_id=bonus_request_id))


@dp.callback_query_handler(approve_br_approve_callback.filter(), UserFilter(only_managers=True))
async def process_approve_br_approve(call: types.CallbackQuery, callback_data: dict):
    bonus_request_id = callback_data.get('bonus_request_id')
    bonus_request = BonusRequestLogics.get_by_id(bonus_request_id)
    user = UserLogics().get_by_chat_id(call.from_user.id)
    user_chat_id = bonus_request.user.chat_id
    try:
        BonusRequestLogics.approve(bonus_request)
        await call.message.answer(
            f'The request has been approved 🥳',
            reply_markup=manage_keyboard())

        await bot.send_message(chat_id=int(user_chat_id),
                               text=f"⚠️ Bonus talebinin durumu: {bonus_request_icon_dict.get(BonusRequestStatuses.Approved.value)}<i>"
                                    f"\n<b>{DefaultKeyboardButtons.BonusRequests.value}</b> sekmesini kontrol et</i>")

    except (BonusAlreadyApprovedError,):
        await call.message.answer(
            f"Ups, the request is already approved 🤭",
            reply_markup=manage_keyboard())
    await call.message.delete()
    await sleep(0.5)
    await _send_bonus_request_info(user_id=user.id,
                                   bonus_id=bonus_request.bonus_id,
                                   bonus_request_id=bonus_request.id)


@dp.callback_query_handler(approve_br_cancel_callback.filter(), UserFilter(only_managers=True))
async def process_approve_br_cancel(call: types.CallbackQuery, callback_data: dict):
    bonus_request_id = callback_data.get('bonus_request_id')
    bonus_request = BonusRequestLogics.get_by_id(bonus_request_id)
    user = UserLogics().get_by_chat_id(call.from_user.id)

    await call.message.answer(
        f"Huh, the request was not approved 😌",
        reply_markup=manage_keyboard())
    await call.message.delete()
    await sleep(0.5)
    await _send_bonus_request_info(user_id=user.id,
                                   bonus_id=bonus_request.bonus_id,
                                   bonus_request_id=bonus_request.id)


@dp.callback_query_handler(request_bonus_callback.filter(), UserFilter())
async def process_request_bonus(call: types.CallbackQuery, callback_data: dict):
    bonus_id = callback_data.get('bonus_id')
    bonus = BonusLogics().get_by_id(bonus_id)
    user = UserLogics().get_by_chat_id(call.from_user.id)
    bonus_requests = BonusRequestLogics.get_list(user_id=user.id, bonus_id=bonus_id)

    if len(bonus_requests):

        bonus_request = bonus_requests[0]
        await call.message.answer(text=f"Bu bonus için zaten bir talep mevcut 🏁",
                                  reply_markup=main_menu_keyboard())
        await sleep(0.2)
        await call.message.delete()
        await _send_bonus_request_info(user_id=bonus_request.user_id,
                                       bonus_id=bonus_request.bonus_id,
                                       bonus_request_id=bonus_request.id)

        return
    else:
        # Check user subscription
        user_subscribed = await UserLogics().is_subscriber(bot=bot, chat_id=user.chat_id)
        if not user_subscribed:
            await call.message.answer(text=f"Bonusu talep etmek için 👉 <a href='{COMMUNITY_URL}'>KANALIMIZA</a> abone ol 📰",
                                      reply_markup=main_menu_keyboard(), disable_web_page_preview=True)

            return
        if not user.site_id:
            await call.message.answer(text=
                                      f"Bonusu talep etmek için Site ID’ni {DefaultKeyboardButtons.Profile.value} bölümünden gir" +
                                      f"veya <a href='{REGISTRATION_URL}'>BURAYA</a> tıkla 🎮",
                                      reply_markup=main_menu_keyboard(), disable_web_page_preview=True)

            return
        if any([user.group != bonus.group,
                bonus.is_active is False,
                bonus.is_removed]):
            await call.message.answer(text=f"Bu bonus artık aktif değil 🕰️",
                                      reply_markup=main_menu_keyboard())
            await sleep(0.2)
            await call.message.delete()
            return

        new_bonus_request = BonusRequestLogics.create(user_id=user.id, bonus_id=bonus_id)
        await call.message.answer(text=f"Bonus talebi başarıyla oluşturuldu ✅",
                                  reply_markup=main_menu_keyboard())

        await _send_bonus_request_info(user_id=new_bonus_request.user_id,
                                       bonus_id=new_bonus_request.bonus_id,
                                       bonus_request_id=new_bonus_request.id)
        await sleep(0.2)
        await call.message.delete()
