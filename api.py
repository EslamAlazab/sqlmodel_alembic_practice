from typing import Annotated
from fastapi import FastAPI, Query, HTTPException
from sqlmodel import SQLModel, select
from sqlalchemy.orm import joinedload

from models import User, UserPublic, UserCreate, UserUpdate, Room, Topic
from database import SessionDep, AsyncSessionDep


app = FastAPI()


@app.get('/users')
def get_users(db: SessionDep, offset: int = 0,
              limit: Annotated[int, Query(le=100)] = 100) -> list[UserPublic]:
    users = db.exec(select(User).offset(offset).limit(limit)).all()
    return users


@app.get("/users/{user_id}", response_model=UserPublic)
def read_hero(user_id: int, session: SessionDep) -> UserPublic:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Hero not found")
    return user


@app.post("/users/", response_model=UserPublic)
def create_hero(user: UserCreate, session: SessionDep) -> User:
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.patch("/users/{user_id}", response_model=UserPublic)
def update_hero(user_id: int, user: UserUpdate, session: SessionDep):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db


class RoomResponse(SQLModel):
    id: int
    name: str
    description: str | None
    joined_count: int
    host: UserPublic | None  # Include relevant host fields
    topic: Topic | None


@app.get('/rooms', response_model=list[RoomResponse])
def get_rooms(session: SessionDep):
    rooms = session.exec(select(Room).options(
        joinedload(Room.host), joinedload(Room.topic))).all()
    return rooms


@app.get('/async-rooms', response_model=list[RoomResponse])
async def get_async_rooms(session: AsyncSessionDep):
    stmt = select(Room).options(
        joinedload(Room.host), joinedload(Room.topic))
    rooms = (await session.scalars(stmt)).all()
    return rooms
