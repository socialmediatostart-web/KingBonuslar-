from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from common.constants import DefaultKeyboardButtons


def main_menu_keyboard():
    keyboard = [
        [
            KeyboardButton(DefaultKeyboardButtons.BonusTransfer.value),
        ],
        [
            KeyboardButton(DefaultKeyboardButtons.Profile.value),
            KeyboardButton(DefaultKeyboardButtons.BonusRequests.value)
        ],
        [
            KeyboardButton(DefaultKeyboardButtons.Bonuses.value),
            KeyboardButton(DefaultKeyboardButtons.Invite.value)
        ],
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


def manage_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(DefaultKeyboardButtons.ReportsGeneration.value),
                KeyboardButton(DefaultKeyboardButtons.CreateBonus.value)
            ],
            [
                KeyboardButton(DefaultKeyboardButtons.ViewUser.value),
                KeyboardButton(DefaultKeyboardButtons.ViewUsersPerGroup.value),
                KeyboardButton(DefaultKeyboardButtons.AllBonusRequests.value)
            ],
            [
                KeyboardButton(DefaultKeyboardButtons.SendMessageToOne.value),
                KeyboardButton(DefaultKeyboardButtons.SendMessageToGroup.value),
                KeyboardButton(DefaultKeyboardButtons.SendMessageToAll.value)
            ],
            [
                KeyboardButton(DefaultKeyboardButtons.Cancel.value)
            ]
        ],
        resize_keyboard=True
    )


def cancel_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(DefaultKeyboardButtons.Cancel.value)
            ]
        ],
        resize_keyboard=True
    )
