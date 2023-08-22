#!/usr/bin/python
"""
 DATABASE STORAGE ABSTRACTION
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base_model import Base
from os import getenv

class DBStorage():
    """db storage class"""
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        con = "mysql+mysqldb://{}:{}@{}/{}".format(user, pwd, host, db)
        self.__engine = create_engine(con, pool_pre_ping=True)
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()
    