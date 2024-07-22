from fastapi import APIRouter, Depends

from src.common.misc.db_enums import UserRoleEnum
from src.infra.schemas.user import UserSchema
from src.infra.services.authentication import RoleChecker, get_current_user

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/me/")
async def get_me(user_data: UserSchema = Depends(get_current_user)):
    return user_data
