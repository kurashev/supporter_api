from src.common.misc.db_enums import UserRoleEnum
from src.infra.schemas.base import BaseSchemaModel


class ChangeRoleRequest(BaseSchemaModel):
    username: str
    new_role: UserRoleEnum
