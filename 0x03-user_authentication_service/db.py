#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import User
from user import Base


class DB:
    """DB class
        methods:
            ___init__
            _session
            add_user
            find_user
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Returns a User object.
        The method should save the user to the database
        Args:
            email: str
            hashed_password: str
        """
        new_user = User(email=email,
                        hashed_password=hashed_password
                        )
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by arbitrary keyword
        """
        if not kwargs:
            raise InvalidRequestError("No filter arguments provided.")

        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound("NO user found")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid result")

    def update_user(self, user_id, **kwargs) -> None:
        """
        Use find_user_by to locate the user to update,
        then will update the user’s attributes as passed
        in the method’s arguments then commit changes to the database.

        If an argument that does not correspond to a user attribute
        is passed, raise a ValueError.
        """
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError()
            setattr(user, key, value)

        self._session.commit()
