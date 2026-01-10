from typing import List
from peewee import ModelSelect, Case
from common.constants import BonusRequestStatuses
from models import db
from models.bonus_request_model import BonusRequest


class BonusRequestLogics:
    @staticmethod
    def get_query() -> ModelSelect:
        query = BonusRequest.select()
        return query

    @classmethod
    def create(cls, user_id: str, bonus_id: str) -> BonusRequest:
        bonus = BonusRequest.create(
            user_id=user_id,
            bonus_id=bonus_id,
        )

        return bonus

    @classmethod
    def approve(cls, bonus_request: BonusRequest) -> None:
        with db.atomic():
            if bonus_request.status != BonusRequestStatuses.Approved.value:
                bonus_request.status = BonusRequestStatuses.Approved.value
                bonus_request.save(only=(BonusRequest.status,))

    @classmethod
    def cancel(cls, bonus_request: BonusRequest) -> None:
        with db.atomic():
            if bonus_request.status != BonusRequestStatuses.Canceled.value:
                bonus_request.status = BonusRequestStatuses.Canceled.value
                bonus_request.save(only=(BonusRequest.status,))

    @classmethod
    def activate(cls, bonus_request: BonusRequest) -> None:
        with db.atomic():
            if bonus_request.status != BonusRequestStatuses.Active.value:
                bonus_request.status = BonusRequestStatuses.Active.value
                bonus_request.save(only=(BonusRequest.status,))

    @classmethod
    def get_by_id(cls, pk: str) -> BonusRequest:
        return cls.get_query().where(BonusRequest.id == pk).first()

    @classmethod
    def get_list(
            cls,
            user_id: str = None,
            bonus_id: str = None,
            status: str = None,
            page: int = None) -> List[BonusRequest]:

        status_priority = Case(
            None,
            [
                (BonusRequest.status == BonusRequestStatuses.Active.value, 0),
                (BonusRequest.status == BonusRequestStatuses.Approved.value, 1),
                (BonusRequest.status == BonusRequestStatuses.Canceled.value, 2),
            ],
            3
        )

        wheres = []
        if user_id:
            wheres.append(BonusRequest.user_id == user_id)
        if bonus_id:
            wheres.append(BonusRequest.bonus_id == bonus_id)
        if status:
            wheres.append(BonusRequest.status == status)

        query = cls.get_query()

        if wheres:
            query = query.where(*wheres)

        query = query.order_by(status_priority, BonusRequest.created_at.desc())

        if page:
            query = query.paginate(page, 5)

        return list(query)
