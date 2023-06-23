# controllers/users.py
# controllers for Users

from typing import Annotated

from fastapi import APIRouter, Path
from neomodel import db

from src.models import User
from src.schemas import UserCreate, UserRead

router = APIRouter(tags=["user"])


@router.post("/user/", response_model=UserRead)
async def create_user(user: UserCreate):
    """
    create_user

    Creates a new User

    """
    with db.transaction:
        new_user = User(name=user.name).save()

    response = UserRead(
        uuid=new_user.uuid,
        name=new_user.name,
        created_at=new_user.created_at,
    )

    return response


@router.get("/user/", response_model=list[UserRead])
async def get_all_users():
    """
    get_all_users

    Returns all Users

    """
    with db.transaction:
        all_users = User.nodes.all()

    response = [
        UserRead(
            uuid=user.uuid,
            name=user.name,
            created_at=user.created_at,
        )
        for user in all_users
    ]

    return response


@router.get("/user/{uuid}", response_model=UserRead)
async def get_user(
    uuid: Annotated[str, Path(title="UUID of the User to be retrieved")]
):
    """
    get_user

    Returns a User by UUID

    """
    with db.transaction:
        user = User.nodes.get(uuid=uuid)

    response = UserRead(
        uuid=user.uuid,
        name=user.name,
        created_at=user.created_at,
    )

    return response


@router.delete("/user/{uuid}", status_code=204)
async def delete_user(
    uuid: Annotated[str, Path(title="UUID of the User to be deleted")]
):
    """
    delete_user

    Deletes a User

    """
    with db.transaction:
        user = User.nodes.get(uuid=uuid)
        user.delete()
