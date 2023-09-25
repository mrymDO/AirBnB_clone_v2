#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models import storage_type



place_amenity = Table("place_amenity", Base.metadata,
                          Column("place_id", String(60),
                                 ForeignKey("places.id"),
                                 primary_key=True,
                                 nullable=False),
                          Column("amenity_id", String(60),
                                 ForeignKey("amenities.id"),
                                 primary_key=True,
                                 nullable=False)
                    )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    #__table_args__ = ({'mysql_default_charset': 'latin1'})

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(String(1024), nullable=True)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)



    user = relationship('User', back_populates='places')
    cities = relationship('City', back_populates='places')

    reviews = relationship('Review', back_populates='place', cascade='all, delete, save-update')
    amenities = relationship('Amenity', secondary='place_amenity', viewonly=False, back_populates='place_amenities')
    amenity_ids = []

    if storage_type != "db":
        @property
        def reviews(self):
            """ return list of review instances """
            from models import storage
            from models.review import Review

            result = []
            for review in storage.all(Review).values():
                if review.place_id == self.id:
                    result.append(review)
            return result

        @property
        def amenities(self):
            """ getter """
            from models import storage
            amenity_list = []
            for amenity in list(storage.all(Amenity).values()):
                if amenity.id in self.amenity_ids: 
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, value):
            """ setter """
            from models.amenity import Amenity
            if type(value) == Amenity:
                self.amenity_ids.append(value.id)
