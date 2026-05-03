import strawberry
from typing import Optional


@strawberry.type
class PermissionType:
    id: int
    name: str


@strawberry.type
class RoleType:
    id: int
    name: str
    permissions: list[PermissionType]


@strawberry.type
class UserType:
    id: int
    username: str
    email: str
    role: Optional[RoleType]


@strawberry.type
class AuthPayloadType:
    """Response type for login mutation"""
    user: UserType
    message: str


@strawberry.type
class AuthCheckType:
    """Response type for checking auth status"""
    authenticated: bool
    user: Optional[UserType]