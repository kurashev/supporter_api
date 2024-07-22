from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import UserDTO
    from .ticket import TicketDTO


@dataclass
class MessageDTO:
    id: int
    message: str
    user_id: int
    ticket_id: int
    user: "UserDTO"
    ticket: "TicketDTO"
    created_at: datetime
    updated_at: datetime
