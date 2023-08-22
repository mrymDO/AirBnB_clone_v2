#!/usr/bin/python
"""
 DATABASE STORAGE ABSTRACTION
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv

from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {
           'User': User, 'Place': Place,
           'State': State, 'City': City, 'Amenity': Amenity,
           'Review': Review
          }


class DBStorage():
    """db storage class"""
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")
        con = "mysql+mysqldb://{}:{}@{}/{}".format(user, pwd, host, db)
        self.__engine = create_engine(con, pool_pre_ping=True)
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()
        if env == "test":
            Base.metadata.drop_all(self.__engine)
    
    def all(self, cls=None):
        if cls:
            data = self._getAll(cls)
        else:
            data = []
            for classObj in classes:
              data.append(self._getAll(classObj))
        dictData = self._toDict(data)
        return dictData
    def _toDict(self, rows):
        newDict = {}
        for row in rows:
            newDict[row["id"]] = row
        return newDict;
    def _getAll(self, cls):
        data = self.__session.query(cls).all()
        return data