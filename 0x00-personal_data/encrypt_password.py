#!/usr/bin/env python3
"""
 Hashes a password using the bcrypt algorithm.
 Check if a given password matches a hashed password.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using the bcrypt algorithm
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ checking if a given password matches a hashed password
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)