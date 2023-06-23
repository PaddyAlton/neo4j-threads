# app.py
# defines the FastAPI Application

import json
import re

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from neomodel import db
from neomodel.exceptions import DoesNotExist, UniqueProperty
from uvicorn import run as serve

from src.controllers import replies, threads, users, votes
from src.models import ReplyLowerLevel, ReplyTopLevel, Thread, User
from src.services.config import AppSettings, get_settings
from src.services.graph import build_cs, graph_init
from src.services.logs import logger

app = FastAPI(
    title="Threads",
    description="A FastAPI app for demonstrating a Neo4J-based forum feature.",
    version="0.0.1",
)


@db.transaction
def seed_data():
    u1 = User(name="John Smith").save()
    u2 = User(name="Joanne Bloggs").save()
    u3 = User(name="Immanuel Kant").save()

    t1 = Thread(
        title="How now, brown cow?",
        body="Hi guys! I was wondering whether you could answer this question.",
    ).save()
    t1.author.connect(u1)

    r1 = ReplyTopLevel(body="The question is unanswerable.").save()
    r1.author.connect(u2)
    r1.parent.connect(t1)

    r2a = ReplyLowerLevel(body="Are you sure?").save()
    r2a.parent.connect(r1)
    r2a.author.connect(u1)

    r2b = ReplyLowerLevel(body="I do not believe that to be the case.").save()
    r2b.parent.connect(r1)
    r2b.author.connect(u3)


@app.on_event("startup")
def prepare_graph_database(settings: AppSettings = Depends(get_settings)):
    settings = get_settings()
    connection_string = build_cs(
        settings.dbuser,
        settings.dbpass,
        settings.dbhost,
        settings.dbname,
    )
    graph_init(connection_string)
    try:  # if the database is empty, add some data
        seed_data()
    except UniqueProperty:
        pass  # catch constraint violation if database is not empty
    logger.info("Neomodel configured. Starting application.")


@app.get("/")
def root() -> str:
    return f"Welcome to {app.title}!"


### include routers


app.include_router(replies.router)
app.include_router(threads.router)
app.include_router(users.router)
app.include_router(votes.router)


### exceptions


def parse_neomodel_exception(exc: DoesNotExist) -> dict:
    """
    parse_neomodel_exception

    Neomodel 'DoesNotExist' exceptions contain a message flagging the
    identifiers used to attempt to locate a resource. We return these
    as a dictionary.

    Input:
        exc - the exception that was raised

    Output:
        exc_data - data extracted from the exception

    """
    exc_data = json.loads(re.sub("'", '"', exc.message))
    return exc_data


@app.exception_handler(UniqueProperty)
async def duplicate_exception_handler(request: Request, exc: UniqueProperty):
    return JSONResponse(status_code=409, content={"message": exc.message})


@app.exception_handler(Thread.DoesNotExist)
async def missing_thread_exception_handler(request: Request, exc: Thread.DoesNotExist):
    uuid = parse_neomodel_exception(exc).get("uuid")
    return JSONResponse(
        status_code=404,
        content={"message": f"Thread with UUID {uuid} not found"},
    )


@app.exception_handler(User.DoesNotExist)
async def missing_user_exception_handler(request: Request, exc: User.DoesNotExist):
    uuid = parse_neomodel_exception(exc).get("uuid")
    return JSONResponse(
        status_code=404,
        content={"message": f"User with UUID {uuid} not found"},
    )


### serve (N.B. in practice we'll usually use uvicorn directly)


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8765)
