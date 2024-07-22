from fastapi import Depends, HTTPException, status

from src.common.misc.db_enums import UserRoleEnum
from src.infra.dto import UserDTO
from src.infra.schemas.user import UserSchema
from src.infra.services.authentication import get_current_user


def can_change_role(current_user: UserSchema = Depends(get_current_user)):
    def verify(target_user: UserDTO, target_role: UserRoleEnum):
        if current_user.user_role == UserRoleEnum.ADMIN:
            if (target_user.user_role not in [UserRoleEnum.USER, UserRoleEnum.SUPPORT] or target_role not in
                    [UserRoleEnum.USER, UserRoleEnum.SUPPORT]):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You have no access",
                )

        # Если роль текущего пользователя ниже, чем у целевого пользователя, или равна
        role_hierarchy = {
            UserRoleEnum.USER: 1,
            UserRoleEnum.SUPPORT: 2,
            UserRoleEnum.ADMIN: 3,
            UserRoleEnum.SUPER_ADMIN: 4
        }
        if role_hierarchy[current_user.user_role] <= role_hierarchy[target_user.user_role]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You have no access",
            )

    return verify
