from fastapi import APIRouter, HTTPException, status, Response
from fastapi.params import Depends
from sqlalchemy.exc import IntegrityError

from src.common.misc.stub import Stub
from src.infra.database.dao.holder import HolderDAO
from src.infra.schemas.auth import UserRegister, UserAuth
from src.infra.services.authentication import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post("/register/",
             status_code=200)
async def user_register(user_data: UserRegister, holder: HolderDAO = Depends(Stub(HolderDAO))):
    user_dict = user_data.dict()
    user_dict['password'] = get_password_hash(user_data.password.get_secret_value())
    try:
        user = await holder.user.add_user(**user_dict)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email is busy"
        )
    await holder.commit()
    return {"success": True, "id": user.id, "username": user.username, "email": user.email}


@router.post("/login/")
async def user_auth(response: Response, user_data: UserAuth, holder: HolderDAO = Depends(Stub(HolderDAO))):
    user = await holder.user.get_user(user_data.username)
    if not user or not verify_password(plain_password=user_data.password.get_secret_value(),
                                       hashed_password=user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong username or password"
        )
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(key="user_access_token", value=access_token, httponly=True)
    return {'access_token': access_token}


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="user_access_token")
    return {'success': True}
