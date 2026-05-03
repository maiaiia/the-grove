from backend.src.model.auth import User, Role, Permission
from backend.src.model.enum.user_role import UserRoleName
from backend.src.model.enum.user_permission import PermissionName
from backend.src.model.database import SessionLocal
from backend.src.service import AuthService


def create_permissions_map(db: SessionLocal) -> dict:
    permissions_map = {}
    for p_name in PermissionName:
        perm = db.query(Permission).filter(Permission.name == p_name).first()
        if not perm:
            perm = Permission(name=p_name)
            db.add(perm)
        permissions_map[p_name] = perm
    db.commit()
    return permissions_map

def create_roles(db: SessionLocal, permissions_map: dict) -> tuple:
    # admin
    admin_role = db.query(Role).filter(Role.name == UserRoleName.ADMIN).first()
    if not admin_role:
        admin_role = Role(name=UserRoleName.ADMIN)
        admin_role.permissions = list(permissions_map.values())
        db.add(admin_role)

    # guest
    guest_role = db.query(Role).filter(Role.name == UserRoleName.GUEST).first()
    if not guest_role:
        guest_role = Role(name=UserRoleName.GUEST)
        guest_role.permissions = [permissions_map[PermissionName.READ_PLANT]]
        db.add(guest_role)
    db.commit()

    # regular user
    user_role = db.query(Role).filter(Role.name == UserRoleName.USER).first()
    if not user_role:
        user_role = Role(name=UserRoleName.USER)
        user_role.permissions = [permissions_map[PermissionName.READ_PLANT],
                                 permissions_map[PermissionName.WRITE_PLANT],
                                 permissions_map[PermissionName.DELETE_PLANT]]
        db.add(user_role)

    db.commit()
    return admin_role, guest_role, user_role

def create_users(db: SessionLocal, admin_role, guest_role, user_role):
    if not db.query(User).filter(User.username == "admin").first():
        admin_user = User(
            username="admin",
            email="admin@mail.com",
            password=AuthService.hash_password('adminpassword'),  # todo encrypt later on
            role=admin_role
        )
        db.add(admin_user)

    if not db.query(User).filter(User.username == "maia").first():
        regular_user = User(
            username="maia",
            email="maia@mail.com",
            password=AuthService.hash_password('userpassword'),  # todo encrypt later on
            role=user_role
        )
        db.add(regular_user)

    db.commit()

def seed_auth_data():
    db = SessionLocal()
    try:
        permissions_map = create_permissions_map(db)
        admin_role, guest_role, user_role = create_roles(db, permissions_map)
        create_users(db, admin_role, guest_role, user_role)

    finally:
        db.close()