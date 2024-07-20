from fastapi import APIRouter, Depends

from src.common.misc.user_role import UserRoleEnum
from src.infra.schemas.user import UserSchema
from src.infra.services.authentication import RoleChecker

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/me/")
async def get_me(user_data: UserSchema = Depends(RoleChecker([UserRoleEnum.USER, UserRoleEnum.ADMIN]))):
    return user_data
