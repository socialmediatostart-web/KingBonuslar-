class ServiceException(Exception):
    def __init__(self, message=None, *args, **kwargs):
        self.message = message
        super().__init__(args, kwargs)


class BonusAlreadyEnabledError(ServiceException):
    pass


class BonusAlreadyRemovedError(ServiceException):
    pass


class BonusAlreadyNotRequestError(ServiceException):
    pass


class BonusAlreadyRequestError(ServiceException):
    pass


class BonusAlreadyDisabledError(ServiceException):
    pass


class BonusAlreadyAllError(ServiceException):
    pass


class BonusAlreadyNegativeError(ServiceException):
    pass


class BonusAlreadyApprovedError(ServiceException):
    pass


class BonusAlreadyActivatedError(ServiceException):
    pass


class BonusAlreadyCanceledError(ServiceException):
    pass


class UserAlreadyVipError(ServiceException):
    pass


class UserAlreadyPositiveError(ServiceException):
    pass


class UserAlreadyNeutralError(ServiceException):
    pass


class UserAlreadyAllError(ServiceException):
    pass


class UserAlreadyNegativeError(ServiceException):
    pass


class UserAlreadyBlockedError(ServiceException):
    pass


class UserAlreadyUnblockedError(ServiceException):
    pass


class BonusAlreadyNeutralError(ServiceException):
    pass


class BonusAlreadyPositiveError(ServiceException):
    pass


class BonusAlreadyVipError(ServiceException):
    pass
