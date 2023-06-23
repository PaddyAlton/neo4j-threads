# schemas.py
# defines the schemas for different requests

from datetime import datetime

from pydantic import BaseModel


### users
class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    uuid: str
    created_at: datetime


### replies
class ReplyBase(BaseModel):
    body: str


class ReplyCreate(ReplyBase):
    pass


class ReplyUpdate(ReplyBase):
    pass


class ReplySimpleRead(ReplyBase):
    uuid: str
    created_at: datetime
    updated_at: datetime


class ReplyReadWithVotes(ReplySimpleRead):
    upvotes: int
    downvotes: int


class ReplyRead(ReplyReadWithVotes):
    author: UserRead
    children: list[ReplySimpleRead]


### threads
class ThreadBase(BaseModel):
    title: str
    body: str


class ThreadCreate(ThreadBase):
    pass


class ThreadUpdate(ThreadBase):
    pass


class ThreadSimpleRead(ThreadBase):
    uuid: str
    created_at: datetime
    updated_at: datetime


class ThreadReadWithVotes(ThreadSimpleRead):
    upvotes: int
    downvotes: int


class ThreadRead(ThreadReadWithVotes):
    author: UserRead
    children: list[ReplySimpleRead]
