#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import String, Column

class Amenity(BaseModel, Base):
    """ Amenity class """
    __tablename__ = "amenities"
    __table_args__ = ({'mysql_default_charset': 'latin1'})
    name = Column(String(128), nullable=False)
    
    place_amenities = relationship('Place', secondary='place_amenity', back_populates='amenities')
