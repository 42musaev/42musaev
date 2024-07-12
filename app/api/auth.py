from fastapi import APIRouter
from fastapi import HTTPException
from jwt import ExpiredSignatureError
from schemas.jwt_token import TokenSchema
from schemas.user import UserSchema
from services.token import create_access_token
from services.token import decode_jwt
from starlette import status

router = APIRouter(prefix='/auth')

FAKE_DB = [
    {
        'email': '42musaev@gmail.com',
        'password': 'string',
    },
]


@router.post('/login', response_model=TokenSchema)
async def login(user: UserSchema):
    if user.password == FAKE_DB[0].get('password'):
        return TokenSchema(access_token=create_access_token(user))
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


@router.post('/token-check')
async def token_check(token: str):
    try:
        token = decode_jwt(token=token)
        return token
    except ExpiredSignatureError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is expired'
        ) from err
