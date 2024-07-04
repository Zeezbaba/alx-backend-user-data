#!/usr/bin/env python3
"""Hash a password using bcrypt and
return the hashed password
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Return a hashed password"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """checks if provided password
    matches the hashed password
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
