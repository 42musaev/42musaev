import hashlib
import time
import uuid
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Dict

import jwt
from core.config import settings
from crud.refresh_session_crud import refresh_session_create
from schemas.user import UserSchema
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response

ACCESS_TOKEN_TYPE: str = 'access'
REFRESH_TOKEN_TYPE: str = 'refresh'

FAKE_DB = [
    {
        'email': '42musaev@gmail.com',
        'password': 'string',
    },
]


def encode_jwt(
    token_type: str,
    payload: dict,
    private_key: str = settings.jwt_settings.private_key.read_text(),
    algorithm: str = settings.jwt_settings.algorithm,
    expire_minutes: int = settings.jwt_settings.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(tz=timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        token_type=token_type,
        exp=expire,
        iat=now,
        jti=str(uuid.uuid4()),
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.jwt_settings.public_key.read_text(),
    algorithm: str = settings.jwt_settings.algorithm,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def create_access_token(
    user: UserSchema,
) -> str:
    jwt_payload = {
        'email': user.email,
    }
    return encode_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        payload=jwt_payload,
        expire_minutes=settings.jwt_settings.access_token_expire_minutes,
    )


def create_refresh_token(
    user: UserSchema,
) -> str:
    jwt_payload = {
        'email': user.email,
    }
    return encode_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        payload=jwt_payload,
        expire_timedelta=timedelta(
            days=settings.jwt_settings.refresh_token_expire_days
        ),
    )


def generate_fingerprint(unique_string: str) -> str:
    return hashlib.sha256(unique_string.encode()).hexdigest()


def check_password(user: UserSchema):
    if user.password == FAKE_DB[0].get('password'):
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


async def create_pair_tokens(
    request: Request,
    response: Response,
    user: UserSchema,
    session: AsyncSession,
) -> Dict[str, str]:
    check_password(user)

    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    decode_refresh_token = decode_jwt(refresh_token)

    client_ip = request.client.host
    user_agent = request.headers.get('user-agent', 'unknown')
    unique_string = f'{client_ip}-{user_agent}'

    fingerprint = generate_fingerprint(unique_string)

    data_refresh_session_create = {
        'user_email': decode_refresh_token.get('email'),
        'refresh_token': refresh_token,
        'user_agent': user_agent,
        'ip': client_ip,
        'fingerprint': fingerprint,
        'expires': decode_refresh_token.get('exp'),
    }
    await refresh_session_create(
        session,
        data_refresh_session_create,
    )

    response.set_cookie(
        key='refreshToken',
        value=refresh_token,
        httponly=True,
        max_age=decode_refresh_token.get('exp') - int(time.time()),
        path='/api/auth',
        secure=True,
    )
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
    }
