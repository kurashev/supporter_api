from datetime import datetime

from pydantic import Field

from src.common.misc.db_enums import UserRoleEnum
from src.infra.schemas.base import BaseSchemaModel
from src.infra.schemas.ticket import TicketMessageSchema


class TicketSchema(BaseSchemaModel):
    id: int
    messages: list[TicketMessageSchema]
    created_at: datetime
    updated_at: datetime


class UserSchema(BaseSchemaModel):
    id: int
    username: str
    email: str
    user_role: UserRoleEnum
    tickets: list[TicketSchema] = Field(default_factory=list)
