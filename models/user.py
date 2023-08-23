#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
<<<<<<< HEAD

=======
from models import storage_type
>>>>>>> 7a7d54a4d52abf8a95f5b213822b1a0eef3d4f67

class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
<<<<<<< HEAD
<<<<<<< HEAD
    places = relationship('Place', backref='user',
                              cascade='all, delete, delete-orphan')
=======
    places = relationship('Place', backref='user', cascade='delete')
>>>>>>> 7a7d54a4d52abf8a95f5b213822b1a0eef3d4f67
=======
    places = relationship('Place', backref='users', cascade='delete')
>>>>>>> a61bf1430bea105835c044a5a0df2653ee5bc0a0
