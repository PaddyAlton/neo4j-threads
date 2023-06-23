# controllers/replies.py
# controllers for Replies

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Path
from neomodel import db

from src.models import Reply, ReplyLowerLevel, ReplyTopLevel, Thread, User
from src.schemas import (
    ReplyCreate,
    ReplyRead,
    ReplySimpleRead,
    ReplyUpdate,
    UserRead,
)

router = APIRouter(tags=["reply"])


### POST requests
@router.post("/thread/{thread_id}/reply", response_model=ReplyRead)
async def create_reply(
    user_id: str,
    thread_id: Annotated[str, Path(title="UUID of the Thread to be retrieved")],
    reply: ReplyCreate,
):
    """
    create_reply

    Creates a new (top level) Reply

    """
    with db.transaction:
        user = User.nodes.get(uuid=user_id)
        thread = Thread.nodes.get(uuid=thread_id)

        new_reply = ReplyTopLevel(body=reply.body).save()
        new_reply.parent.connect(thread)
        new_reply.author.connect(user)

    author_data = UserRead(
        uuid=user.uuid,
        name=user.name,
        created_at=user.created_at,
    )

    response = ReplyRead(
        uuid=new_reply.uuid,
        body=new_reply.body,
        author=author_data,
        children=[],
        created_at=new_reply.created_at,
        updated_at=new_reply.updated_at,
        upvotes=0,
        downvotes=0,
    )

    return response


@router.post("/thread/{thread_id}/reply/{reply_id}", response_model=ReplyRead)
async def create_nested_reply(
    user_id: str,
    thread_id: Annotated[str, Path(title="UUID of the Thread to be retrieved")],
    reply_id: Annotated[str, Path(title="UUID of the Reply to be retrieved")],
    reply: ReplyCreate,
):
    """
    create_nested_reply

    Creates a new (nested) Reply

    N.B. the thread ID is included in the path for purely semantic
         reasons; the reply ID is unique and therefore sufficient
         to identify the reply. An incorrect thread ID will be ignored.

    """
    with db.transaction:
        user = User.nodes.get(uuid=user_id)
        parent_reply = Reply.nodes.get(uuid=reply_id)

        new_reply = ReplyLowerLevel(body=reply.body).save()
        new_reply.parent.connect(parent_reply)
        new_reply.author.connect(user)

    author_data = UserRead(
        uuid=user.uuid,
        name=user.name,
        created_at=user.created_at,
    )

    response = ReplyRead(
        uuid=new_reply.uuid,
        body=new_reply.body,
        author=author_data,
        children=[],
        created_at=new_reply.created_at,
        updated_at=new_reply.updated_at,
        upvotes=0,
        downvotes=0,
    )

    return response


### PATCH requests
@router.patch("/thread/{thread_id}/reply/{reply_id}", response_model=ReplyRead)
async def update_reply(
    thread_id: Annotated[str, Path(title="UUID of the Thread to be retrieved")],
    reply_id: Annotated[str, Path(title="UUID of the Reply to be retrieved")],
    reply: ReplyUpdate,
):
    """
    update_reply

    Updates an existing Reply

    N.B. the thread ID is included in the path for purely semantic
         reasons; the reply ID is unique and therefore sufficient
         to identify the reply. An incorrect thread ID will be ignored.

    """
    with db.transaction:
        updated_reply = Reply.nodes.get(uuid=reply_id)
        updated_reply.body = reply.body
        updated_reply.updated_at = datetime.now()
        updated_reply.save()

    response = ReplySimpleRead(
        uuid=updated_reply.uuid,
        body=updated_reply.body,
        created_at=updated_reply.created_at,
        updated_at=updated_reply.updated_at,
    )

    return response


### GET requests
@router.get("/thread/{thread_id}/reply/{reply_id}", response_model=ReplyRead)
async def get_reply(
    thread_id: Annotated[str, Path(title="UUID of the Thread to be retrieved")],
    reply_id: Annotated[str, Path(title="UUID of the Reply to be retrieved")],
):
    with db.transaction:
        reply = Reply.nodes.get(uuid=reply_id)
        author = reply.author.get()
        children = reply.children.all()

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

    response = ReplyRead(
        uuid=reply.uuid,
        body=reply.body,
        author=author_data,
        children=children_data,
        created_at=reply.created_at,
        updated_at=reply.updated_at,
        upvotes=reply.n_upvotes(),
        downvotes=reply.n_downvotes(),
    )

    return response


### DELETE requests
@router.delete("/thread/{thread_id}/reply/{reply_id}", status_code=204)
async def delete_reply(
    thread_id: Annotated[str, Path(title="UUID of the Thread to be retrieved")],
    reply_id: Annotated[str, Path(title="UUID of the Reply to be deleted")],
):
    """
    delete_reply

    Deletes a Reply

    N.B. the thread ID is included in the path for purely semantic
         reasons; the reply ID is unique and therefore sufficient
         to identify the reply. An incorrect thread ID will be ignored.

    """
    with db.transaction:
        reply = Reply.nodes.get(uuid=reply_id)
        reply.delete()
