from _operator import or_
from typing import Sequence, TYPE_CHECKING

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.common.misc.db_enums import TicketStatusEnum
from src.infra import dto
from src.infra.database.dao.base import BaseDAO
from src.infra.database.models import Ticket, TicketMessage


class TicketDAO(BaseDAO):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def add_ticket(self, user_id: int,
                         status: TicketStatusEnum = TicketStatusEnum.WAIT_SUPPORT_ANSWER) -> dto.TicketDTO:
        stmt = insert(Ticket).values(user_id=user_id, status=status).returning(Ticket)

        return (await self._session.scalars(stmt)).first().to_dto()

    async def get_ticket_by_ticket_id(self, ticket_id: int) -> dto.TicketDTO | None:
        stmt = select(Ticket).where(Ticket.id == ticket_id)

        result = await self._session.scalars(stmt)

        ticket: Ticket = result.first()
        if not ticket:
            return None

        return ticket.to_dto()

    async def get_user_tickets(self, user_id: int) -> list[dto.TicketDTO]:
        stmt = select(Ticket).where(Ticket.user_id == user_id)

        result = await self._session.scalars(stmt)

        tickets: Sequence[Ticket] = result.all()

        return [ticket.to_dto() for ticket in tickets]

    async def get_tickets_by_status(self, status: TicketStatusEnum) -> list[dto.TicketDTO]:
        stmt = select(Ticket).where(Ticket.status == status).options(joinedload(Ticket.user),
                                                                     joinedload(Ticket.messages).joinedload(
                                                                         TicketMessage.user))

        result = await self._session.scalars(stmt)

        tickets: Sequence[Ticket] = result.unique().all()

        return [ticket.to_dto_all_prefetched() for ticket in tickets]

    async def get_tickets_from_request(self, user_id: int | None = None, status: TicketStatusEnum | None = None) -> \
            list[dto.TicketDTO]:
        stmt = select(Ticket).options(
            joinedload(Ticket.user),
            joinedload(Ticket.messages).joinedload(TicketMessage.user)
        )

        if user_id is not None:
            stmt = stmt.where(Ticket.user_id == user_id)

        if status is not None:
            stmt = stmt.where(Ticket.status == status)

        result = await self._session.scalars(stmt)

        tickets: Sequence[Ticket] = result.unique().all()

        return [ticket.to_dto_all_prefetched() for ticket in tickets]

    async def edit_ticket_status(self, ticket_id: int, status: TicketStatusEnum) -> None:
        stmt = update(Ticket).where(Ticket.id == ticket_id).values(status=status)

        await self._session.execute(stmt)

    async def add_ticket_message(self, ticket_id: int, user_id: int, message: str) -> dto.MessageDTO:
        stmt = insert(TicketMessage).values(ticket_id=ticket_id, user_id=user_id, message=message).returning(
            TicketMessage)

        return (await self._session.scalars(stmt)).first().to_dto()

    async def edit_message(self, message_id: int, message: str):
        stmt = update(TicketMessage).where(TicketMessage.id == message_id).values(message=message)

        await self._session.execute(stmt)

    async def delete_message(self, message_id: int) -> None:
        stmt = delete(TicketMessage).where(TicketMessage.id == message_id)

        await self._session.execute(stmt)

    async def get_message(self, message_id: int) -> dto.MessageDTO | None:
        stmt = select(TicketMessage).where(TicketMessage.id == message_id).options(
            joinedload(TicketMessage.user), joinedload(TicketMessage.ticket)
        )

        result = await self._session.scalars(stmt)

        message: TicketMessage | None = result.first()

        if not message:
            return None
        return message.to_dto_all_prefetched()
