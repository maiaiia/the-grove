from sqlalchemy.orm import Session
from typing import Optional
from backend.src.model.auth import User, Role, Permission
from backend.src.model.enum.user_role import UserRoleName


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, username: str, email: str, hashed_password: str, role_id: int) -> User:
        user = User(
            username=username,
            email=email,
            password=hashed_password,
            role_id=role_id
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_role_by_name(self, role_name: UserRoleName) -> Optional[Role]:
        return self.db.query(Role).filter(Role.name == role_name).first()

    def get_user_permissions(self, user: User) -> list[str]:
        if not user.role:
            return []
        return [perm.name.value for perm in user.role.permissions]

    def user_has_permission(self, user: User, permission_name: str) -> bool:
        if not user.role:
            return False
        return any(perm.name.value == permission_name for perm in user.role.permissions)