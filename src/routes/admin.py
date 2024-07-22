from typing import Callable

from fastapi import APIRouter, Depends, HTTPException, status

from src.common.misc.stub import Stub
from src.common.misc.db_enums import UserRoleEnum
from src.infra.database.dao.holder import HolderDAO
from src.infra.dto import UserDTO
from src.infra.schemas.admin import ChangeRoleRequest
from src.infra.services.admin import can_change_role

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.put("/change-role/", dependencies=[Depends(can_change_role)])
async def change_role(request: ChangeRoleRequest, verify: Callable[[UserDTO, UserRoleEnum], None] = Depends(can_change_role),
                      holder: HolderDAO = Depends(Stub(HolderDAO))):
    target_user = await holder.user.get_user(username=request.username)
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    verify(target_user, request.new_role)

    await holder.user.edit_user_role(request.username, request.new_role)
    await holder.commit()

    return {"message": "User role updated successfully"}
