from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List

from pydantic.alias_generators import to_camel


class BaseModelWithCaseConversion(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )


class LoginRequest(BaseModelWithCaseConversion):
    username: str
    password: str


class RegisterRequest(BaseModelWithCaseConversion):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModelWithCaseConversion):
    id: int
    username: str
    email: str
    role: Optional[str] = None
    permissions: List[str] = []

    class Config:
        from_attributes = True


class LoginResponse(BaseModelWithCaseConversion):
    user: UserResponse
    message: str = "Login successful"


class MessageResponse(BaseModelWithCaseConversion):
    message: str