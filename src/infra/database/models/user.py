import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from src.infra import dto
from src.infra.database.models.base import BaseModel, TimestampMixin


class User(BaseModel, TimestampMixin):
    id: Mapped[int] = mapped_column(sa.BIGINT, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(sa.VARCHAR(33))
    email: Mapped[str] = mapped_column(sa.String)
    password: Mapped[str] = mapped_column(sa.String)
    is_support: Mapped[bool] = mapped_column(sa.BOOLEAN, server_default="f")

    def to_dto(self) -> dto.UserDTO:
        return dto.UserDTO(
            id=self.id,
            username=self.username,
            email=self.email,
            password=self.password,
            is_support=self.is_support
        )
