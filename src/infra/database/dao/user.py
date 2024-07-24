from sqlalchemy import insert, select, or_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.common.misc.db_enums import UserRoleEnum
from src.infra import dto
from src.infra.database.dao.base import BaseDAO
from src.infra.database.models import User, Ticket, TicketMessage


class UserDAO(BaseDAO):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def add_user(self, username: str, email: str, password: str) -> dto.UserDTO:
        stmt = insert(User).values(username=username, email=email, password=password).returning(User)

        return (await self._session.scalars(stmt)).first().to_dto()

    async def get_user(self, username: str | None = None, email: str | None = None) -> dto.UserDTO | None:
        stmt = select(User).where(or_(User.username == username, User.email == email))

        result = await self._session.scalars(stmt)

        user: User | None = result.first()
        if not user:
            return None

        return user.to_dto()

    async def get_user_by_user_id(self, user_id: int) -> dto.UserDTO | None:
        stmt = select(User).where(User.id == user_id).options(
            joinedload(User.tickets).joinedload(Ticket.messages).joinedload(TicketMessage.user)
        )

        result = await self._session.scalars(stmt)

        user: User | None = result.unique().first()
        if not user:
            return None

        return user.to_dto_tickets_prefetched()

    async def edit_user_role(self, username: str, role: UserRoleEnum) -> None:
        stmt = update(User).where(User.username == username).values(user_role=role)

        await self._session.execute(stmt)


