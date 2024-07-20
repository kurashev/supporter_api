import functools
from datetime import datetime, timezone, timedelta
from typing import TYPE_CHECKING, List, Callable
from fastapi import Request, HTTPException, status, Depends

from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic.types import SecretStr

from src.common.config.auth import AuthConfig
from src.common.misc.stub import Stub
from src.common.misc.user_role import UserRoleEnum
from src.infra.database.dao.holder import HolderDAO
from src.infra.schemas.user import UserSchema

if TYPE_CHECKING:
    from src.infra.dto import UserDTO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: SecretStr | str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = AuthConfig.compose()
    encode_jwt = jwt.encode(to_encode, auth_data.secret_key, algorithm=auth_data.algorithm)
    return encode_jwt


def get_token(request: Request):
    token = request.cookies.get('user_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    return token


async def get_current_user(token: str = Depends(get_token), holder: HolderDAO = Depends(Stub(HolderDAO))):
    try:
        auth_data = AuthConfig.compose()
        payload = jwt.decode(token, auth_data.secret_key, algorithms=[auth_data.algorithm])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Can\'t found user ID')

    user = await holder.user.get_user_by_user_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return UserSchema.from_orm(user)


class RoleChecker:
    def __init__(self, required_roles: List[UserRoleEnum]):
        self.required_roles = required_roles

    async def __call__(self, current_user: UserSchema = Depends(get_current_user)):
        if current_user.user_role not in self.required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return current_user
