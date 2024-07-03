from __future__ import annotations

import enum
from datetime import date, datetime, time  # noqa: TCH003

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_json import MutableJson

from dinghybook.database import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    # rya certificates or similar inc. first_aid
    certificates: Mapped[list[str]] = mapped_column(MutableJson)
    # roles e.g. approved_helm, safety3
    roles: Mapped[list[str]] = mapped_column(MutableJson)

    # def __init__(self, name=None, email=None):
    #     self.name = name
    #     self.email = email

    def __repr__(self):
        return f'<User {self.name!r}>'


class Boat(Base):
    __tablename__ = 'boats'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    type_id: Mapped[int] = mapped_column(ForeignKey('types.id'))
    type: Mapped[Type] = relationship(back_populates='boats')
    in_service: Mapped[bool] = mapped_column(default=True)
    last_updated: Mapped[datetime]
    issues: Mapped[list[Issue]] = relationship(back_populates='boat')


class Type(Base):
    __tablename__ = 'types'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    image: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    boats: Mapped[list[Boat]] = relationship(back_populates='type')
    handicaps: Mapped[list[Handicap]] = relationship(back_populates='type')
    issues: Mapped[list[Issue]] = relationship(back_populates='type')


class Handicap(Base):
    __tablename__ = 'handicaps'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[int]
    type_id: Mapped[int] = mapped_column(ForeignKey('types.id'))
    type: Mapped[Type] = relationship(back_populates='handicaps')
    effective_from: Mapped[date] = mapped_column(nullable=True)
    comment: Mapped[str] = mapped_column(nullable=True)


class Issue(Base):
    __tablename__ = 'issues'
    id: Mapped[int] = mapped_column(primary_key=True)
    type_id: Mapped[int] = mapped_column(ForeignKey('types.id'))
    type: Mapped[Type] = relationship(back_populates='issues')
    boat_id: Mapped[int] = mapped_column(ForeignKey('boats.id'))
    boat: Mapped[Boat] = relationship(back_populates='issues')
    reported: Mapped[datetime]
    comment: Mapped[str]
    more_details: Mapped[str] = mapped_column(nullable=True)


class EventType(enum.Enum):
    race = 1
    cruise = 2
    training = 3
    social = 4


class Event(Base):
    __tablename__ = 'events'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[EventType]
    date: Mapped[date]
    start: Mapped[time] = mapped_column(nullable=True)
    briefing: Mapped[time] = mapped_column(nullable=True)
