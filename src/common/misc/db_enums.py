from enum import Enum


class UserRoleEnum(Enum):
    SUPER_ADMIN = 'SUPERADMIN'
    ADMIN = 'ADMIN'
    SUPPORT = 'SUPPORT'
    USER = 'USER'


class TicketStatusEnum(Enum):
    WAIT_SUPPORT_ANSWER = "WAIT_SUPPORT_ANSWER"
    WAIT_USER_ANSWER = "WAIT_USER_ANSWER"
    CLOSED = "CLOSED"
