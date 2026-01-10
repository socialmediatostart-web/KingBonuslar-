from aiogram.dispatcher.filters.state import StatesGroup, State


class SendMessageToAll(StatesGroup):
    send_message = State()


class SendMessageToGroup(StatesGroup):
    send_message = State()


class SendPersonalMessage(StatesGroup):
    send_message = State()


class CreateNewBonus(StatesGroup):
    send_bonus_description = State()


class UpdateBonusDescription(StatesGroup):
    send_bonus_description = State()


class UpdateBonusImageURL(StatesGroup):
    send_bonus_image_url = State()


class ApproveBonusRequest(StatesGroup):
    send_bonus_request = State()


class SendChatID(StatesGroup):
    send_chat_id = State()


class MessageUser(StatesGroup):
    send_message = State()


class SendBonusToUser(StatesGroup):
    send_bonus = State()


class ViewUser(StatesGroup):
    send_chat_id = State()


class ViewUsersPerGroup(StatesGroup):
    send_group = State()


class SendMessageToOne(StatesGroup):
    send_message = State()


class UpdateSiteID(StatesGroup):
    send_side_id = State()
