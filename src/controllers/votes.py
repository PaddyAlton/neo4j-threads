# controllers/votes.py
# controllers for Upvotes and Downvotes

from fastapi import APIRouter
from neomodel import db

from src.models import Reply, Thread, User
from src.schemas import ReplyReadWithVotes, ThreadReadWithVotes

router = APIRouter(tags=["votes"])


### POST requests
@router.post("/thread/{thread_id}/upvote", response_model=ThreadReadWithVotes)
async def upvote_thread(user_id: str, thread_id: str):
    """
    upvote_thread

    Adds an upvote to a Thread

    """
    with db.transaction:
        user = User.nodes.get(uuid=user_id)
        thread = Thread.nodes.get(uuid=thread_id)
        thread.upvoters.connect(user)

    response = ThreadReadWithVotes(
        uuid=thread.uuid,
        title=thread.title,
        body=thread.body,
        created_at=thread.created_at,
        updated_at=thread.updated_at,
        upvotes=thread.n_upvotes(),
        downvotes=thread.n_downvotes(),
    )

    return response


@router.post(
    "/thread/{thread_id}/reply/{reply_id}/upvote", response_model=ReplyReadWithVotes
)
async def upvote_reply(
    user_id: str,
    thread_id: str,
    reply_id: str,
):
    """
    upvote_reply

    Adds an upvote to a Reply

    N.B. the thread ID is included in the path for purely semantic
         reasons; the reply ID is unique and therefore sufficient
         to identify the reply. An incorrect thread ID will be ignored.

    """
    with db.transaction:
        user = User.nodes.get(uuid=user_id)
        reply = Reply.nodes.get(uuid=reply_id)
        reply.upvoters.connect(user)

    response = ReplyReadWithVotes(
        uuid=reply.uuid,
        body=reply.body,
        created_at=reply.created_at,
        updated_at=reply.updated_at,
        upvotes=reply.n_upvotes(),
        downvotes=reply.n_downvotes(),
    )

    return response


@router.post("/thread/{thread_id}/downvote", response_model=ThreadReadWithVotes)
async def downvote_thread(user_id: str, thread_id: str):
    """
    upvote_thread

    Adds a downvote to a Thread

    """
    with db.transaction:
        user = User.nodes.get(uuid=user_id)
        thread = Thread.nodes.get(uuid=thread_id)
        thread.downvoters.connect(user)

    response = ThreadReadWithVotes(
        uuid=thread.uuid,
        title=thread.title,
        body=thread.body,
        created_at=thread.created_at,
        updated_at=thread.updated_at,
        upvotes=thread.n_upvotes(),
        downvotes=thread.n_downvotes(),
    )

    return response


@router.post(
    "/thread/{thread_id}/reply/{reply_id}/downvote", response_model=ReplyReadWithVotes
)
async def downvote_reply(
    user_id: str,
    thread_id: str,
    reply_id: str,
):
    """
    downvote_reply

    Adds a downvote to a Reply

    N.B. the thread ID is included in the path for purely semantic
         reasons; the reply ID is unique and therefore sufficient
         to identify the reply. An incorrect thread ID will be ignored.

    """
    with db.transaction:
        user = User.nodes.get(uuid=user_id)
        reply = Reply.nodes.get(uuid=reply_id)
        reply.downvoters.connect(user)

    response = ReplyReadWithVotes(
        uuid=reply.uuid,
        body=reply.body,
        created_at=reply.created_at,
        updated_at=reply.updated_at,
        upvotes=reply.n_upvotes(),
        downvotes=reply.n_downvotes(),
    )

    return response


### DELETE requests
@router.delete("/thread/{thread_id}/upvote", status_code=204)
async def remove_upvote_from_thread(user_id: str, thread_id: str):
    """
    remove_upvote_from_thread

    Removes an upvote from a Thread

    """
    with db.transaction:
        user = User.nodes.get(uuid=user_id)
        thread = Thread.nodes.get(uuid=thread_id)
        thread.upvoters.disconnect(user)


@router.delete("/thread/{thread_id}/reply/{reply_id}/upvote", status_code=204)
async def remove_upvote_from_reply(
    user_id: str,
    thread_id: str,
    reply_id: str,
):
    """
    remove_upvote_from_reply

    Removes an upvote from a Reply

    N.B. the thread ID is included in the path for purely semantic
         reasons; the reply ID is unique and therefore sufficient
         to identify the reply. An incorrect thread ID will be ignored.

    """
    with db.transaction:
        user = User.nodes.get(uuid=user_id)
        reply = Reply.nodes.get(uuid=reply_id)
        reply.upvoters.disconnect(user)


@router.delete("/thread/{thread_id}/downvote", status_code=204)
async def remove_downvote_from_thread(user_id: str, thread_id: str):
    """
    remove_downvote_from_thread

    Removes a downvote from a Thread

    """
    with db.transaction:
        user = User.nodes.get(uuid=user_id)
        thread = Thread.nodes.get(uuid=thread_id)
        thread.downvoters.disconnect(user)


@router.delete("/thread/{thread_id}/reply/{reply_id}/downvote", status_code=204)
async def remove_downvote_from_reply(
    user_id: str,
    thread_id: str,
    reply_id: str,
):
    """
    remove_downvote_from_reply

    Removes a downvote from a Reply

    N.B. the thread ID is included in the path for purely semantic
         reasons; the reply ID is unique and therefore sufficient
         to identify the reply. An incorrect thread ID will be ignored.

    """
    with db.transaction:
        user = User.nodes.get(uuid=user_id)
        reply = Reply.nodes.get(uuid=reply_id)
        reply.downvoters.disconnect(user)
