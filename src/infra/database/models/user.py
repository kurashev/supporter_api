from typing import TYPE_CHECKING

import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.misc.db_enums import UserRoleEnum
from src.infra import dto
from src.infra.database.models.base import BaseModel, TimestampMixin
from sqlalchemy.dialects.postgresql import ENUM

if TYPE_CHECKING:
    from .ticket import Ticket


class User(BaseModel, TimestampMixin):
    id: Mapped[int] = mapped_column(sa.BIGINT, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(sa.VARCHAR(33), unique=True)
    email: Mapped[str] = mapped_column(sa.String, unique=True)
    password: Mapped[str] = mapped_column(sa.String)
    user_role: Mapped[UserRoleEnum] = mapped_column(ENUM(UserRoleEnum), server_default="USER")
    tickets: Mapped[list["Ticket"]] = relationship(back_populates="user", uselist=True)

    def to_dto(self, tickets: list[dto.TicketDTO] | None = None) -> dto.UserDTO:
        if tickets is None:
            tickets = []
        return dto.UserDTO(
            id=self.id,
            username=self.username,
            email=self.email,
            password=self.password,
            user_role=self.user_role,
            tickets=tickets
        )

    def to_dto_tickets_prefetched(self):
        return self.to_dto(tickets=[ticket.to_dto_messages_prefetched() for ticket in self.tickets])
