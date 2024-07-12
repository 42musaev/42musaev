import uuid
from datetime import datetime
from datetime import timedelta
from datetime import timezone

import jwt
from core.config import settings
from schemas.user import UserSchema

ACCESS_TOKEN_TYPE: str = 'access'


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
