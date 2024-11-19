#!/usr/bin/env python3
"""
In this module we create a SQLAlchemy model named
User for a database table named users
(by using the mapping declaration of SQLAlchemy).

The model will have the following attributes:
class: User
Args:
    id(int): the integer primary key
    email(str), a non-nullable string
    hashed_password(str), a non-nullable string
    session_id(str): a nullable string
    reset_token(str): a nullable string
"""
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    """
    In this module we create a SQLAlchemy model named
    User for a database table named users
    (by using the mapping declaration of SQLAlchemy).

    The model will have the following attributes:
    class: User
    Args:
        id(int): the integer primary key
        email(str), a non-nullable string
    hashed_password(str), a non-nullable string
    session_id(str): a nullable string
"""
    __tablename__ = 'users'
    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(250), nullable=False)
    hashed_password: str = Column(String(250), nullable=False)
    session_id: str = Column(String(250), nullable=True)
    reset_token: str = Column(String(250), nullable=True)
