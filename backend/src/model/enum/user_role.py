from enum import Enum

class UserRoleName(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    GUEST = "GUEST"