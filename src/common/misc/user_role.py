from enum import Enum


class UserRoleEnum(Enum):
    SUPER_ADMIN = 'SUPERADMIN'
    ADMIN = 'ADMIN'
    SUPPORT = 'SUPPORT'
    USER = 'USER'
