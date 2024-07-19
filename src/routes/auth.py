from fastapi import APIRouter, HTTPException, status, Response, Request
from fastapi.params import Depends

from src.common.misc.stub import Stub
from src.infra.database.dao.holder import HolderDAO
from src.infra.dto import UserDTO
from src.infra.schemas.user import UserRegister, UserAuth
from src.infra.services.authentication import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post("/register/",
             status_code=200)
async def user_register(user_data: UserRegister, holder: HolderDAO = Depends(Stub(HolderDAO))):
    user = await holder.user.get_user(user_data.username, user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )

    user_dict = user_data.dict()
    user_dict['password'] = get_password_hash(user_data.password.get_secret_value())
    await holder.user.add_user(**user_dict)
    await holder.commit()
    return {"success": True}


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
    return {'access_token': access_token, 'refresh_token': None}


@router.get("/me/")
async def get_me(user_data: UserDTO = Depends(get_current_user)):
    return user_data


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="user_access_token")
    return {'success': True}
