#!/usr/bin/python3
"""
 DATABASE STORAGE ABSTRACTION
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from os import getenv

from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review



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

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ returns dict of models """
        results_dict = {}
        if cls is None:
            models = [User, State, City, Amenity, Place, Review]
            results_list = []
            for model in models:
                query_list = self.__session.query(model).all()
                results_list = results_list + query_list
        else:
            if type(cls) == str:
                cls = eval(cls)
            results_list = self.__session.query(cls).all()

        for result in results_list:
            results_dict[f"{type(result).__name__}.{result.id}"] = result

        return results_dict

    def new(self, obj):
        """ add new object to current db """
        if obj:
            self.__session.add(obj)

    def save(self):
        """ Commit all changes of current db """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete from current db """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Create tables and current db session """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
                bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Closes the SQLAlchemy session."""
        self.__session.close()
