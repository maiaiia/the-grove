from sqlalchemy import Column, Integer, String, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from .base import Base
from .enum.user_permission import PermissionName
from .enum.user_role import UserRoleName

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id")),
    Column("permission_id", Integer, ForeignKey("permissions.id"))
)


class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    name = Column(Enum(PermissionName), unique=True, nullable=False)


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(Enum(UserRoleName), unique=True, nullable=False)

    permissions = relationship("Permission", secondary=role_permissions)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)

    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role")