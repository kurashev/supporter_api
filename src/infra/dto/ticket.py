from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.infra.dto import UserDTO
    from .message import MessageDTO
    from src.common.misc.db_enums import TicketStatusEnum


@dataclass
class TicketDTO:
    id: int
    user_id: int
    user: "UserDTO"
    status: "TicketStatusEnum"
    created_at: datetime
    updated_at: datetime
    messages: list["MessageDTO"] = field(default_factory=list)
