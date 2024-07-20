import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from src.common.misc.user_role import UserRoleEnum
from src.infra import dto
from src.infra.database.models.base import BaseModel, TimestampMixin
from sqlalchemy.dialects.postgresql import ENUM


class User(BaseModel, TimestampMixin):
    id: Mapped[int] = mapped_column(sa.BIGINT, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(sa.VARCHAR(33), unique=True)
    email: Mapped[str] = mapped_column(sa.String, unique=True)
    password: Mapped[str] = mapped_column(sa.String)
    user_role: Mapped[UserRoleEnum] = mapped_column(ENUM(UserRoleEnum), server_default="USER")

    def to_dto(self) -> dto.UserDTO:
        return dto.UserDTO(
            id=self.id,
            username=self.username,
            email=self.email,
            password=self.password,
            user_role=self.user_role
        )
