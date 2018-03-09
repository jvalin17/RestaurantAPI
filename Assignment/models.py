import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime,  PrimaryKeyConstraint, Float, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime

Base = declarative_base()

class Restaurant(Base):

    __tablename__ = 'restaurant'

    restaurant_name = Column(String(50), primary_key=True)
    restaurant_category = Column(String(50))
    addresses = relationship ('Address', backref = "post" , cascade = "all, delete-orphan", lazy='dynamic' )

class User(Base):

    __tablename__ = 'user'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    phone = Column(Integer, unique=True)

    

class Address(Base):

    __tablename__ = 'address'
    
    address_id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String(200))
    city = Column(String(20))
    state = Column(String(20))
    zipcode = Column(Integer)
    restaurant_name = Column(String(50), ForeignKey('restaurant.restaurant_name'),nullable=False)


class Rating(Base):

    __tablename__ = 'rating'

    user_id = Column(Integer, ForeignKey('user.user_id'))
    address_id = Column(Integer, ForeignKey('address.address_id'))
    restaurant_name = Column(String(50), ForeignKey('restaurant.restaurant_name'))
    date = Column(DateTime, default=datetime.datetime.utcnow())
    cost_rating = Column(Integer)
    food_rating = Column(Integer)
    cleanliness_rating = Column(Integer)
    service_rating = Column(Integer)
    total_score = Column(Float)

    PrimaryKeyConstraint(user_id, address_id)
    #__table_args__ = (UniqueConstraint(user_id, address_id),)

engine = create_engine('sqlite:///restaurantRatingAPI.db')


Base.metadata.create_all(engine)