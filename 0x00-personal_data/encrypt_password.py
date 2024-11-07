#!/usr/bin/env python3
"""
a hash_password function that expects
one string argument name password and
returns a salted, hashed password, which is a byte string.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    a hash_password function that expects
    one string argument name password and
    returns a salted, hashed password, which is a byte string.
    Args:
        password(str): password
    """
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password.encode(), salt)
    return hash_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
     expects 2 arguments and returns a boolean.

    Arg:

    hashed_password: bytes type
    password: string type
    """
    compare = bcrypt.checkpw(password.encode(), hashed_password)
    return compare
