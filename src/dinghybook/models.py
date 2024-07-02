from __future__ import annotations

from datetime import date, datetime  # noqa: TCH003

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_json import MutableJson

from dinghybook.database import db


class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    profile: Mapped[Profile] = relationship(back_populates='user', cascade='all, delete-orphan')

    # def __init__(self, name=None, email=None):
    #     self.name = name
    #     self.email = email

    def __repr__(self):
        return f'<User {self.name!r}>'


class Profile(db.Model):
    __tablename__ = 'user_profiles'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped[User] = relationship(back_populates='profile')
    certificates: Mapped[list[str]] = mapped_column(MutableJson)  # rya certificates or similar inc. first_aid
    roles: Mapped[list[str]] = mapped_column(MutableJson)  # roles e.g. approved_helm, safety3

    # def __init__(self, name=None, email=None):
    #     self.name = name
    #     self.email = email

    def __repr__(self):
        return f'<Profile for {self.user.name!r}>'


class Boat(db.Model):
    __tablename__ = 'boats'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    type_id: Mapped[int] = mapped_column(ForeignKey('types.id'))
    type: Mapped[Type] = relationship(back_populates='boats')
    in_service: Mapped[bool] = mapped_column(default=True)
    last_updated: Mapped[datetime]
    issues: Mapped[list[Issue]] = relationship(back_populates='boat')


class Type(db.Model):
    __tablename__ = 'types'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    image: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    boats: Mapped[list[Boat]] = relationship(back_populates='type')
    handicaps: Mapped[list[Handicap]] = relationship(back_populates='type')
    issues: Mapped[list[Issue]] = relationship(back_populates='type')


class Handicap(db.Model):
    __tablename__ = 'handicaps'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[int]
    type_id: Mapped[int] = mapped_column(ForeignKey('types.id'))
    type: Mapped[Type] = relationship(back_populates='handicaps')
    effective_from: Mapped[date] = mapped_column(nullable=True)
    comment: Mapped[str] = mapped_column(nullable=True)


class Issue(db.Model):
    __tablename__ = 'issues'
    id: Mapped[int] = mapped_column(primary_key=True)
    type_id: Mapped[int] = mapped_column(ForeignKey('types.id'))
    type: Mapped[Type] = relationship(back_populates='issues')
    boat_id: Mapped[int] = mapped_column(ForeignKey('boats.id'))
    boat: Mapped[Boat] = relationship(back_populates='issues')
    reported: Mapped[datetime]
    comment: Mapped[str]
    more_details: Mapped[str] = mapped_column(nullable=True)
