from typing import TYPE_CHECKING

import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.misc.db_enums import TicketStatusEnum
from src.infra import dto
from src.infra.database.models.base import BaseModel, TimestampMixin
from sqlalchemy.dialects.postgresql import ENUM

if TYPE_CHECKING:
    from .user import User
    from .message import TicketMessage


class Ticket(BaseModel, TimestampMixin):
    id: Mapped[int] = mapped_column(sa.BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(sa.BIGINT, sa.ForeignKey("users.id"))
    status: Mapped[TicketStatusEnum] = mapped_column(ENUM(TicketStatusEnum), server_default="WAIT_SUPPORT_ANSWER")
    user: Mapped["User"] = relationship(back_populates="tickets", uselist=False)
    messages: Mapped[list["TicketMessage"]] = relationship(back_populates="ticket", uselist=True)

    def to_dto(self, user: dto.UserDTO | None = None, messages: list[dto.MessageDTO] | None = None) -> dto.TicketDTO:
        if messages is None:
            messages = []
        return dto.TicketDTO(
            id=self.id,
            user_id=self.user_id,
            status=self.status,
            user=user,
            messages=messages,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    def to_dto_user_prefetched(self):
        return self.to_dto(user=self.user.to_dto())

    def to_dto_messages_prefetched(self):
        return self.to_dto(messages=[message.to_dto_user_prefetched() for message in self.messages])

    def to_dto_all_prefetched(self):
        return self.to_dto(user=self.user.to_dto(), messages=[message.to_dto_user_prefetched() for message in self.messages])
