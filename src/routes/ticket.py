from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache

from src.common.misc.db_enums import UserRoleEnum, TicketStatusEnum
from src.common.misc.stub import Stub
from src.infra.database.dao.holder import HolderDAO
from src.infra.schemas.ticket import TicketsListSchema, AddTicketMessageSchema, EditTicketMessage, EditTicketStatus
from src.infra.schemas.user import UserSchema
from src.infra.services.authentication import RoleChecker, get_current_user

router = APIRouter(prefix="/ticket", tags=["Tickets"])


@router.get("/")
@cache(expire=10, namespace="tickets")
async def tickets_list(user_id: int | None = None, ticket_status: TicketStatusEnum | None = None,
                       _: UserSchema = Depends(RoleChecker(UserRoleEnum.SUPPORT)),
                       holder: HolderDAO = Depends(Stub(HolderDAO))):
    tickets = await holder.ticket.get_tickets_from_request(user_id, ticket_status)
    return TicketsListSchema(tickets=tickets)


@router.post("/")
async def create_ticket(message: str, user: UserSchema = Depends(get_current_user),
                        holder: "HolderDAO" = Depends(Stub(HolderDAO))):
    ticket = await holder.ticket.add_ticket(user.id)
    await holder.ticket.add_ticket_message(ticket.id, user.id, message)
    await holder.commit()

    return {"success": True, "message": message}


@router.put("/")
async def edit_ticket_status_request(ticket: EditTicketStatus,
                                     _: UserSchema = Depends(RoleChecker(UserRoleEnum.SUPPORT)),
                                     holder: HolderDAO = Depends(Stub(HolderDAO))):
    ticket_db = await holder.ticket.get_ticket_by_ticket_id(ticket.ticket_id)
    if not ticket_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket was not found"
        )

    await holder.ticket.edit_ticket_status(ticket.ticket_id, ticket.status)
    await holder.commit()
    return {"success": True, "id": ticket.ticket_id}


@router.post("/add-message/")
async def add_message(new_message: AddTicketMessageSchema, current_user: UserSchema = Depends(get_current_user),
                      holder: HolderDAO = Depends(Stub(HolderDAO))):
    ticket = await holder.ticket.get_ticket_by_ticket_id(new_message.ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket was not found"
        )
    if ticket.status == TicketStatusEnum.CLOSED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ticket is closed"
        )
    if current_user.user_role == UserRoleEnum.USER and current_user.id != ticket.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN
        )
    if ticket.status == TicketStatusEnum.WAIT_SUPPORT_ANSWER and ticket.user_id != current_user.id:
        await holder.ticket.edit_ticket_status(new_message.ticket_id, TicketStatusEnum.WAIT_USER_ANSWER)
    elif ticket.status == TicketStatusEnum.WAIT_USER_ANSWER and ticket.user_id == current_user.id:
        await holder.ticket.edit_ticket_status(new_message.ticket_id, TicketStatusEnum.WAIT_SUPPORT_ANSWER)
    message = await holder.ticket.add_ticket_message(new_message.ticket_id, current_user.id, new_message.message)
    await holder.commit()
    return {"success": True, "message_id": message.id}


@router.put("/edit-message/")
async def edit_message(message: EditTicketMessage, current_user: UserSchema = Depends(get_current_user),
                       holder: HolderDAO = Depends(Stub(HolderDAO))):
    message_db = await holder.ticket.get_message(message.message_id)

    if not message_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket was not found"
        )

    if message_db.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    await holder.ticket.edit_message(message.message_id, message.new_message)
    await holder.commit()

    return {"success": True, "id": message.message_id}
