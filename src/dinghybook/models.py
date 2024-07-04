from __future__ import annotations

from datetime import date, datetime, time  # noqa: TCH003

from sqlalchemy import Column, ForeignKey, Table, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_json import MutableJson

from dinghybook.database import Base

type_eventtype_table = Table(
    'type_eventtype_assoc',
    Base.metadata,
    Column('type_id', ForeignKey('types.id'), primary_key=True),
    Column('event_type_id', ForeignKey('event_types.id'), primary_key=True),
)

boat_event_table = Table(
    'boat_event_assoc',
    Base.metadata,
    Column('boat_id', ForeignKey('boats.id'), primary_key=True),
    Column('event_id', ForeignKey('events.id'), primary_key=True),
)


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    # rya certificates or similar inc. first_aid
    certificates: Mapped[list[str]] = mapped_column(MutableJson)
    # roles e.g. approved_helm, safety3
    roles: Mapped[list[str]] = mapped_column(MutableJson)
    bookings: Mapped[list[Booking]] = relationship(back_populates='user')
    time_created: Mapped[datetime] = mapped_column(server_default=func.now())
    time_updated: Mapped[datetime] = mapped_column(server_onupdate=func.now())

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
    events: Mapped[list[Event]] = relationship(secondary=type_eventtype_table, back_populates='boats')


class Type(Base):
    __tablename__ = 'types'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    image: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    boats: Mapped[list[Boat]] = relationship(back_populates='type')
    handicaps: Mapped[list[Handicap]] = relationship(back_populates='type')
    issues: Mapped[list[Issue]] = relationship(back_populates='type')
    event_types: Mapped[list[EventType]] = relationship(secondary=type_eventtype_table, back_populates='types')


class Handicap(Base):
    __tablename__ = 'handicaps'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[int]
    type_id: Mapped[int] = mapped_column(ForeignKey('types.id'))
    type: Mapped[Type] = relationship(back_populates='handicaps')
    effective_from: Mapped[date] = mapped_column(nullable=True)
    comment: Mapped[str] = mapped_column(nullable=True)
    time_created: Mapped[datetime] = mapped_column(server_default=func.now())
    time_updated: Mapped[datetime] = mapped_column(server_onupdate=func.now())


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
    time_created: Mapped[datetime] = mapped_column(server_default=func.now())
    time_updated: Mapped[datetime] = mapped_column(server_onupdate=func.now())


class Event(Base):
    __tablename__ = 'events'
    id: Mapped[int] = mapped_column(primary_key=True)
    type_id: Mapped[int] = mapped_column(ForeignKey('event_types.id'))
    type: Mapped[EventType] = relationship(back_populates='events')
    date: Mapped[date]
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    start: Mapped[time] = mapped_column(nullable=True)
    briefing: Mapped[time] = mapped_column(nullable=True)
    bookings: Mapped[list[Booking]] = relationship(back_populates='event')
    extra_roles: Mapped[list[str]] = mapped_column(MutableJson, nullable=True)
    time_created: Mapped[datetime] = mapped_column(server_default=func.now())
    time_updated: Mapped[datetime] = mapped_column(server_onupdate=func.now())


class EventType(Base):
    __tablename__ = 'event_types'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    events: Mapped[list[Event]] = relationship(back_populates='type')
    needed_roles: Mapped[list[str]] = mapped_column(MutableJson, nullable=True)
    types: Mapped[list[Type]] = relationship(secondary=type_eventtype_table, back_populates='event_types')


class Booking(Base):
    __tablename__ = 'bookings'
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey('events.id'), primary_key=True)
    is_helm: Mapped[bool] = mapped_column(default=False)
    is_crew: Mapped[bool] = mapped_column(default=False)
    has_paid: Mapped[bool] = mapped_column(default=False)
    date_paid: Mapped[datetime] = mapped_column(nullable=True)
    user: Mapped[User] = relationship(back_populates='bookings')
    event: Mapped[Event] = relationship(back_populates='bookings')
    time_created: Mapped[datetime] = mapped_column(server_default=func.now())
    time_updated: Mapped[datetime] = mapped_column(server_onupdate=func.now())
