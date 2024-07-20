from datetime import datetime

from pydantic import BaseModel
from pydantic import EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    created_at: datetime
