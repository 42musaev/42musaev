import hashlib
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Dict

import jwt
from core.config import settings
from crud.refresh_session_crud import create_or_update_refresh_session
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
        'email': 'user@example.com',
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
    payload: Dict,
) -> str:
    return encode_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        payload=payload,
        expire_minutes=settings.jwt_settings.access_token_expire_minutes,
    )


def create_refresh_token(
    payload: Dict,
) -> str:
    return encode_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        payload=payload,
        expire_timedelta=timedelta(settings.jwt_settings.refresh_token_expire_days),
    )


def generate_fingerprint(unique_string: str) -> str:
    return hashlib.sha256(unique_string.encode()).hexdigest()


def check_password(user: UserSchema):
    user_db = FAKE_DB[0]
    if user.model_dump() != user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Email or password incorrect',
        )


def get_fingerprint(unique_string: str) -> str:
    return hashlib.sha256(unique_string.encode()).hexdigest()


async def create_pair_tokens(
    request: Request,
    response: Response,
    user: UserSchema,
    session: AsyncSession,
) -> Dict[str, str]:
    check_password(user)
    payload = user.model_dump(exclude={'password'})

    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)
    decoded_refresh_token = decode_jwt(refresh_token)

    ip = request.client.host
    user_agent = request.headers.get('user-agent', 'unknown')
    fingerprint = generate_fingerprint(f'{ip}-{user_agent}')
    data_refresh_session_create = {
        'user_email': decoded_refresh_token.get('email'),
        'refresh_token': refresh_token,
        'user_agent': user_agent,
        'ip': ip,
        'fingerprint': fingerprint,
        'expires': decoded_refresh_token.get('exp'),
    }
    await create_or_update_refresh_session(session, data_refresh_session_create)
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        domain=settings.domain,
        path='/api/v1/auth',
        max_age=decoded_refresh_token.get('exp'),
        httponly=True,
    )
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
    }
