import logging
from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from bot.filters import UserFilter
from bot.keyboards.callback_datas import view_bonus_callback, enable_bonus_callback, disable_bonus_callback, \
    set_bonus_all_callback, set_bonus_vip_callback, set_bonus_negative_callback, set_bonus_neutral_callback, \
    set_bonus_positive_callback, group_display_dict, update_bonus_description_callback, update_bonus_image_url_callback, \
    delete_bonus_callback, bonuses_page_callback, delete_bonus_approve_callback, delete_bonus_cancel_callback, \
    set_bonus_not_for_request_callback, set_bonus_for_request_callback, set_bonus_for_request_cancel_callback, \
    set_bonus_for_request_approve_callback, set_bonus_not_for_request_cancel_callback, \
    set_bonus_not_for_request_approve_callback, enable_bonus_approve_callback, enable_bonus_cancel_callback, \
    disable_bonus_cancel_callback, disable_bonus_approve_callback, change_bonus_group_callback, \
    change_bonus_group_cancel_callback
from bot.keyboards.default import cancel_keyboard, manage_keyboard
from bot.keyboards.inline import bonus_keyboard, bonuses_navigation_keyboard, delete_bonus_confirmation_keyboard, \
    set_bonus_is_for_request_confirmation_keyboard, set_bonus_is_not_for_request_confirmation_keyboard, \
    enable_bonus_confirmation_keyboard, disable_bonus_confirmation_keyboard, change_bonus_group_keyboard
from bot.loader import dp, bot
from bot.states import UpdateBonusDescription, UpdateBonusImageURL
from common.constants import DefaultInlineButtons, Groups, DefaultKeyboardButtons, BonusRequestStatuses
from common.exceptions import BonusAlreadyEnabledError, BonusAlreadyDisabledError, BonusAlreadyNegativeError, \
    BonusAlreadyAllError, BonusAlreadyNeutralError, BonusAlreadyPositiveError, BonusAlreadyVipError, \
    BonusAlreadyRemovedError, BonusAlreadyRequestError, BonusAlreadyNotRequestError
from config import BONUSES_PER_PAGE
from logics import UserLogics, BonusLogics, BonusRequestLogics
from models import Bonus


# TODO: To remove after release patch
@dp.channel_post_handler()
async def handle_channel_post(message: types.Message):
    logging.debug(f"Private channel ID is: {message.chat.id}")


async def _send_bonus_info(user_id: str, bonus_id: str, is_requested: bool = False):
    user = UserLogics.get_by_chat_id(user_id)
    bonus = BonusLogics.get_by_id(bonus_id)

    if user.is_manager:
        bonus_image_url_link = f"<a href='{bonus.photo_url}'>THE LINK</a>"
        is_for_request_text = "Could be requested ⚙️💌" if bonus.is_request else "For info! No requests! ⚙️🪧"

        bonus_text_data = f"<b>Description</b>: {bonus.description}" \
                          f"\n<b>Group</b>: {group_display_dict.get(bonus.group)[0]}, {bonus.group}" \
                          f"\n<b>Request-able</b>: {is_for_request_text}" \
                          f"\n<b>Image URL</b>: {bonus_image_url_link if bonus.photo_url else ''}"

        if is_for_request_text:
            all_statuses_requests = BonusRequestLogics.get_list(bonus_id=bonus_id)
            canceled_requests = 0
            waiting_requests = 0
            approved_requests = 0
            for request in all_statuses_requests:
                if request.status == BonusRequestStatuses.Canceled.value:
                    canceled_requests += 1
                elif request.status == BonusRequestStatuses.Active.value:
                    waiting_requests += 1
                elif request.status == BonusRequestStatuses.Approved.value:
                    approved_requests += 1

            bonus_text_data += f"\n<b>Requests</b>: ⏰: {waiting_requests}, ❌: {canceled_requests}, ✅: {approved_requests}"
    else:
        bonus_text_data = f"{bonus.description}"

    if bonus.photo_url:
        await bot.send_photo(
            chat_id=int(user_id),
            photo=bonus.photo_url,
            caption=bonus_text_data,
            parse_mode="HTML",
            reply_markup=bonus_keyboard(
                bonus_id=bonus_id,
                is_for_request=bonus.is_request,
                is_bonus_active=bonus.is_active,
                current_group=bonus.group,
                is_manager=user.is_manager,
                is_requested=is_requested
            )
        )
    else:
        await bot.send_message(
            chat_id=int(user_id),
            text=bonus_text_data,
            parse_mode="HTML",
            reply_markup=bonus_keyboard(
                bonus_id=bonus_id,
                is_for_request=bonus.is_request,
                is_bonus_active=bonus.is_active,
                current_group=bonus.group,
                is_manager=user.is_manager,
                is_requested=is_requested
            )
        )


@dp.callback_query_handler(view_bonus_callback.filter(), UserFilter())
async def process_view_bonus(call: types.CallbackQuery, callback_data: dict):
    bonus_id = callback_data.get('bonus_id')
    bonus = BonusLogics.get_by_id(bonus_id)
    if bonus.is_removed:
        return
    await _send_bonus_info(call.from_user.id, bonus_id)


async def send_bonuses_page(message=None, call=None, user=None, page=1):
    bonuses, total = get_paginated_bonuses(user, page)

    if not bonuses:
        await (call.message if call else message).answer("Yeni bonuslar bekleniyor 👓")
        return

    for bonus in bonuses:
        is_requested = bool(len(BonusRequestLogics.get_list(user_id=user.id, bonus_id=bonus.id)))
        await _send_bonus_info(
            user_id=user.chat_id,
            bonus_id=bonus.id,
            is_requested=is_requested
        )
        await sleep(0.2)

    await (call.message if call else message).answer(
        text=f"Sayfa {page}",
        reply_markup=bonuses_navigation_keyboard(page=page, total=total)
    )


@dp.message_handler(Text(DefaultKeyboardButtons.Bonuses.value), UserFilter())
async def process_open_my_bonuses(message: types.Message):
    user = UserLogics().get_by_chat_id(message.from_user.id)
    await send_bonuses_page(message=message, user=user, page=1)


def get_paginated_bonuses(user, page: int):
    if user.is_manager:
        all_bonuses = BonusLogics.get_list(is_removed=False)
    else:
        all_bonuses = BonusLogics.get_list(is_active=True, is_removed=False)
        all_bonuses = [bonus for bonus in all_bonuses if bonus.group == user.group or bonus.group == Groups.All.value]

    total = len(all_bonuses)
    start = (page - 1) * BONUSES_PER_PAGE
    end = start + BONUSES_PER_PAGE
    return all_bonuses[start:end], total


@dp.callback_query_handler(bonuses_page_callback.filter())
async def process_bonuses_pagination(call: types.CallbackQuery, callback_data: dict):
    page = int(callback_data["page"])
    user = UserLogics().get_by_chat_id(call.from_user.id)
    await send_bonuses_page(call=call, user=user, page=page)
    await call.answer()


@dp.callback_query_handler(change_bonus_group_callback.filter(), UserFilter(only_managers=True))
async def process_change_bonus_group_callback(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    bonus_id = callback_data.get('bonus_id')
    bonus = BonusLogics.get_by_id(bonus_id)
    await state.update_data(bonus_id=bonus_id)

    await call.message.answer(f"Select new group for the bonus",
                              reply_markup=change_bonus_group_keyboard(bonus_id=bonus_id,
                                                                       current_group=bonus.group))
    await call.message.delete()


@dp.callback_query_handler(change_bonus_group_cancel_callback.filter(), UserFilter(only_managers=True))
async def process_change_bonus_group_cancel_callback(call: types.CallbackQuery, callback_data: dict):
    bonus_id = callback_data.get("bonus_id")

    await call.message.answer(
        f"Huh, the bonus group was not changed 😌",
        reply_markup=manage_keyboard())
    await _send_bonus_info(call.from_user.id, bonus_id)

    await call.message.delete()
    await sleep(0.5)


@dp.callback_query_handler(enable_bonus_callback.filter(), UserFilter(only_managers=True))
async def process_enable_bonus(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    bonus_id = callback_data.get('bonus_id')
    await state.update_data(bonus_id=bonus_id)

    await call.message.answer(f"Are you sure you want to enable the bonus? ⚠️",
                              reply_markup=enable_bonus_confirmation_keyboard(bonus_id=bonus_id))
    await call.message.delete()


@dp.callback_query_handler(enable_bonus_cancel_callback.filter(), UserFilter(only_managers=True))
async def process_enable_bonus_cancel(call: types.CallbackQuery, callback_data: dict):
    bonus_id = callback_data.get("bonus_id")

    await call.message.answer(
        f"Huh, the bonus was not enabled 😌",
        reply_markup=manage_keyboard())
    await _send_bonus_info(call.from_user.id, bonus_id)

    await call.message.delete()
    await sleep(0.5)


@dp.callback_query_handler(enable_bonus_approve_callback.filter(), UserFilter(only_managers=True))
async def process_enable_bonus_approve(call: types.CallbackQuery, callback_data: dict):
    bonus_id = callback_data.get("bonus_id")
    bonus = BonusLogics.get_by_id(bonus_id)
    try:
        BonusLogics.enable(bonus)
        await call.answer('The bonus has been enabled!', show_alert=True)

    except (BonusAlreadyEnabledError,):
        await call.answer("Ups, the bonus already has been enabled 🤭", show_alert=True)

    await call.message.delete()
    await process_view_bonus(call, {"bonus_id": bonus_id})


@dp.callback_query_handler(disable_bonus_callback.filter(), UserFilter(only_managers=True))
async def process_disable_bonus(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    bonus_id = callback_data.get('bonus_id')
    await state.update_data(bonus_id=bonus_id)

    await call.message.answer(f"Are you sure you want to disable the bonus? ⚠️",
                              reply_markup=disable_bonus_confirmation_keyboard(bonus_id=bonus_id))
    await call.message.delete()


@dp.callback_query_handler(disable_bonus_cancel_callback.filter(), UserFilter(only_managers=True))
async def process_disable_bonus_cancel(call: types.CallbackQuery, callback_data: dict):
    bonus_id = callback_data.get("bonus_id")

    await call.message.answer(
        f"Huh, the bonus was not disabled 😌",
        reply_markup=manage_keyboard())
    await _send_bonus_info(call.from_user.id, bonus_id)

    await call.message.delete()
    await sleep(0.5)


@dp.callback_query_handler(disable_bonus_approve_callback.filter(), UserFilter(only_managers=True))
async def process_disable_bonus_approve(call: types.CallbackQuery, callback_data: dict):
    bonus_id = callback_data.get("bonus_id")
    bonus = BonusLogics.get_by_id(bonus_id)
    try:
        BonusLogics.disable(bonus)
        await call.answer('The bonus has been disabled!', show_alert=True)

    except (BonusAlreadyDisabledError,):
        await call.answer("Ups, the bonus already has been disabled 🤭", show_alert=True)

    await call.message.delete()
    await process_view_bonus(call, {"bonus_id": bonus_id})


@dp.callback_query_handler(set_bonus_all_callback.filter(), UserFilter(only_managers=True))
async def process_set_bonus_all(call: types.CallbackQuery, callback_data: dict):
    bonus_id = callback_data.get('bonus_id')
    bonus = BonusLogics.get_by_id(bonus_id)
    try:
        BonusLogics.set_group_all(bonus)
        await call.answer(f'The bonus has been set to {DefaultInlineButtons.AllBonus.value} {Groups.All.value} group!',
                          show_alert=True)

    except (BonusAlreadyAllError,):
        await call.answer(f"Ups, the bonus group is already {DefaultInlineButtons.AllBonus.value} {Groups.All.value} 🤭",
                          show_alert=True)

    await call.message.delete()
    await process_view_bonus(call, {"bonus_id": bonus_id})


@dp.callback_query_handler(set_bonus_negative_callback.filter(), UserFilter(only_managers=True))
async def process_set_bonus_negative(call: types.CallbackQuery, callback_data: dict):
    bonus_id = callback_data.get('bonus_id')
    bonus = BonusLogics.get_by_id(bonus_id)
    try:
        BonusLogics.set_group_negative(bonus)
        await call.answer(f'The bonus has been set to {DefaultInlineButtons.NegativeBonus.value} {Groups.Negative.value} group!',
                          show_alert=True)

    except (BonusAlreadyNegativeError,):
        await call.answer(f"Ups, the bonus group is already {DefaultInlineButtons.NegativeBonus.value} {Groups.Negative.value} 🤭",
                          show_alert=True)

    await call.message.delete()
    await process_view_bonus(call, {"bonus_id": bonus_id})


@dp.callback_query_handler(set_bonus_neutral_callback.filter(), UserFilter(only_managers=True))
async def process_set_bonus_neutral(call: types.CallbackQuery, callback_data: dict):
    bonus_id = callback_data.get('bonus_id')
    bonus = BonusLogics.get_by_id(bonus_id)
    try:
        BonusLogics.set_group_neutral(bonus)
        await call.answer(f'The bonus has been set to {DefaultInlineButtons.NeutralBonus.value} {Groups.Neutral.value} group!',
                          show_alert=True)

    except (BonusAlreadyNeutralError,):
        await call.answer(f"Ups, the bonus group is already {DefaultInlineButtons.NeutralBonus.value} {Groups.Neutral.value} 🤭",
                          show_alert=True)

    await call.message.delete()
    await process_view_bonus(call, {"bonus_id": bonus_id})


@dp.callback_query_handler(set_bonus_positive_callback.filter(), UserFilter(only_managers=True))
async def process_set_bonus_positive(call: types.CallbackQuery, callback_data: dict):
    bonus_id = callback_data.get('bonus_id')
    bonus = BonusLogics.get_by_id(bonus_id)
    try:
        BonusLogics.set_group_positive(bonus)
        await call.answer(f'The bonus has been set to {DefaultInlineButtons.PositiveBonus.value} {Groups.Positive.value} group!',
                          show_alert=True)

    except (BonusAlreadyPositiveError,):
        await call.answer(f"Ups, the bonus group is already {DefaultInlineButtons.PositiveBonus.value} {Groups.Positive.value} 🤭",
                          show_alert=True)

    await call.message.delete()
    await process_view_bonus(call, {"bonus_id": bonus_id})


@dp.callback_query_handler(set_bonus_vip_callback.filter(), UserFilter(only_managers=True))
async def process_set_bonus_vip(call: types.CallbackQuery, callback_data: dict):
    bonus_id = callback_data.get('bonus_id')
    bonus = BonusLogics.get_by_id(bonus_id)
    try:
        BonusLogics.set_group_vip(bonus)
        await call.answer(f'The bonus has been set to {DefaultInlineButtons.VIPBonus.value} {Groups.Vip.value} group!',
                          show_alert=True)

    except (BonusAlreadyVipError,):
        await call.answer(f"Ups, the bonus group is already {DefaultInlineButtons.VIPBonus.value} {Groups.Vip.value} 🤭",
                          show_alert=True)

    await call.message.delete()
    await process_view_bonus(call, {"bonus_id": bonus_id})


@dp.callback_query_handler(update_bonus_description_callback.filter(), UserFilter(only_managers=True))
async def process_update_bonus_description(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    bonus_id = callback_data.get("bonus_id")
    await state.update_data(bonus_id=bonus_id)

    await call.message.answer(f"Enter new bonus description (>1000 symbols)👉:", reply_markup=cancel_keyboard())
    await call.message.delete()
    await UpdateBonusDescription.send_bonus_description.set()


@dp.message_handler(state=UpdateBonusDescription.send_bonus_description)
async def process_confirm_bonus_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    bonus_id = data.get("bonus_id")
    await state.finish()

    bonus = BonusLogics.get_by_id(bonus_id)
    new_bonus_description = message.text
    if len(new_bonus_description) < 1000:
        bonus.description = new_bonus_description
        bonus.save(only=(Bonus.description,))
        await message.answer(f"The new bonus description was successfully saved 😉",
                             reply_markup=manage_keyboard())
    else:
        await message.answer("The bonus description must be less then 1000 characters 😉",
                             reply_markup=manage_keyboard())

    await _send_bonus_info(message.from_user.id, bonus_id)


@dp.callback_query_handler(update_bonus_image_url_callback.filter(), UserFilter(only_managers=True))
async def process_update_image_url(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    bonus_id = callback_data.get("bonus_id")
    await state.update_data(bonus_id=bonus_id)

    await call.message.answer(f"Enter new bonus image URL (>250 symbols)👉:", reply_markup=cancel_keyboard())
    await call.message.delete()
    await UpdateBonusImageURL.send_bonus_image_url.set()


@dp.message_handler(state=UpdateBonusImageURL.send_bonus_image_url)
async def process_confirm_bonus_image_url(message: types.Message, state: FSMContext):
    data = await state.get_data()
    bonus_id = data.get("bonus_id")
    await state.finish()

    bonus = BonusLogics.get_by_id(bonus_id)
    new_bonus_image_url = message.text
    if len(new_bonus_image_url) < 250:
        bonus.photo_url = new_bonus_image_url
        bonus.save(only=(Bonus.photo_url,))
        await message.answer(f"The new bonus image URL was successfully saved 😉",
                             reply_markup=manage_keyboard())
    else:
        await message.answer("The bonus image URL must be less then 250 characters 😉",
                             reply_markup=manage_keyboard())

    await _send_bonus_info(message.from_user.id, bonus_id)


@dp.callback_query_handler(delete_bonus_callback.filter(), UserFilter(only_managers=True))
async def process_delete_bonus(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    bonus_id = callback_data.get("bonus_id")
    await state.update_data(bonus_id=bonus_id)

    await call.message.answer(f"Are you sure you want to remove the bonus? ⚠️",
                              reply_markup=delete_bonus_confirmation_keyboard(bonus_id=bonus_id))
    await call.message.delete()


@dp.callback_query_handler(delete_bonus_approve_callback.filter(), UserFilter(only_managers=True))
async def process_delete_bonus_approve(call: types.CallbackQuery, callback_data: dict):
    bonus_id = callback_data.get("bonus_id")
    bonus = BonusLogics.get_by_id(bonus_id)
    try:
        BonusLogics.set_bonus_removed(bonus)
        await call.message.answer(
            f'The bonus has been removed 😈',
            reply_markup=manage_keyboard())

    except (BonusAlreadyRemovedError,):
        await call.message.answer(
            f"Ups, the bonus is already removed 🤭",
            reply_markup=manage_keyboard())

    await call.message.delete()
    await sleep(0.5)


@dp.callback_query_handler(delete_bonus_cancel_callback.filter(), UserFilter(only_managers=True))
async def process_delete_bonus_cancel(call: types.CallbackQuery, callback_data: dict):
    bonus_id = callback_data.get("bonus_id")

    await call.message.answer(
        f"Huh, the bonus was not removed 😌",
        reply_markup=manage_keyboard())
    await _send_bonus_info(call.from_user.id, bonus_id)

    await call.message.delete()
    await sleep(0.5)


@dp.callback_query_handler(set_bonus_for_request_callback.filter(), UserFilter(only_managers=True))
async def process_set_bonus_is_for_request(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    bonus_id = callback_data.get('bonus_id')
    await state.update_data(bonus_id=bonus_id)

    await call.message.answer(f"Are you sure you want to make the bonus for requests? ⚠️",
                              reply_markup=set_bonus_is_for_request_confirmation_keyboard(bonus_id=bonus_id))
    await call.message.delete()


@dp.callback_query_handler(set_bonus_for_request_cancel_callback.filter(), UserFilter(only_managers=True))
async def process_set_bonus_for_request_cancel(call: types.CallbackQuery, callback_data: dict):
    bonus_id = callback_data.get("bonus_id")

    await call.message.answer(
        f"Huh, the bonus was not set for requests 😌",
        reply_markup=manage_keyboard())
    await _send_bonus_info(call.from_user.id, bonus_id)

    await call.message.delete()
    await sleep(0.5)


@dp.callback_query_handler(set_bonus_for_request_approve_callback.filter(), UserFilter(only_managers=True))
async def process_set_bonus_for_request_approve(call: types.CallbackQuery, callback_data: dict):
    bonus_id = callback_data.get("bonus_id")
    bonus = BonusLogics.get_by_id(bonus_id)
    try:
        BonusLogics.set_as_request(bonus)
        await call.answer('The bonus is for requests for now ⚙️💌', show_alert=True)

    except (BonusAlreadyRequestError,):
        await call.answer("Ups, the bonus already has been set for requests 🤭", show_alert=True)

    await call.message.delete()
    await process_view_bonus(call, {"bonus_id": bonus_id})


@dp.callback_query_handler(set_bonus_not_for_request_callback.filter(), UserFilter(only_managers=True))
async def process_set_bonus_not_for_request(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    bonus_id = callback_data.get('bonus_id')
    await state.update_data(bonus_id=bonus_id)

    await call.message.answer(f"Are you sure you want to make the bonus just for information? ⚠️",
                              reply_markup=set_bonus_is_not_for_request_confirmation_keyboard(bonus_id=bonus_id))
    await call.message.delete()


@dp.callback_query_handler(set_bonus_not_for_request_cancel_callback.filter(), UserFilter(only_managers=True))
async def process_set_bonus_not_for_request_cancel(call: types.CallbackQuery, callback_data: dict):
    bonus_id = callback_data.get("bonus_id")

    await call.message.answer(
        f"Huh, the bonus was not set for just information 😌",
        reply_markup=manage_keyboard())
    await _send_bonus_info(call.from_user.id, bonus_id)

    await call.message.delete()
    await sleep(0.5)


@dp.callback_query_handler(set_bonus_not_for_request_approve_callback.filter(), UserFilter(only_managers=True))
async def process_set_bonus_not_for_request_approve(call: types.CallbackQuery, callback_data: dict):
    bonus_id = callback_data.get("bonus_id")
    bonus = BonusLogics.get_by_id(bonus_id)
    try:
        BonusLogics.set_not_request(bonus)
        await call.answer('The bonus is for Info only for now ⚙️🪧', show_alert=True)

    except (BonusAlreadyNotRequestError,):
        await call.answer("Ups, the bonus already has been set for Info 🤭", show_alert=True)

    await call.message.delete()
    await process_view_bonus(call, {"bonus_id": bonus_id})
