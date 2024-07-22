from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra import dto
from src.infra.database.models.base import BaseModel, TimestampMixin

if TYPE_CHECKING:
    from .ticket import Ticket
    from .user import User


class TicketMessage(BaseModel, TimestampMixin):
    id: Mapped[int] = mapped_column(sa.BIGINT, primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column(sa.String)
    user_id: Mapped[int] = mapped_column(sa.BIGINT, sa.ForeignKey("users.id"))
    ticket_id: Mapped[int] = mapped_column(sa.BIGINT, sa.ForeignKey("tickets.id"))
    user: Mapped["User"] = relationship(uselist=False)
    ticket: Mapped["Ticket"] = relationship(back_populates="messages", uselist=False)

    def to_dto(self, user: dto.UserDTO | None = None, ticket: dto.TicketDTO | None = None) -> dto.MessageDTO:
        return dto.MessageDTO(
            id=self.id,
            message=self.message,
            user_id=self.user_id,
            ticket_id=self.ticket_id,
            user=user,
            ticket=ticket,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    def to_dto_user_prefetched(self):
        return self.to_dto(user=self.user.to_dto())

    def to_dto_all_prefetched(self):
        return self.to_dto(user=self.user.to_dto(), ticket=self.ticket.to_dto())
