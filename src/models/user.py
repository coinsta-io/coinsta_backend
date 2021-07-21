from sqlalchemy import create_engine, Table, ForeignKey
from sqlalchemy import Column, String, Integer, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

followers = Table('association', Base.metadata,
                          Column('follower_id', Integer, ForeignKey('user.id')),
                          Column('following_id', Integer, ForeignKey('user.id'))
                          )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    followers = relationship("User",
                             secondary=followers,
                             back_populates="following")
    following = relationship("User",
                             secondary=followers,
                             back_populates="followers")
    posts = relationship
    register_date = Column(Date)
    is_admin = Column(Boolean)

    def __str__(self):
        return ""
