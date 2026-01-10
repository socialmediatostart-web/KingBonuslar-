from typing import List
from peewee import ModelSelect

from common.constants import Groups
from models import Bonus, db
from common.exceptions import BonusAlreadyEnabledError, BonusAlreadyDisabledError, BonusAlreadyAllError, \
    BonusAlreadyNegativeError, BonusAlreadyNeutralError, BonusAlreadyPositiveError, BonusAlreadyVipError, \
    BonusAlreadyRemovedError, BonusAlreadyNotRequestError, BonusAlreadyRequestError


class BonusLogics:
    @staticmethod
    def get_query() -> ModelSelect:
        query = Bonus.select()
        return query

    @classmethod
    def create(cls, description: str, group: str) -> Bonus:
        bonus = Bonus.create(
            description=description,
            group=group,
        )
        return bonus

    @classmethod
    def set_as_request(cls, bonus: Bonus):
        if not bonus:
            raise
        if bonus.is_request:
            raise BonusAlreadyRequestError

        with db.atomic():
            bonus.is_request = True
            bonus.save(only=(Bonus.is_request,))

    @classmethod
    def set_not_request(cls, bonus: Bonus):
        if not bonus:
            raise
        if not bonus.is_request:
            raise BonusAlreadyNotRequestError

        with db.atomic():
            bonus.is_request = False
            bonus.save(only=(Bonus.is_request,))

    @classmethod
    def set_bonus_removed(cls, bonus: Bonus) -> None:
        if not bonus:
            raise
        if bonus.is_removed:
            raise BonusAlreadyRemovedError

        with db.atomic():
            bonus.is_removed = True
            bonus.save(only=(Bonus.is_removed,))


    @classmethod
    def get_by_id(cls, pk: str) -> Bonus:
        return cls.get_query().where(Bonus.id == pk).first()

    @classmethod
    def get_list(cls, is_active: bool = None, group: str = None, is_removed: bool = None) -> List[Bonus]:
        wheres = []
        if is_removed is not None:
            wheres.append(Bonus.is_removed == is_removed)
        if is_active is not None:
            wheres.append(Bonus.is_active == is_active)

        if group is not None:
            wheres.append(Bonus.group == group)

        query = cls.get_query()
        if wheres:
            query = query.where(*wheres)

        return list(query)

    @classmethod
    def enable(cls, bonus: Bonus):
        if not bonus:
            raise
        if bonus.is_active:
            raise BonusAlreadyEnabledError

        with db.atomic():
            bonus.is_active = True
            bonus.save(only=(Bonus.is_active,))

    @classmethod
    def disable(cls, bonus: Bonus):
        if not bonus:
            raise
        if not bonus.is_active:
            raise BonusAlreadyDisabledError

        with db.atomic():
            bonus.is_active = False
            bonus.save(only=(Bonus.is_active,))

    @classmethod
    def set_group_all(cls, bonus: Bonus):
        if not bonus:
            raise
        if bonus.group == Groups.All.value:
            raise BonusAlreadyAllError

        with db.atomic():
            bonus.group = Groups.All.value
            bonus.save(only=(Bonus.group,))

    @classmethod
    def set_group_negative(cls, bonus: Bonus):
        if not bonus:
            raise
        if bonus.group == Groups.Negative.value:
            raise BonusAlreadyNegativeError

        with db.atomic():
            bonus.group = Groups.Negative.value
            bonus.save(only=(Bonus.group,))

    @classmethod
    def set_group_neutral(cls, bonus: Bonus):
        if not bonus:
            raise
        if bonus.group == Groups.Neutral.value:
            raise BonusAlreadyNeutralError

        with db.atomic():
            bonus.group = Groups.Neutral.value
            bonus.save(only=(Bonus.group,))

    @classmethod
    def set_group_positive(cls, bonus: Bonus):
        if not bonus:
            raise
        if bonus.group == Groups.Positive.value:
            raise BonusAlreadyPositiveError

        with db.atomic():
            bonus.group = Groups.Positive.value
            bonus.save(only=(Bonus.group,))

    @classmethod
    def set_group_vip(cls, bonus: Bonus):
        if not bonus:
            raise
        if bonus.group == Groups.Vip.value:
            raise BonusAlreadyVipError

        with db.atomic():
            bonus.group = Groups.Vip.value
            bonus.save(only=(Bonus.group,))
