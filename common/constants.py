from enum import Enum, IntFlag

from config import TOP_REFERRAL_SOURCES_N

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
LOG_FORMAT = "%(asctime)s [%(thread)d:%(threadName)s] [%(levelname)s] - %(name)s:%(message)s"
BASE_58_SYMBOLS = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


class Groups(Enum):
    Negative = 'negative'
    Neutral = 'neutral'
    Positive = 'positive'
    Vip = 'vip'
    All = 'all'


class StorageIndexes(IntFlag):
    AdminPassword = 1


class BotCommands(Enum):
    Start = 'start'
    Help = 'help'
    Manage = 'm'


class BuiltInReferralSources(Enum):
    Telegram = 'telegram'
    User = 'user'


class DefaultInlineButtons(Enum):
    ChangeSiteID = "✏️ Site Kimliğini Güncelle"
    # Bonus Logic
    RequestBonus = "📲 Talep Et"
    BonusAlreadyRequested = "🚀 Bonus Talep Edildi"
    LearMore = "↪️ Aktif Et ↩️"
    RefreshBonusRequest = "🔄 Yenile"
    ApproveBonusRequest = "🛃 Approve"
    DisableBonus = "🔴 OFF"
    EnableBonus = "🟢 ON"
    SetBonusForRequest = "⚙️💌"
    SetBonusNotForRequest = "⚙️🪧"
    SetBonusGroup = "⚙️🟧"
    GoToRequests = "➡️💌"
    SendBonusToUser = "📬 👤"
    SendBonusToGroup = "📬 👥"
    AllBonus = "🟩"
    NegativeBonus = "⬛"
    NeutralBonus = "⬜"
    PositiveBonus = "🟨"
    VIPBonus = "🟧"
    UpdateBonusDescription = "✏️ Txt"
    UpdateBonusImageURL = "🖼️ Img"
    ViewBonus = "🔍 🎁"

    # User Buttons
    InputManually = "✍️ Manuel Gir"
    Invite = "✉️ Davet Et"
    SendInvite = "↖️️ Davet Gönder"
    AcceptInvite = "🔥️ Daveti Kabul Et"
    EnterCommunity = "💬 Katıl"
    # Helper Buttons
    Confirm = "✅ Confirm"
    Cancel = "❌ Cancel"
    JustReject = "⚰️ Just Reject"
    Close = "❌"
    DeleteBonus = "❌ Del"
    CancelBonus = "‍❌ Cancel"
    Back = "⬅️ Back"
    Activate = "✅ Activate"
    Next = "➡️"
    Previous = "⬅️"
    OpenUser = "🔍👤"
    MessageUser = "📩 Message"
    BlockUser = "⚰️ Block"
    UnblockUser = "👼 Unblock"
    SetUserGroup = "⚙️🟧"


class DefaultKeyboardButtons(Enum):
    Bonuses = "🎁 Bonuslar"
    Profile = "🤴🏻 Profil"
    BonusRequests = "💌 Bonus Talepleri"
    Invite = "📨 Arkadaşını Davet Et"
    Community = "💬 Kanalımız"
    BonusTransfer = "🧧 Deneme Bonus"
    Help = "⚙️ DESTEK"

    SendMessageToAll = "📩 👥"
    SendMessageToOne = "📩 👤"
    SendMessageToGroup = "📩 👥 🟧"
    CreateBonus = "⚙️ 🎁"
    AllBonuses = "🔍 🎁"
    AllBonusRequests = "🔍 ALL 💌"
    ReportsGeneration = "⚙️ 📊"
    ViewUser = "🔍 👤"
    ViewUserM = "🔍 👤"
    ViewUsersPerGroup = "🔍 👥 🟧"

    Cancel = "‍⬅️ İptal"


class InlineQueryTypes(Enum):
    Invite = 'invite'


BonusRequestRejectReasons = {
    "Invalid Site ID": "Profilinizin İD numarası geçerli değil.",
    "No subscription": "Kanalımıza abone değilsiniz.",
    "Already Received": "Bu bonus profilinizden daha önce alınmıştır.",
    "Just Reject": "."}


class CallbackQueryTypes(Enum):
    UpdateSiteID = 'update_site_id'
    Cancel = "cancel"
    # Bonus Logic
    ViewBonus = "view_bonus"
    DeleteBonus = "delete_bonus"
    SetBonusForRequest = "set_bonus_for_request"
    SetBonusForRequestCancel = "set_bonus_for_request_cancel"
    SetBonusForRequestApprove = "set_bonus_for_request_approve"
    SetBonusNotForRequestCancel = "set_bonus_not_for_request_cancel"
    SetBonusNotForRequestApprove = "set_bonus_not_for_request_approve"
    EnableBonusApprove = "enable_bonus_approve"
    EnableBonusCancel = "enable_bonus_cancel"
    DisableBonusCancel = "disable_bonus_cancel"
    DisableBonusApprove = "disable_bonus_approve"
    ChangeBonusGroup = "change_bonus_group"
    ChangeBonusGroupCancel = "change_bonus_group_cancel"
    SetBonusNotForRequest = "set_bonus_not_for_request"
    SendBonusToGroupApprove = "send_bonus_2_group_approve"
    SendBonusToGroupCancel = "send_bonus_2_group_cancel"
    DeleteBonusApprove = "delete_bonus_approve"
    DeleteBonusCancel = "delete_bonus_cancel"
    BlockUserApprove = "block_user_approve"
    BlockUserCancel = "block_user_cancel"
    UnblockUserApprove = "unblock_user_approve"
    UnblockUserCancel = "unblock_user_cancel"
    ActivateBonusRequestApprove = "activate_bonus_request_approve"
    ActivateBonusRequestCancel = "activate_bonus_request_cancel"
    ApproveBonusRequestApprove = "approve_bonus_request_approve"
    ApproveBonusRequestCancel = "approve_bonus_request_cancel"
    CancelBonusRequestApprove = "cancel_bonus_request_approve"
    CancelBonusRequestCancel = "cancel_bonus_request_cancel"
    BonusRequestStatusFilter = "bonus_request_status_filter"
    OpenBonusRequestStatusFilter = "open_bonus_request_status_filter"
    ApproveBonusRequestCancelOpt = "approve_br_cancel_opt"
    OpenUser = "open_user"
    DisableBonus = "disable_bonus"
    EnableBonus = "enable_bonus"
    SetBonusAll = "set_bonus_all"
    SetBonusNegative = "set_bonus_negative"
    SetBonusNeutral = "set_bonus_neutral"
    SetBonusPositive = "set_bonus_positive"
    SetBonusVIP = "set_bonus_vip"
    UpdateBonusDescription = "update_bonus_description"
    UpdateBonusImageURL = "update_bonus_image"
    # Bonus Request
    RequestBonus = "request_bonus"
    RefreshBonusRequest = "refresh_bonus_request"
    ApproveBonusRequest = "approve_bonus_request"
    ActivateBonusRequest = "activate_bonus_request"
    BonusAlreadyRequested = "bonus_already_requested"
    CancelBonusRequest = "cancel_bonus_request"
    # User
    CancelPersonalMessage = "cancel_personal_message"
    ApprovePersonalMessage = "approve_personal_message"
    ApproveGroupMessage = "approve_group_message"
    CancelGroupMessage = "cancel_group_message"
    ApproveAllMessage = "approve_all_message"
    CancelAllMessage = "cancel_all_message"
    ApproveByChatIDMessage = "ApproveByChatIDMessage"
    CancelByChatIDMessage = "CancelByChatIDMessage"
    SendMessageToGroup = "send_message_to_group"
    OpenUsersPerGroup = "open_users_per_group"
    SendBonusToGroup = "send_bonus_to_group"
    SendBonusToUser = "send_bonus_to_user"
    ChangeUserGroupCancel = "change_user_group_cancel"
    ChangeUserGroup = "change_user_group"
    SetUserNegative = "set_user_negative"
    SetUserNeutral = "set_user_neutral"
    SetUserPositive = "set_user_positive"
    SetUserVip = "set_user_vip"
    SetUserAll = "set_user_all"
    MessageUser = "message_user"
    BlockUser = "block_user"
    UnblockUser = "unblock_user"


class BonusRequestStatuses(Enum):
    Active = "active"
    Approved = "approved"
    Canceled = "canceled"


bonus_request_icon_dict = {
    "canceled": '🎈 İptal edildi',
    "approved": '🥳 Onaylandı',
    "active": '⏰ Onay Bekliyor'
}


class RequestReportTitles(Enum):
    request_created_at = "REQUEST CREATED"
    user_created_at = "USER CREATED"
    request_status = "REQUEST STATUS"
    tg_chat_id = "TG CHAT ID"
    site_id = "SITE ID"
    group = "GROUP"
    is_subscribed = "IS SUBSCRIBED"
    bonus_description = "BONUS DESCRIPTION"


class RequestReportTotalTitles(Enum):
    users_total = "Users Total"
    users_banned_or_disabled = "Users Banned or Disabled"
    users_with_bonus_request = "Users with Bonus Requests"
    users_with_rejected_bonus_requests = "Users with rejected Bonus Requests"
    users_with_waiting_bonus_requests = "Users with waiting Bonus Requests"
    users_with_approved_bonus_requests = "Users with approved Bonus Requests"
    bonus_request_total = "Bonus Requests Total"
    rejected_bonus_request_total = "Rejected Bonus Requests Total"
    waiting_bonus_request_total = "Waiting Bonus Requests Total"
    approved_bonus_request_total = "Approved Bonus Requests Total"
    # last 2 titles for a different row
    top_referral_sources = f"Top {TOP_REFERRAL_SOURCES_N} User Referral sources"
    referrals_count = "Referrals count:"
