from asyncio import sleep
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType
from bot.filters import UserFilter
from bot.keyboards.callback_datas import open_user_callback, user_group_display_dict, set_user_negative_callback, \
    set_user_positive_callback, set_user_neutral_callback, set_user_vip_callback, set_user_all_callback, \
    block_user_callback, unblock_user_callback, open_users_per_group_callback, group_display_dict, users_page_callback, \
    block_user_approve_callback, block_user_cancel_callback, unblock_user_approve_callback, \
    unblock_user_cancel_callback, change_user_group_cancel_callback, change_user_group_callback
from bot.keyboards.default import cancel_keyboard, main_menu_keyboard, manage_keyboard
from bot.keyboards.inline import profile_keyboard, user_keyboard, open_users_per_group_keyboard, \
    users_navigation_keyboard, block_user_confirmation_keyboard, unblock_user_confirmation_keyboard, \
    change_user_group_keyboard
from bot.loader import dp, bot
from bot.states import UpdateSiteID, ViewUser
from common.constants import DefaultKeyboardButtons, CallbackQueryTypes, DefaultInlineButtons, Groups
from common.exceptions import UserAlreadyNegativeError, UserAlreadyPositiveError, UserAlreadyNeutralError, \
    UserAlreadyVipError, UserAlreadyAllError, UserAlreadyBlockedError, UserAlreadyUnblockedError
from config import COMMUNITY_URL, REGISTRATION_URL, USERS_PER_PAGE
from logics import UserLogics
from models import User
from html import escape as html_escape


async def _send_user_info(message: types.Message, user_id: str):
    user = UserLogics().get_by_id(user_id)
    user_subscribed = await UserLogics().is_subscriber(bot=bot, chat_id=user.chat_id)
    site_id_text = html_escape(user.site_id) if user.site_id else "📛 No Site ID!"
    referrals_count = len(UserLogics().get_referral_users_list(user.id))
    source = user.referral_source
    if user.referral_user_id:
        source = UserLogics().get_by_id(user.referral_user_id).chat_id
    await message.answer(
        f"<pre>{user.chat_id}</pre>\n"
        f"🔗: {user.username if user.username else user.nickname}, 🃏: <b>{site_id_text}</b>\n"
        f"📣: <b>{'✅ Subscribed' if user_subscribed else '📛 Not subscribed!'}</b>\n"
        f"⚖️: <b>Referrals:</b> {referrals_count}\n"
        f"📤: <b>Source:</b> \n<pre>{source}</pre>\n"
        f"⛓️‍: <b>{'Blocked' if user.is_blocked else 'Not blocked'}</b>, "
        f"{'👮‍, ' if user.is_manager else ''}Group: {user_group_display_dict.get(user.group)[0]}",
        disable_web_page_preview=True,
        parse_mode="HTML",
        reply_markup=user_keyboard(
            opened_user_id=user_id,
            is_opened_user_blocked=user.is_blocked
        )
    )


@dp.callback_query_handler(open_user_callback.filter(), UserFilter(only_managers=True))
async def process_open_user_callback(call: types.CallbackQuery, callback_data: dict):
    user_id = callback_data.get('user_id')
    await _send_user_info(call.message, user_id)
    await call.answer()


async def send_users_page(message=None, call=None, group=None, page=1):
    users, total = get_paginated_users(group, page)

    target = call.message if call else message

    if not users:
        await target.answer(f"No users found for group: {group_display_dict.get(group)[0]} {group}")
        return

    # Send user cards
    for user in users:
        await _send_user_info(target, user.id)
        await sleep(0.2)

    # Page controller
    page_text = f"Users in {group_display_dict.get(group)[0]} → Page {page} / {(total + USERS_PER_PAGE - 1) // USERS_PER_PAGE}"
    keyboard = users_navigation_keyboard(group=group, page=page, total=total)

    if call:
        # Edit page control message
        try:
            await call.message.edit_text(page_text, reply_markup=keyboard)
        except Exception:
            # Fallback if edit fails
            await call.message.answer(page_text, reply_markup=keyboard)
    else:
        await message.answer(page_text, reply_markup=keyboard)


def get_paginated_users(group, page: int):
    all_users = UserLogics().get_group_list(group)
    total = len(all_users)
    start = (page - 1) * USERS_PER_PAGE
    end = start + USERS_PER_PAGE
    return all_users[start:end], total


@dp.message_handler(Text(DefaultKeyboardButtons.ViewUsersPerGroup.value), UserFilter(only_managers=True))
async def process_view_users_by_group(message: types.Message):
    await message.answer("Select user group to view first 👉:", reply_markup=open_users_per_group_keyboard())


@dp.callback_query_handler(open_users_per_group_callback.filter(), UserFilter(only_managers=True))
async def confirm_view_users_by_group(call: types.CallbackQuery, callback_data: dict):
    group = callback_data.get('group')
    await send_users_page(message=call.message, group=group, page=1)
    await call.answer()


@dp.callback_query_handler(users_page_callback.filter(), UserFilter(only_managers=True))
async def process_users_pagination(call: types.CallbackQuery, callback_data: dict):
    group = callback_data["group"]
    page = int(callback_data["page"])
    await send_users_page(call=call, group=group, page=page)
    await call.answer()


@dp.message_handler(Text(DefaultKeyboardButtons.ViewUser.value), UserFilter(only_managers=True))
async def process_view_user_by_id(message: types.Message):
    await ViewUser.send_chat_id.set()
    await message.answer("Enter user chat id to view 👉:",
                         reply_markup=cancel_keyboard())


@dp.message_handler(UserFilter(only_managers=True), state=ViewUser.send_chat_id,
                    content_types=(ContentType.ANY,))
async def confirm_view_entered_user(message: types.Message, state: FSMContext):
    user_to_view = message.text.strip()
    user = UserLogics().get_by_chat_id(user_to_view)

    await state.finish()

    if not user:
        await message.answer(text="The user is not found 🚨", reply_markup=manage_keyboard())
        return

    await message.answer(text="The user is found ✅", reply_markup=manage_keyboard())
    if not user_to_view.isdigit() or len(user_to_view) > 20:
        await message.answer(
            f'Wrong user chat id input (only < 20 digits)🚨',
            reply_markup=manage_keyboard())
    else:
        await _send_user_info(message=message, user_id=user.id)


@dp.callback_query_handler(block_user_callback.filter(), UserFilter(only_managers=True))
async def process_block_user(call: types.CallbackQuery, callback_data: dict):
    opened_user_id = callback_data.get('opened_user_id')
    await call.message.answer(f"Are you sure you want to block the user? 👉",
                              reply_markup=block_user_confirmation_keyboard(opened_user_id=opened_user_id))


@dp.callback_query_handler(block_user_approve_callback.filter(), UserFilter(only_managers=True))
async def process_block_user_approve(call: types.CallbackQuery, callback_data: dict):
    opened_user_id = callback_data.get('opened_user_id')
    opened_user = UserLogics().get_by_id(opened_user_id)
    try:
        UserLogics().block(opened_user)
        await call.message.answer(
            f'The user has been blocked 😈',
            reply_markup=manage_keyboard())

    except (UserAlreadyBlockedError,):
        await call.message.answer(
            f"Ups, the user is already blocked 🤭",
            reply_markup=manage_keyboard())

    await call.message.delete()
    await _send_user_info(call.message, opened_user_id)


@dp.callback_query_handler(block_user_cancel_callback.filter(), UserFilter(only_managers=True))
async def process_block_user_cancel(call: types.CallbackQuery, callback_data: dict):
    opened_user_id = callback_data.get('opened_user_id')
    await call.message.answer(
        f"Huh, the user was not blocked 😌",
        reply_markup=manage_keyboard())

    await call.message.delete()
    await _send_user_info(call.message, opened_user_id)


@dp.callback_query_handler(unblock_user_callback.filter(), UserFilter(only_managers=True))
async def process_unblock_user(call: types.CallbackQuery, callback_data: dict):
    opened_user_id = callback_data.get('opened_user_id')
    await call.message.answer(f"Are you sure you want to unblock the user? 👉",
                              reply_markup=unblock_user_confirmation_keyboard(opened_user_id=opened_user_id))
    await call.message.delete()


@dp.callback_query_handler(unblock_user_approve_callback.filter(), UserFilter(only_managers=True))
async def process_unblock_user_approve(call: types.CallbackQuery, callback_data: dict):
    opened_user_id = callback_data.get('opened_user_id')
    opened_user = UserLogics().get_by_id(opened_user_id)
    try:
        UserLogics().unblock(opened_user)
        await call.message.answer(
            f'The user has been unblocked 😈',
            reply_markup=manage_keyboard())

    except (UserAlreadyUnblockedError,):
        await call.message.answer(
            f"Ups, the user is already unblocked 🤭",
            reply_markup=manage_keyboard())

    await call.message.delete()
    await _send_user_info(call.message, opened_user_id)


@dp.callback_query_handler(unblock_user_cancel_callback.filter(), UserFilter(only_managers=True))
async def process_unblock_user_cancel(call: types.CallbackQuery, callback_data: dict):
    opened_user_id = callback_data.get('opened_user_id')
    await call.message.answer(f"Huh, the user was not unblocked 😌", reply_markup=manage_keyboard())
    await call.message.delete()
    await _send_user_info(call.message, opened_user_id)


@dp.callback_query_handler(change_user_group_callback.filter(), UserFilter(only_managers=True))
async def process_change_user_group_callback(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    opened_user_id = callback_data.get('opened_user_id')
    user = UserLogics.get_by_id(opened_user_id)
    await state.update_data(opened_user_id=opened_user_id)

    await call.message.answer(f"Select new group for the user",
                              reply_markup=change_user_group_keyboard(opened_user_id=opened_user_id, current_group=user.group))
    await call.message.delete()


@dp.callback_query_handler(change_user_group_cancel_callback.filter(), UserFilter(only_managers=True))
async def process_change_user_group_cancel_callback(call: types.CallbackQuery, callback_data: dict):
    opened_user_id = callback_data.get('opened_user_id')
    await call.message.answer(f"Huh, the user group was not changed 😌", reply_markup=manage_keyboard())
    await call.message.delete()
    await _send_user_info(call.message, opened_user_id)


@dp.callback_query_handler(set_user_all_callback.filter(), UserFilter(only_managers=True))
async def process_set_user_all(call: types.CallbackQuery, callback_data: dict):
    opened_user_id = callback_data.get('opened_user_id')
    opened_user = UserLogics().get_by_id(opened_user_id)
    try:
        UserLogics().set_group_all(opened_user)
        await call.answer(
            f'The user has been set to {DefaultInlineButtons.AllBonus.value} {Groups.All.value} group!',
            show_alert=True)
    except UserAlreadyAllError:
        await call.answer(
            f"Ups, the user group is already {DefaultInlineButtons.AllBonus.value} {Groups.All.value} 🤭",
            show_alert=True)

    await call.message.delete()

    await _send_user_info(call.message, opened_user_id)


@dp.callback_query_handler(set_user_vip_callback.filter(), UserFilter(only_managers=True))
async def process_set_user_vip(call: types.CallbackQuery, callback_data: dict):
    opened_user_id = callback_data.get('opened_user_id')
    opened_user = UserLogics().get_by_id(opened_user_id)
    try:
        UserLogics().set_group_vip(opened_user)
        await call.answer(
            f'The user has been set to {DefaultInlineButtons.VIPBonus.value} {Groups.Vip.value} group!',
            show_alert=True)
    except UserAlreadyVipError:
        await call.answer(
            f"Ups, the user group is already {DefaultInlineButtons.VIPBonus.value} {Groups.Vip.value} 🤭",
            show_alert=True)

    await call.message.delete()

    await _send_user_info(call.message, opened_user_id)


@dp.callback_query_handler(set_user_positive_callback.filter(), UserFilter(only_managers=True))
async def process_set_user_positive(call: types.CallbackQuery, callback_data: dict):
    opened_user_id = callback_data.get('opened_user_id')
    opened_user = UserLogics().get_by_id(opened_user_id)
    try:
        UserLogics().set_group_positive(opened_user)
        await call.answer(
            f'The user has been set to {DefaultInlineButtons.PositiveBonus.value} {Groups.Positive.value} group!',
            show_alert=True)
    except UserAlreadyPositiveError:
        await call.answer(
            f"Ups, the user group is already {DefaultInlineButtons.PositiveBonus.value} {Groups.Positive.value} 🤭",
            show_alert=True)

    await call.message.delete()

    await _send_user_info(call.message, opened_user_id)


@dp.callback_query_handler(set_user_neutral_callback.filter(), UserFilter(only_managers=True))
async def process_set_user_neutral(call: types.CallbackQuery, callback_data: dict):
    opened_user_id = callback_data.get('opened_user_id')
    opened_user = UserLogics().get_by_id(opened_user_id)
    try:
        UserLogics().set_group_neutral(opened_user)
        await call.answer(
            f'The user has been set to {DefaultInlineButtons.NeutralBonus.value} {Groups.Neutral.value} group!',
            show_alert=True)
    except UserAlreadyNeutralError:
        await call.answer(
            f"Ups, the user group is already {DefaultInlineButtons.NeutralBonus.value} {Groups.Neutral.value} 🤭",
            show_alert=True)

    await call.message.delete()

    await _send_user_info(call.message, opened_user_id)


@dp.callback_query_handler(set_user_negative_callback.filter(), UserFilter(only_managers=True))
async def process_set_user_negative(call: types.CallbackQuery, callback_data: dict):
    opened_user_id = callback_data.get('opened_user_id')
    opened_user = UserLogics().get_by_id(opened_user_id)
    try:
        UserLogics().set_group_negative(opened_user)
        await call.answer(
            f'The user has been set to {DefaultInlineButtons.NegativeBonus.value} {Groups.Negative.value} group!',
            show_alert=True)
    except UserAlreadyNegativeError:
        await call.answer(
            f"Ups, the user group is already {DefaultInlineButtons.NegativeBonus.value} {Groups.Negative.value} 🤭",
            show_alert=True)

    await call.message.delete()

    await _send_user_info(call.message, opened_user_id)


@dp.message_handler(Text(DefaultKeyboardButtons.Profile.value), UserFilter())
async def process_open_profile(message: types.Message):
    user = UserLogics().get_by_chat_id(message.from_user.id)

    user_subscribed = await UserLogics().is_subscriber(bot=bot, chat_id=message.from_user.id)
    channel_str_link = f"<a href='{COMMUNITY_URL}'>Kanal</a>"
    site_str_link = f"<a href='{REGISTRATION_URL}'>Registration Link</a>"

    # site_id_clean = html_escape(user.site_id) if user.site_id else f"<i>Site ID’ni {site_str_link} üzerinden gir</i>"

    await message.answer(
        f"🌟: <b>{user.nickname if user.nickname else user.username}</b>\n" +
        # f"🃏: <b>{site_id_clean}</b>\n" +
        f"📣: <b>{'✅ Abone Olundu' if user_subscribed else f'📛 {channel_str_link} kanalımıza abone ol'}</b>",
        disable_web_page_preview=True,
        reply_markup=profile_keyboard() if user.is_manager or user.group == Groups.All.value else None
    )


@dp.callback_query_handler(text=CallbackQueryTypes.UpdateSiteID.value)
async def process_update_site_id(call: types.CallbackQuery):
    await call.message.answer(f"Site ID’ni gir", reply_markup=cancel_keyboard())
    await call.message.delete()
    await UpdateSiteID.send_side_id.set()


@dp.message_handler(state=UpdateSiteID.send_side_id)
async def process_write_site_id(message: types.Message, state: FSMContext):
    await state.finish()
    user = UserLogics.get_by_chat_id(message.from_user.id)
    user_input = message.text.strip()
    if len(user_input) <= 32 and user_input.isdigit():
        user.site_id = user_input
        user.save(only=(User.site_id,))
        await message.answer(f"Site ID başarıyla kaydedildi 😉" +
                             f"\n👉 Değiştirmen gerekirse, {DefaultKeyboardButtons.Profile.value} menüsünü ziyaret edebilirsin.",
                             reply_markup=main_menu_keyboard())
    else:
        await message.answer("Site ID sadece rakamlardan oluşmalı 😉", reply_markup=main_menu_keyboard())
