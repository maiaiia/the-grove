from enum import Enum

class PermissionName(str, Enum):
    READ_PLANT = "read_plant"
    WRITE_PLANT = "write_plant"
    DELETE_PLANT = "delete_plant"
    MANAGE_USERS = "manage_users"