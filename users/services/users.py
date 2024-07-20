import jwt
from core.config import settings
from crud.users import get_user_by_email
from db.db_helper import get_db_session
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from jwt import DecodeError
from jwt import ExpiredSignatureError
from schemas.users import UserSchema
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

ACCESS_TOKEN_TYPE = 'access'


def decode_access_jwt(
    token: str | bytes,
    public_key: str = settings.jwt_public_key.read_text(),
    algorithm: str = settings.jwt_algorithm,
) -> dict:
    try:
        decoded_token = jwt.decode(token, public_key, algorithms=[algorithm])
        if decoded_token.get('token_type') != ACCESS_TOKEN_TYPE:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token isn't access"
            )
        return decoded_token
    except ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is expired'
        ) from e
    except DecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid'
        ) from e


async def get_user_by_token(
    session: AsyncSession = Depends(get_db_session),
    authorization: str = Header(),
) -> UserSchema:
    decoded_token = decode_access_jwt(authorization)
    email = decoded_token.get('email')
    user = await get_user_by_email(session, email)
    return UserSchema(**user)
