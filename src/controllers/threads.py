# controllers/threads.py
# controllers for Threads

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Path
from neomodel import db

from src.models import Thread, User
from src.schemas import (
    ReplySimpleRead,
    ThreadCreate,
    ThreadRead,
    ThreadSimpleRead,
    ThreadUpdate,
    UserRead,
)

router = APIRouter(tags=["thread"])


@router.post("/thread/", response_model=ThreadRead)
async def create_thread(user_id: str, thread: ThreadCreate):
    """
    create_thread

    Creates a new Thread

    """
    with db.transaction:
        user = User.nodes.get(uuid=user_id)

        new_thread = Thread(title=thread.title, body=thread.body).save()
        new_thread.author.connect(user)

    author_data = UserRead(
        uuid=user.uuid,
        name=user.name,
        created_at=user.created_at,
    )

    response = ThreadRead(
        uuid=new_thread.uuid,
        title=new_thread.title,
        body=new_thread.body,
        author=author_data,
        children=[],
        created_at=new_thread.created_at,
        updated_at=new_thread.updated_at,
        upvotes=0,
        downvotes=0,
    )

    return response


@router.get("/thread/", response_model=list[ThreadSimpleRead])
async def get_all_threads():
    """
    get_all_threads

    Returns all Threads

    """
    with db.transaction:
        all_threads = Thread.nodes.all()

    response = [
        ThreadSimpleRead(
            uuid=thread.uuid,
            title=thread.title,
            body=thread.body,
            created_at=thread.created_at,
            updated_at=thread.updated_at,
        )
        for thread in all_threads
    ]

    return response


@router.patch("/thread/{thread_id}", response_model=ThreadSimpleRead)
async def update_thread(
    thread_id: Annotated[str, Path(title="UUID of the Thread to be updated")],
    thread: ThreadUpdate,
):
    """
    update_thread

    Updates an existing Thread

    """
    with db.transaction:
        updated_thread = Thread.nodes.get(uuid=thread_id)
        updated_thread.title = thread.title
        updated_thread.body = thread.body
        updated_thread.save()

    response = ThreadSimpleRead(
        uuid=updated_thread.uuid,
        title=updated_thread.title,
        body=updated_thread.body,
        created_at=updated_thread.created_at,
        updated_at=datetime.now(),
    )

    return response


@router.get("/thread/{thread_id}", response_model=ThreadRead)
async def get_thread(
    thread_id: Annotated[str, Path(title="UUID of the Thread to be retrieved")]
):
    """
    get_thread

    Returns a thread by UUID

    """
    with db.transaction:
        thread = Thread.nodes.get(uuid=thread_id)
        author = thread.author.get()
        children = thread.children.all()

    author_data = UserRead(
        uuid=author.uuid,
        name=author.name,
        created_at=author.created_at,
    )

    children_data = [
        ReplySimpleRead(
            uuid=child.uuid,
            body=child.body,
            created_at=child.created_at,
            updated_at=child.updated_at,
        )
        for child in children
    ]

    response = ThreadRead(
        uuid=thread.uuid,
        title=thread.title,
        body=thread.body,
        author=author_data,
        children=children_data,
        created_at=thread.created_at,
        updated_at=thread.updated_at,
        upvotes=thread.n_upvotes(),
        downvotes=thread.n_downvotes(),
    )

    return response


@router.delete("/thread/{thread_id}", status_code=204)
async def delete_thread(
    thread_id: Annotated[str, Path(title="UUID of the Thread to be deleted")]
):
    """
    delete_thread

    Deletes a Thread

    """
    with db.transaction:
        thread = Thread.nodes.get(uuid=thread_id)
        thread.delete()
