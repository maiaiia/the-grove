from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from backend.src.repository.auth_repository import AuthRepository
from backend.src.model.auth import User
from backend.src.model.enum.user_role import UserRoleName
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for AuthService")
ALGORITHM = os.getenv("HASHING_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

class AuthService:
    def __init__(self, db: Session):
        self.repo = AuthRepository(db)
        self.db = db

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.repo.get_user_by_username(username)
        if not user:
            return None
        if not self.verify_password(password, user.password):
            return None
        return user

    def login(self, username: str, password: str) -> Optional[tuple[User, str]]:
        """Login user and return user object + JWT token"""
        user = self.authenticate_user(username, password)
        if not user:
            return None

        # Create token with user data
        token_data = {
            "sub": str(user.id),
            "username": user.username,
            "role": user.role.name.value if user.role else None
        }
        access_token = self.create_access_token(token_data)

        return user, access_token

    def get_current_user(self, token: str) -> Optional[User]:
        """Get current user from JWT token"""
        payload = self.decode_token(token)
        if not payload:
            return None

        user_id: str = payload.get("sub")
        if user_id is None:
            return None

        user = self.repo.get_user_by_id(int(user_id))
        return user

    def register_user(self, username: str, email: str, password: str,
                      role_name: UserRoleName = UserRoleName.USER) -> Optional[User]:
        if self.repo.get_user_by_username(username):
            return None
        if self.repo.get_user_by_email(email):
            return None

        role = self.repo.get_role_by_name(role_name)
        if not role:
            return None

        hashed_password = self.hash_password(password)
        user = self.repo.create_user(username, email, hashed_password, role.id)
        return user

    def check_permission(self, user: User, permission: str) -> bool:
        return self.repo.user_has_permission(user, permission)

    def get_user_permissions(self, user: User) -> list[str]:
        return self.repo.get_user_permissions(user)