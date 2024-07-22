from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.common.misc.db_enums import UserRoleEnum
    from .ticket import TicketDTO


@dataclass
class UserDTO:
    id: int
    username: str
    email: str
    password: str
    user_role: "UserRoleEnum"
    tickets: list["TicketDTO"] = field(default_factory=list)
