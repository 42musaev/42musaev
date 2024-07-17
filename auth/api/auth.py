from db.db_helper import get_db_session
from fastapi import APIRouter
from fastapi import Depends
from schemas.jwt_token import TokenSchema
from schemas.user import UserSchema
from services.token import create_pair_tokens
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response

router = APIRouter(prefix='/auth')


@router.post('/login', response_model=TokenSchema)
async def login(
    request: Request,
    response: Response,
    user: UserSchema,
    session: AsyncSession = Depends(get_db_session),
):
    return await create_pair_tokens(request, response, user, session)
