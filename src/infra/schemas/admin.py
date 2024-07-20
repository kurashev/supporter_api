from src.common.misc.user_role import UserRoleEnum
from src.infra.schemas.base import BaseSchemaModel


class ChangeRoleRequest(BaseSchemaModel):
    username: str
    new_role: UserRoleEnum
