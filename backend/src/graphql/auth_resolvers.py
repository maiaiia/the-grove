import strawberry
from fastapi import Response
from typing import Optional
from sqlalchemy.orm import Session

from backend.src.graphql.auth_types import (
    UserType, RoleType, PermissionType,
    AuthPayloadType, AuthCheckType
)
from backend.src.service.auth_service import AuthService
from backend.src.model.auth import User


# region helpers

def _permission(p) -> PermissionType:
    """Convert Permission model to GraphQL type"""
    return PermissionType(
        id=p.id,
        name=p.name.value
    )


def _role(r) -> RoleType:
    """Convert Role model to GraphQL type"""
    return RoleType(
        id=r.id,
        name=r.name.value,
        permissions=[_permission(p) for p in r.permissions]
    )


def _user(u: User) -> UserType:
    """Convert User model to GraphQL type"""
    return UserType(
        id=u.id,
        username=u.username,
        email=u.email,
        role=_role(u.role) if u.role else None
    )


def get_current_user_from_context(info: strawberry.Info) -> Optional[User]:
    """Extract current user from GraphQL context (set by get_context in main.py)"""
    return info.context.get("current_user")


def require_auth(info: strawberry.Info) -> User:
    """Require authentication - raises error if not authenticated"""
    current_user = get_current_user_from_context(info)
    if not current_user:
        raise Exception("Authentication required")
    return current_user


def require_permission(info: strawberry.Info, permission: str) -> User:
    """Require specific permission - raises error if not authorized"""
    current_user = require_auth(info)
    db: Session = info.context["db"]
    auth_service = AuthService(db)

    if not auth_service.check_permission(current_user, permission):
        raise Exception(f"Permission denied: {permission} required")

    return current_user


def require_admin(info: strawberry.Info) -> User:
    """Require admin role - raises error if not admin"""
    current_user = require_auth(info)
    if not current_user.role or current_user.role.name.value != "ADMIN":
        raise Exception("Admin access required")
    return current_user


# endregion


# region input types

@strawberry.input
class LoginInput:
    username: str
    password: str


@strawberry.input
class RegisterInput:
    username: str
    email: str
    password: str


# endregion


# region queries

@strawberry.type
class AuthQuery:
    @strawberry.field
    def me(self, info: strawberry.Info) -> Optional[UserType]:
        """Get current logged-in user"""
        current_user = require_auth(info)
        return _user(current_user)

    @strawberry.field
    def check_auth(self, info: strawberry.Info) -> AuthCheckType:
        """Check if user is authenticated (doesn't require auth)"""
        current_user = get_current_user_from_context(info)
        if current_user:
            return AuthCheckType(
                authenticated=True,
                user=_user(current_user)
            )
        return AuthCheckType(
            authenticated=False,
            user=None
        )


# endregion


# region mutations

@strawberry.type
class AuthMutation:
    @strawberry.mutation
    def login(self, input: LoginInput, info: strawberry.Info) -> AuthPayloadType:
        """Login user - sets cookie via context"""
        db: Session = info.context["db"]
        auth_service = AuthService(db)

        result = auth_service.login(input.username, input.password)
        if not result:
            raise Exception("Incorrect username or password")

        user, access_token = result

        response: Response = info.context["response"]
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=60 * 60 * 24,
            samesite="lax",
            secure=False
        )

        return AuthPayloadType(
            user=_user(user),
            message="Login successful",
            token=access_token,
        )

    @strawberry.mutation
    def register(self, input: RegisterInput, info: strawberry.Info) -> UserType:
        """Register a new user"""
        db: Session = info.context["db"]
        auth_service = AuthService(db)

        user = auth_service.register_user(
            username=input.username,
            email=input.email,
            password=input.password
        )

        if not user:
            raise Exception("Username or email already exists")

        return _user(user)

    @strawberry.mutation
    def logout(self, info: strawberry.Info) -> str:
        response: Response = info.context["response"]
        response.delete_cookie(key="access_token")
        return "Logged out successfully"

# endregion