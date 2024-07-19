from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database.dao.base import BaseDAO


class HolderDAO(BaseDAO):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
