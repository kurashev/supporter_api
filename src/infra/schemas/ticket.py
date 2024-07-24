from datetime import datetime
from typing import Any

from pydantic import Field

from src.common.misc.db_enums import TicketStatusEnum, UserRoleEnum
from src.infra.schemas.base import BaseSchemaModel


class UserTicketSchema(BaseSchemaModel):
    id: int
    username: str
    email: str
    user_role: UserRoleEnum


class UserMessageTicketSchema(BaseSchemaModel):
    id: int
    username: str


class TicketMessageSchema(BaseSchemaModel):
    id: int
    message: str
    created_at: datetime
    updated_at: datetime
    user: UserMessageTicketSchema | None


class TicketSchema(BaseSchemaModel):
    id: int
    user: UserTicketSchema
    status: TicketStatusEnum
    messages: list[TicketMessageSchema]
    created_at: datetime
    updated_at: datetime


class TicketsListSchema(BaseSchemaModel):
    tickets: list[TicketSchema]


class AddTicketMessageSchema(BaseSchemaModel):
    ticket_id: int
    message: str


class EditTicketMessage(BaseSchemaModel):
    message_id: int
    new_message: str


class EditTicketStatus(BaseSchemaModel):
    ticket_id: int
    status: TicketStatusEnum
