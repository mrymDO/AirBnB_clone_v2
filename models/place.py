#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from models import storage_type
from models.review import Review
from models.amenity import Amenity
from sqlalchemy.sql.schema import Table

place_amenity = Table(
        'place_amenity',
        Base.metadata,
        Column('place_id', String(60), ForeignKey('places.id'), primary_key=True);
        Column('amenity_id', String(60), ForeignKiey('amenities.id'), primary_key=True)
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

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

    reviews = relationship('Review', backref='place', cascade='delete')
    amenities = relationship('Amenity', secondary=place_amenity, back_populates='place_amenities')

    if storage_type != "db":
        @property
        def reviews(self):
            result = []
            for review in models.storage.all(Review).values():
                if review.place_id == self.id:
                    result.append(review)
            return result

        @property
        def amenities(self):
            return [storage.get(Amenity, amenity_id) for amenity_id in self.amenity_ids]

        @amenities.setter
        def amenities(self, amenity_obj):
            if isinstance(amenity_obj, Amenity):
                self.amenity_ids.append(amenity_obj.id)
