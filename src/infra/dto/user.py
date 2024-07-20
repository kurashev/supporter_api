from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.common.misc.user_role import UserRoleEnum


@dataclass
class UserDTO:
    id: int
    username: str
    email: str
    password: str
    user_role: "UserRoleEnum"
