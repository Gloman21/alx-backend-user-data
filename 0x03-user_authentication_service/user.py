#!/usr/bin/python3
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """Represents a record from the `users` table.

    Attributes:
        id (int): The primary key, unique identifier for each user.
        email (str): The user's email, must be non-nullable.
        hashed_password (str): The user's hashed password, must be non-nullable.
        session_id (str): Optional session ID for user session management.
        reset_token (str): Optional token for password reset functionality.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)