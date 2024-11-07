#!/usr/bin/env python3
"""
a hash_password function that expects
one string argument name password and
returns a salted, hashed password, which is a byte string.
 """
import bcrypt


def hash_password(password: str):
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
