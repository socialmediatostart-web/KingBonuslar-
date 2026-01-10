from typing import List

from peewee import ModelSelect, fn
from common.constants import BuiltInReferralSources, Groups
from common.exceptions import UserAlreadyNegativeError, UserAlreadyAllError, UserAlreadyNeutralError, \
    UserAlreadyPositiveError, UserAlreadyVipError, UserAlreadyBlockedError, UserAlreadyUnblockedError
from models import User, db
from aiogram import Bot
from aiogram.utils.exceptions import BadRequest
from config import CHANNEL_USERNAME, CHANNEL_ID


class UserLogics:
    @staticmethod
    def get_query() -> ModelSelect:
        query = User.select()
        return query

    @staticmethod
    def create(chat_id: int,
               username: str = None,
               nickname: str = None,
               site_id: str = None,
               referral_source: str = None,
               referral_user_id: str = None,
               is_manager: bool = None) -> User:
        user = User.create(
            chat_id=chat_id,
            username=username,
            nickname=nickname or username or chat_id,
            site_id=site_id,
            referral_source=referral_source or BuiltInReferralSources.Telegram.value,
            referral_user_id=referral_user_id,
            is_manager=is_manager
        )

        return user

    @classmethod
    def get_by_id(cls, pk: str) -> User:
        return cls.get_query().where(User.id == pk).first()

    @classmethod
    def get_group_list(cls, group: str) -> List:
        return list(cls.get_query().where(User.group == group))

    @classmethod
    def get_referral_users_list(cls, referral_user_id: str) -> List:
        return list(cls.get_query().where(User.referral_user_id == referral_user_id))

    @classmethod
    def block(cls, user) -> None:
        if not user:
            raise
        if user.is_blocked:
            raise UserAlreadyBlockedError

        with db.atomic():
            user.is_blocked = True
            user.save(only=(User.is_blocked,))

    @classmethod
    def unblock(cls, user) -> None:
        if not user:
            raise
        if not user.is_blocked:
            raise UserAlreadyUnblockedError

        with db.atomic():
            user.is_blocked = False
            user.save(only=(User.is_blocked,))

    @classmethod
    def set_group_negative(cls, user) -> None:
        if not user:
            raise
        if user.group == Groups.Negative.value:
            raise UserAlreadyNegativeError

        with db.atomic():
            user.group = Groups.Negative.value
            user.save(only=(User.group,))

    @classmethod
    def set_group_all(cls, user) -> None:
        if not user:
            raise
        if user.group == Groups.All.value:
            raise UserAlreadyAllError

        with db.atomic():
            user.group = Groups.All.value
            user.save(only=(User.group,))

    @classmethod
    def set_group_neutral(cls, user) -> None:
        if not user:
            raise
        if user.group == Groups.Neutral.value:
            raise UserAlreadyNeutralError

        with db.atomic():
            user.group = Groups.Neutral.value
            user.save(only=(User.group,))

    @classmethod
    def set_group_positive(cls, user) -> None:
        if not user:
            raise
        if user.group == Groups.Positive.value:
            raise UserAlreadyPositiveError

        with db.atomic():
            user.group = Groups.Positive.value
            user.save(only=(User.group,))

    @classmethod
    def set_group_vip(cls, user) -> None:
        if not user:
            raise
        if user.group == Groups.Vip.value:
            raise UserAlreadyVipError

        with db.atomic():
            user.group = Groups.Vip.value
            user.save(only=(User.group,))

    @classmethod
    def get_by_chat_id(cls, chat_id: str) -> User:
        return cls.get_query().where(User.chat_id == chat_id).first()

    @classmethod
    async def is_subscriber_public(cls, bot: Bot, chat_id: int) -> bool:
        try:
            member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=chat_id)
            return member.status in ('member', 'administrator', 'creator')
        except BadRequest:
            return False

    @classmethod
    async def is_subscriber_private(cls, bot: Bot, chat_id: int) -> bool:
        try:
            member = await bot.get_chat_member(chat_id=int(CHANNEL_ID), user_id=chat_id)
            return member.status in ('member', 'administrator', 'creator')
        except BadRequest:
            return False

    @classmethod
    async def is_subscriber(cls, bot: Bot, chat_id: int) -> bool:
        return await cls.is_subscriber_public(bot, chat_id) or await cls.is_subscriber_private(bot, chat_id)

    @classmethod
    def count(cls,
              is_active: bool = None,
              is_blocked: bool = None,
              group: str = None,
              is_manager: bool = None) -> int:
        query = User.select()

        if is_active is not None:
            query = query.where(User.is_active == is_active)
        if is_blocked is not None:
            query = query.where(User.is_blocked == is_blocked)
        if group is not None:
            query = query.where(User.group == group)
        if is_manager is not None:
            query = query.where(User.is_manager == is_manager)

        return query.count()

    @classmethod
    def get_top_referral_sources_list(cls, limit: int = 10) -> List[dict]:
        referral_counts = (
            User
            .select(User.referral_user_id, fn.COUNT(User.id).alias('referral_count'))
            .where(User.referral_user_id.is_null(False))
            .group_by(User.referral_user_id)
            .order_by(fn.COUNT(User.id).desc())
            .limit(limit)
        )

        # Fetch full user data based on referral_user_id
        top_referrers = []
        for entry in referral_counts:
            referrer = cls.get_by_id(entry.referral_user_id)
            if referrer:
                top_referrers.append({
                    'user_id': referrer.id,
                    'chat_id': referrer.chat_id,
                    'username': referrer.username,
                    'referral_count': entry.referral_count
                })

        return top_referrers
