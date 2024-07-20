from src.common.misc.user_role import UserRoleEnum
from src.infra.schemas.base import BaseSchemaModel


class UserSchema(BaseSchemaModel):
    id: int
    username: str
    email: str
    user_role: UserRoleEnum
