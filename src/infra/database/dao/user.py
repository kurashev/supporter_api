from sqlalchemy import insert, select, or_, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.misc.user_role import UserRoleEnum
from src.infra import dto
from src.infra.database.dao.base import BaseDAO
from src.infra.database.models import User


class UserDAO(BaseDAO):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def add_user(self, username: str, email: str, password: str):
        stmt = insert(User).values(username=username, email=email, password=password)

        await self._session.execute(stmt)

    async def get_user(self, username: str | None = None, email: str | None = None) -> dto.UserDTO | None:
        stmt = select(User).where(or_(User.username == username, User.email == email))

        result = await self._session.scalars(stmt)

        user: User | None = result.first()
        if not user:
            return None

        return user.to_dto()

    async def get_user_by_user_id(self, user_id: int) -> dto.UserDTO | None:
        stmt = select(User).where(User.id == user_id)

        result = await self._session.scalars(stmt)

        user: User | None = result.first()
        if not user:
            return None

        return user.to_dto()

    async def edit_user_role(self, username: str, role: UserRoleEnum) -> None:
        stmt = update(User).where(User.username == username).values(user_role=role)

        await self._session.execute(stmt)


