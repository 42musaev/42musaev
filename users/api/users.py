from fastapi import APIRouter
from fastapi import Depends
from schemas.users import UserSchema
from services.users import get_user_by_token

router = APIRouter(prefix='/users')


@router.get('/me')
async def get_me(
    user: UserSchema = Depends(get_user_by_token),
):
    return user.model_dump()
