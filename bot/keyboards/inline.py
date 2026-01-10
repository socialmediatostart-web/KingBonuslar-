from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from bot.keyboards.callback_datas import *
from common.constants import CallbackQueryTypes, InlineQueryTypes, DefaultInlineButtons, BonusRequestRejectReasons, \
    bonus_request_icon_dict, DefaultKeyboardButtons
from config import BONUSES_PER_PAGE, BONUS_REQUESTS_PER_PAGE, ALL_BONUS_REQUESTS_PER_PAGE, USERS_PER_PAGE, \
    BONUS_TRANSFER_URL


def share_keyboard():
    inline_keyboard = [
        [
            InlineKeyboardButton(text=f'{DefaultInlineButtons.SendInvite.value}', switch_inline_query=InlineQueryTypes.Invite.value),
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


def invite_keyboard(url: str):
    inline_keyboard = [
        [
            InlineKeyboardButton(text=f'{DefaultInlineButtons.AcceptInvite.value}', url=url),
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


def send_bonus_2_group_confirmation_keyboard(bonus_id: str, current_group: str):
    inline_keyboard = [
        [
            InlineKeyboardButton(text=f'{DefaultInlineButtons.Confirm.value}',
                                 callback_data=send_bonus_2_group_approve_callback.new(
                                     bonus_id=bonus_id,
                                     current_group=current_group
                                 )),
            InlineKeyboardButton(text=f'{DefaultInlineButtons.Cancel.value}',
                                 callback_data=send_bonus_2_group_cancel_callback.new(
                                     bonus_id=bonus_id,
                                     current_group=current_group
                                 ))
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


def block_user_confirmation_keyboard(opened_user_id: str):
    inline_keyboard = [
        [
            InlineKeyboardButton(text=f'{DefaultInlineButtons.Confirm.value}',
                                 callback_data=block_user_approve_callback.new(
                                     opened_user_id=opened_user_id
                                 )),
            InlineKeyboardButton(text=f'{DefaultInlineButtons.Cancel.value}',
                                 callback_data=block_user_cancel_callback.new(
                                     opened_user_id=opened_user_id
                                 ))
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


def unblock_user_confirmation_keyboard(opened_user_id: str):
    inline_keyboard = [
        [
            InlineKeyboardButton(text=f'{DefaultInlineButtons.Confirm.value}',
                                 callback_data=unblock_user_approve_callback.new(
                                     opened_user_id=opened_user_id
                                 )),
            InlineKeyboardButton(text=f'{DefaultInlineButtons.Cancel.value}',
                                 callback_data=unblock_user_cancel_callback.new(
                                     opened_user_id=opened_user_id
                                 ))
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


def activate_bonus_request_confirmation_keyboard(bonus_request_id: str):
    inline_keyboard = [
        [
            InlineKeyboardButton(text=f'{DefaultInlineButtons.Confirm.value}',
                                 callback_data=activate_br_approve_callback.new(
                                     bonus_request_id=bonus_request_id
                                 )),
            InlineKeyboardButton(text=f'{DefaultInlineButtons.Cancel.value}',
                                 callback_data=activate_br_cancel_callback.new(
                                     bonus_request_id=bonus_request_id
                                 ))
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


def personal_message_confirmation_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=DefaultInlineButtons.Confirm.value,
                callback_data=approve_personal_message_callback.new()
            ),
            InlineKeyboardButton(
                text=DefaultInlineButtons.Cancel.value,
                callback_data=cancel_personal_message_callback.new()
            )
        ]
    ])


def group_message_confirmation_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=DefaultInlineButtons.Confirm.value,
                callback_data=approve_group_message_callback.new()
            ),
            InlineKeyboardButton(
                text=DefaultInlineButtons.Cancel.value,
                callback_data=cancel_group_message_callback.new()
            )
        ]
    ])


def all_message_confirmation_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=DefaultInlineButtons.Confirm.value,
                                 callback_data=approve_all_message_callback.new()),
            InlineKeyboardButton(text=DefaultInlineButtons.Cancel.value,
                                 callback_data=cancel_all_message_callback.new())
        ]
    ])


def by_chat_id_message_confirmation_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=DefaultInlineButtons.Confirm.value,
                callback_data=approve_by_chat_id_message_callback.new()
            ),
            InlineKeyboardButton(
                text=DefaultInlineButtons.Cancel.value,
                callback_data=cancel_by_chat_id_message_callback.new()
            )
        ]
    ])


def approve_bonus_request_confirmation_keyboard(bonus_request_id: str):
    inline_keyboard = [
        [
            InlineKeyboardButton(text=f'{DefaultInlineButtons.Confirm.value}',
                                 callback_data=approve_br_approve_callback.new(
                                     bonus_request_id=bonus_request_id
                                 )),
            InlineKeyboardButton(text=f'{DefaultInlineButtons.Cancel.value}',
                                 callback_data=approve_br_cancel_callback.new(
                                     bonus_request_id=bonus_request_id
                                 ))
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


def cancel_bonus_request_options_keyboard(bonus_request_id: str):
    inline_keyboard = []

    for reason in BonusRequestRejectReasons.keys():
        button = InlineKeyboardButton(
            text=f'{reason}',
            callback_data=cancel_br_approve_opt_callback.new(
                bonus_request_id=bonus_request_id,
                reject_reason=reason
            )
        )
        inline_keyboard.append([button])

    cancel_button = InlineKeyboardButton(
        text=f'{DefaultInlineButtons.Cancel.value}',
        callback_data=cancel_br_cancel_callback.new(
            bonus_request_id=bonus_request_id
        )
    )
    inline_keyboard.append([cancel_button])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def cancel_bonus_request_confirmation_keyboard(bonus_request_id: str):
    inline_keyboard = [
        [
            InlineKeyboardButton(text=f'{DefaultInlineButtons.Confirm.value}',
                                 callback_data=cancel_br_approve_callback.new(
                                     bonus_request_id=bonus_request_id
                                 )),
            InlineKeyboardButton(text=f'{DefaultInlineButtons.Cancel.value}',
                                 callback_data=cancel_br_cancel_callback.new(
                                     bonus_request_id=bonus_request_id
                                 ))
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


def delete_bonus_confirmation_keyboard(bonus_id: str):
    inline_keyboard = [
        [
            InlineKeyboardButton(text=f'{DefaultInlineButtons.Confirm.value}',
                                 callback_data=delete_bonus_approve_callback.new(
                                     bonus_id=bonus_id
                                 )),
            InlineKeyboardButton(text=f'{DefaultInlineButtons.Cancel.value}',
                                 callback_data=delete_bonus_cancel_callback.new(
                                     bonus_id=bonus_id
                                 ))
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


def set_bonus_is_for_request_confirmation_keyboard(bonus_id: str):
    inline_keyboard = [
        [
            InlineKeyboardButton(text=f'{DefaultInlineButtons.Confirm.value}',
                                 callback_data=set_bonus_for_request_approve_callback.new(
                                     bonus_id=bonus_id
                                 )),
            InlineKeyboardButton(text=f'{DefaultInlineButtons.Cancel.value}',
                                 callback_data=set_bonus_for_request_cancel_callback.new(
                                     bonus_id=bonus_id
                                 ))
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


def select_bonus_request_filter_keyboard(bonus_id=''):
    inline_keyboard = []
    for k, v in bonus_request_icon_dict.items():
        button = InlineKeyboardButton(text=f'{v}',
                                      callback_data=bonus_request_status_filter_callback.new(
                                          bonus_request_status=k, bonus_id=bonus_id
                                      ))
        inline_keyboard.append([button])

    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )



def enable_bonus_confirmation_keyboard(bonus_id: str):
    inline_keyboard = [
        [
            InlineKeyboardButton(text=f'{DefaultInlineButtons.Confirm.value}',
                                 callback_data=enable_bonus_approve_callback.new(
                                     bonus_id=bonus_id
                                 )),
            InlineKeyboardButton(text=f'{DefaultInlineButtons.Cancel.value}',
                                 callback_data=enable_bonus_cancel_callback.new(
                                     bonus_id=bonus_id
                                 ))
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


def disable_bonus_confirmation_keyboard(bonus_id: str):
    inline_keyboard = [
        [
            InlineKeyboardButton(text=f'{DefaultInlineButtons.Confirm.value}',
                                 callback_data=disable_bonus_approve_callback.new(
                                     bonus_id=bonus_id
                                 )),
            InlineKeyboardButton(text=f'{DefaultInlineButtons.Cancel.value}',
                                 callback_data=disable_bonus_cancel_callback.new(
                                     bonus_id=bonus_id
                                 ))
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


def set_bonus_is_not_for_request_confirmation_keyboard(bonus_id: str):
    inline_keyboard = [
        [
            InlineKeyboardButton(text=f'{DefaultInlineButtons.Confirm.value}',
                                 callback_data=set_bonus_not_for_request_approve_callback.new(
                                     bonus_id=bonus_id
                                 )),
            InlineKeyboardButton(text=f'{DefaultInlineButtons.Cancel.value}',
                                 callback_data=set_bonus_not_for_request_cancel_callback.new(
                                     bonus_id=bonus_id
                                 ))
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


def community_keyboard(url):
    inline_keyboard = [
        [
            InlineKeyboardButton(text=f'{DefaultInlineButtons.EnterCommunity.value}', url=url),
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


def profile_keyboard():
    inline_keyboard = [
        [
            InlineKeyboardButton(text=f'{DefaultInlineButtons.ChangeSiteID.value}',
                                 callback_data=CallbackQueryTypes.UpdateSiteID.value)
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


def message_inline_button_keyboard(button_url: str):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(text=DefaultInlineButtons.LearMore.value, url=button_url.strip())
    )


def bonus_transfer_inline_button_keyboard():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text=DefaultKeyboardButtons.BonusTransfer.value,
            web_app=WebAppInfo(url=BONUS_TRANSFER_URL)
        )
    )


def message_group_keyboard():
    inline_keyboard = [
        [
            InlineKeyboardButton(text=f'{data[0]}',
                                 callback_data=send_message_to_group_callback.new(group=g_key))
            for g_key, data in group_display_dict.items()
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


def open_users_per_group_keyboard():
    inline_keyboard = [
        [
            InlineKeyboardButton(text=f'{data[0]}',
                                 callback_data=open_users_per_group_callback.new(group=g_key))
            for g_key, data in group_display_dict.items()
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


def user_keyboard(opened_user_id: str, is_opened_user_blocked: bool):
    manage_buttons = [InlineKeyboardButton(text=f'{DefaultInlineButtons.MessageUser.value}',
                                           callback_data=message_user_callback.new(opened_user_id=opened_user_id)),
                      InlineKeyboardButton(text=f'{DefaultInlineButtons.SetUserGroup.value}',
                                           callback_data=change_user_group_callback.new(opened_user_id=opened_user_id))
                      ]
    if not is_opened_user_blocked:
        manage_buttons.append(InlineKeyboardButton(text=f'{DefaultInlineButtons.BlockUser.value}',
                                                   callback_data=block_user_callback.new(opened_user_id=opened_user_id)))
    else:
        manage_buttons.append(InlineKeyboardButton(text=f'{DefaultInlineButtons.UnblockUser.value}',
                                                   callback_data=unblock_user_callback.new(
                                                       opened_user_id=opened_user_id)))
    inline_keyboard = [manage_buttons]

    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


def users_navigation_keyboard(group, page: int, total: int):
    max_page = (total + USERS_PER_PAGE - 1) // USERS_PER_PAGE
    buttons = []

    if page > 1:
        buttons.append(InlineKeyboardButton(
            DefaultInlineButtons.Previous.value,
            callback_data=users_page_callback.new(group=group, page=page - 1)
        ))
    if page < max_page:
        buttons.append(InlineKeyboardButton(
            DefaultInlineButtons.Next.value,
            callback_data=users_page_callback.new(group=group, page=page + 1)
        ))

    buttons.append(InlineKeyboardButton(DefaultInlineButtons.Close.value, callback_data="cancel"))

    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.row(*buttons)

    return keyboard


def view_bonus_keyboard(bonus_id: str):
    inline_keyboard = [
        [
            InlineKeyboardButton(text=f'{DefaultInlineButtons.ViewBonus.value}',
                                 callback_data=view_bonus_callback.new(bonus_id=bonus_id))
        ]
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


def bonus_request_keyboard(bonus_id: str, bonus_request_id: str,
                           request_is_active: bool, user_id: str,
                           is_manager: bool = False):
    inline_keyboard = [
            ]
    manager_buttons = []

    if is_manager:
        manager_buttons.append(
            InlineKeyboardButton(text=f'{DefaultInlineButtons.OpenUser.value}',
                                 callback_data=open_user_callback.new(
                                    user_id=user_id)))
        manager_buttons.append(
            InlineKeyboardButton(text=f'{DefaultInlineButtons.ViewBonus.value}',
                                 callback_data=view_bonus_callback.new(
                                     bonus_id=bonus_id))
            )
        if request_is_active:
            inline_keyboard.append([
                InlineKeyboardButton(text=f'{DefaultInlineButtons.CancelBonus.value}',
                                     callback_data=cancel_bonus_request_callback.new(
                                         bonus_request_id=bonus_request_id)),
                InlineKeyboardButton(text=f'{DefaultInlineButtons.ApproveBonusRequest.value}',
                                     callback_data=approve_bonus_request_callback.new(
                                         bonus_request_id=bonus_request_id))])
        else:
            manager_buttons.append(

                    InlineKeyboardButton(text=f'{DefaultInlineButtons.Activate.value}',
                                         callback_data=activate_bonus_request_callback.new(
                                             bonus_request_id=bonus_request_id))
                )
        inline_keyboard.append(manager_buttons)
    else:

        inline_keyboard.append([InlineKeyboardButton(text=f'{DefaultInlineButtons.RefreshBonusRequest.value}',
                                                     callback_data=refresh_bonus_request_callback.new(
                                                         bonus_request_id=bonus_request_id))])

    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


def change_bonus_group_keyboard(bonus_id: str, current_group: str):
    bonus_group_buttons = []
    for i, v in group_display_dict.items():
        if i == current_group:
            pass
        else:
            bonus_group_buttons.append(InlineKeyboardButton(
                text=f'{v[0]}', callback_data=v[1].new(bonus_id=bonus_id)))

    inline_keyboard = list()
    inline_keyboard.append(bonus_group_buttons)
    inline_keyboard.append(
        [InlineKeyboardButton(text=f'{DefaultInlineButtons.Cancel.value}',
                              callback_data=change_bonus_group_cancel_callback.new(bonus_id=bonus_id))]
    )
    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


def change_user_group_keyboard(opened_user_id: str, current_group: str):
    user_group_buttons = []
    for i, v in user_group_display_dict.items():
        if i == current_group:
            pass
        else:
            user_group_buttons.append(InlineKeyboardButton(
                text=f'{v[0]}', callback_data=v[1].new(opened_user_id=opened_user_id)))

    inline_keyboard = list()
    inline_keyboard.append(user_group_buttons)
    inline_keyboard.append(
        [InlineKeyboardButton(text=f'{DefaultInlineButtons.Cancel.value}',
                              callback_data=change_user_group_cancel_callback.new(opened_user_id=opened_user_id))]
    )
    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


def bonus_keyboard(bonus_id: str, is_bonus_active: bool, current_group: str,
                   is_for_request: bool, is_manager: bool = False, is_requested=False):
    message_buttons = []
    inline_keyboard = []

    if is_for_request:
        if not is_requested:
            inline_keyboard.append([
                InlineKeyboardButton(text=f'{DefaultInlineButtons.RequestBonus.value}',
                                     callback_data=request_bonus_callback.new(bonus_id=bonus_id))
            ])
        else:
            inline_keyboard.append([InlineKeyboardButton(text=f'{DefaultInlineButtons.BonusAlreadyRequested.value}',
                                    callback_data=bonus_already_requested_callback.new(bonus_id=bonus_id))])

    if is_manager:
        if is_bonus_active:
            message_buttons.append(
                    InlineKeyboardButton(text=f'{DefaultInlineButtons.DisableBonus.value}',
                                         callback_data=disable_bonus_callback.new(bonus_id=bonus_id))
                )
        else:
            message_buttons.append(
                InlineKeyboardButton(text=f'{DefaultInlineButtons.EnableBonus.value}',
                                     callback_data=enable_bonus_callback.new(bonus_id=bonus_id))
            )
        if is_for_request:
            message_buttons.append(
                InlineKeyboardButton(text=DefaultInlineButtons.SetBonusNotForRequest.value,
                                     callback_data=set_bonus_not_for_request_callback.new(bonus_id=bonus_id))
            )
        else:
            message_buttons.append(
                InlineKeyboardButton(text=DefaultInlineButtons.SetBonusForRequest.value,
                                     callback_data=set_bonus_for_request_callback.new(bonus_id=bonus_id))
            )
        message_buttons.append(
                InlineKeyboardButton(text=f'{DefaultInlineButtons.SendBonusToUser.value}',
                                     callback_data=send_bonus_to_user_callback.new(bonus_id=bonus_id))
            )
        message_buttons.append(
                InlineKeyboardButton(text=f'{DefaultInlineButtons.SendBonusToGroup.value}',
                                     callback_data=send_bonus_to_group_callback.new(current_group=current_group,
                                                                                    bonus_id=bonus_id))
            )

        inline_keyboard.append(message_buttons)

        inline_keyboard.append([
            InlineKeyboardButton(text=f'{DefaultInlineButtons.UpdateBonusDescription.value}',
                                 callback_data=update_bonus_description_callback.new(bonus_id=bonus_id)),
            InlineKeyboardButton(text=f'{DefaultInlineButtons.UpdateBonusImageURL.value}',
                                 callback_data=update_bonus_image_url_callback.new(bonus_id=bonus_id)),
            InlineKeyboardButton(text=f'{DefaultInlineButtons.DeleteBonus.value}',
                                 callback_data=delete_bonus_callback.new(bonus_id=bonus_id)),
            InlineKeyboardButton(text=f'{DefaultInlineButtons.SetBonusGroup.value}',
                                 callback_data=change_bonus_group_callback.new(bonus_id=bonus_id))
        ])
        if is_for_request:
            inline_keyboard[-1].append(InlineKeyboardButton(
                text=f'{DefaultInlineButtons.GoToRequests.value}',
                callback_data=open_bonus_request_status_filter_callback.new(bonus_id=bonus_id)))

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def bonus_requests_navigation_keyboard(page: int, total: int):
    max_page = (total + BONUS_REQUESTS_PER_PAGE - 1) // BONUS_REQUESTS_PER_PAGE
    buttons = []

    if page > 1:
        buttons.append(InlineKeyboardButton(DefaultInlineButtons.Previous.value,
                                            callback_data=bonus_requests_page_callback.new(page=page - 1)))
    if page < max_page:
        buttons.append(InlineKeyboardButton(DefaultInlineButtons.Next.value,
                                            callback_data=bonus_requests_page_callback.new(page=page + 1)))

    buttons.append(InlineKeyboardButton("❌ Close", callback_data="cancel"))

    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.row(*buttons)

    return keyboard


def all_bonus_requests_navigation_keyboard(page: int, total: int):
    max_page = (total + ALL_BONUS_REQUESTS_PER_PAGE - 1) // ALL_BONUS_REQUESTS_PER_PAGE
    buttons = []

    if page > 1:
        buttons.append(InlineKeyboardButton(DefaultInlineButtons.Previous.value,
                                            callback_data=all_bonus_requests_page_callback.new(page=page - 1)))
    if page < max_page:
        buttons.append(InlineKeyboardButton(DefaultInlineButtons.Next.value,
                                            callback_data=all_bonus_requests_page_callback.new(page=page + 1)))
    # Practically deprecated
    # buttons.append(InlineKeyboardButton(DefaultInlineButtons.Close.value, callback_data="cancel"))

    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.row(*buttons)

    return keyboard


def bonuses_navigation_keyboard(page: int, total: int):
    max_page = (total + BONUSES_PER_PAGE - 1) // BONUSES_PER_PAGE
    buttons = []

    if page > 1:
        buttons.append(InlineKeyboardButton(DefaultInlineButtons.Previous.value,
                                            callback_data=bonuses_page_callback.new(page=page - 1)))
    if page < max_page:
        buttons.append(InlineKeyboardButton(DefaultInlineButtons.Next.value,
                                            callback_data=bonuses_page_callback.new(page=page + 1)))
    buttons.append(InlineKeyboardButton(DefaultInlineButtons.Close.value, callback_data="cancel"))
    keyboard = InlineKeyboardMarkup(row_width=3)  # 3 because max = Previous + Next + Close
    keyboard.row(*buttons)

    return keyboard


def paginate_history_keyboard(callback, page: int):
    row = []
    if page > 1:
        row.append(InlineKeyboardButton(text=f'{DefaultInlineButtons.Next.value}',
                                        callback_data=callback.new(page=page - 1)))
    row.append(InlineKeyboardButton(text=f'{DefaultInlineButtons.Previous.value}',
                                    callback_data=callback.new(page=page + 1)))

    return InlineKeyboardMarkup(
        inline_keyboard=[row, [InlineKeyboardButton(text=f'{DefaultInlineButtons.Close.value}',
                                                    callback_data=CallbackQueryTypes.Cancel.value)]])
