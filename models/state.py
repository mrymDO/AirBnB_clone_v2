#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models import storage_type


class State(BaseModel, Base):
    """ State class """

    __tablename__ = "states"
    __table_args__ = ({'mysql_default_charset': 'latin1'})

    name = Column(String(128), nullable=False)

    if storage_type == 'db':
        
        cities = relationship('City', back_populates='state',
                              cascade='all, delete, save-update')
    else:
        @property
        def cities(self):
            """ returns list of City instances """
            from models import storage
            from models.city import City
            city_instances = storage.all(City)
            return [city for city in city_instances.values() if city.state_id == self.id]            
