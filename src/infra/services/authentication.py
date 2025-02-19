from datetime import datetime, timezone, timedelta
from typing import Union, Any

from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic.types import SecretStr

from src.common.config.auth import AuthConfig
from src.common.misc.db_enums import UserRoleEnum
from src.common.misc.stub import Stub
from src.infra.database.dao.holder import HolderDAO
from src.infra.schemas.user import UserSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: SecretStr | str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=21)
    to_encode.update({"exp": expire})
    auth_data = AuthConfig.compose()
    encode_jwt = jwt.encode(to_encode, auth_data.jwt_secret_key, algorithm=auth_data.algorithm)
    return encode_jwt


def create_refresh_token(subject: Union[str, Any]) -> str:
    expires_delta = datetime.utcnow() + timedelta(days=7)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    auth_data = AuthConfig.compose()
    encoded_jwt = jwt.encode(to_encode, auth_data.jwt_refresh_secret_key, auth_data.algorithm)
    return encoded_jwt


def get_token(request: Request):
    token = request.cookies.get('user_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    return token


async def get_current_user(token: str = Depends(get_token), holder: HolderDAO = Depends(Stub(HolderDAO))):
    try:
        auth_data = AuthConfig.compose()
        payload = jwt.decode(token, auth_data.jwt_secret_key, algorithms=[auth_data.algorithm])
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
    def __init__(self, required_role: UserRoleEnum):
        self.required_role = required_role

    async def __call__(self, current_user: UserSchema = Depends(get_current_user)):
        role_hierarchy = {
            UserRoleEnum.USER: 1,
            UserRoleEnum.SUPPORT: 2,
            UserRoleEnum.ADMIN: 3,
            UserRoleEnum.SUPER_ADMIN: 4
        }
        if role_hierarchy[self.required_role] > role_hierarchy[current_user.user_role]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return current_user
