from typing import Annotated
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone


class RoomParticipantLink(SQLModel, table=True):
    __tablename__ = 'base_room_participants'
    room_id: int = Field(foreign_key="base_room.id", primary_key=True)
    user_id: int = Field(foreign_key="base_user.id", primary_key=True)


class UserBase(SQLModel):
    username: str = Field(max_length=150, unique=True, index=True)
    email: str | None = Field(default=None, unique=True, max_length=254)
    name: str | None = Field(default=None, max_length=200)


class User(UserBase, table=True):
    __tablename__ = 'base_user'
    id: int | None = Field(default=None, primary_key=True, index=True)
    password: str
    bio: str | None = Field(default=None)
    avatar: str | None = Field(default="avatar.svg")
    is_active: bool = Field(default=True)
    is_staff: bool = Field(default=False)
    is_superuser: bool = Field(default=False)
    date_joined: Annotated[datetime, Field(
        default_factory=lambda: datetime.now(timezone.utc))]
    last_login: datetime | None = Field(default=None)

    # Relationships
    hosted_rooms: list['Room'] = Relationship(back_populates='host')
    joined_rooms: list['Room'] = Relationship(
        back_populates='participants', link_model=RoomParticipantLink)
    messages: list["Message"] = Relationship(
        back_populates="user", cascade_delete=True)


class UserPublic(UserBase):
    id: int
    date_joined: datetime
    last_login: datetime | None
    bio: str | None


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    username: str | None = Field(default=None, max_length=150)
    password: str | None = Field(default=None)
    bio: str | None = Field(default=None)
    avatar: str | None = Field(default="avatar.svg")


class Topic(SQLModel, table=True):
    __tablename__ = 'base_topic'
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=200)

    rooms: list["Room"] = Relationship(back_populates='topic')


class Room(SQLModel, table=True):
    __tablename__ = 'base_room'
    id: int | None = Field(default=None, primary_key=True)
    host_id: int | None = Field(
        foreign_key="base_user.id", nullable=True)  # ForeignKey to User
    topic_id: int | None = Field(
        foreign_key="base_topic.id", nullable=True, ondelete='SET NULL')  # ForeignKey to Topic
    name: str = Field(max_length=200)
    description: str | None = Field(default=None)
    joined_count: int | None = Field(default=0)  # Tracks participant count
    updated: datetime | None = Field(default=None)
    created: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    topic: "Topic" = Relationship(back_populates="rooms")
    host: "User" = Relationship(back_populates="hosted_rooms")
    participants: list["User"] = Relationship(
        back_populates="joined_rooms", link_model=RoomParticipantLink)
    messages: list["Message"] = Relationship(
        back_populates="room", cascade_delete=True)


class Message(SQLModel, table=True):
    __tablename__ = "base_message"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="base_user.id", ondelete='CASCADE')
    room_id: int = Field(foreign_key="base_room.id", ondelete='CASCADE')
    body: str
    updated: datetime | None = Field(default=None)
    created: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    user: "User" = Relationship(back_populates="messages")
    room: "Room" = Relationship(back_populates="messages")
