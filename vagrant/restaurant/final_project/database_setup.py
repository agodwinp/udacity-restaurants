import sys

# these will come in handy when writing our mapper code
from sqlalchemy import Column, ForeignKey, Integer, String

# we will use this in the configuration and class code, to inherit some features from declarative base
from sqlalchemy.ext.declarative import declarative_base

# in order to create our foreign key relationships, will be useful when writing the mapper
from sqlalchemy.orm import relationship

# we will use this in the configuration code at the end of the file
from sqlalchemy import create_engine

# this will let SQLAlchemy know that the classes are special SQLAlchemy classes, that correspond to tables in our database
Base = declarative_base()


# class code
# inside each of these classes, we must create a table representation
class Restaurant(Base):
    __tablename__ = 'restaurant'
    # mapper code
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class MenuItem(Base):
    __tablename__ = 'menu_item'
    # mapper code
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    # We added this serialize function to be able to send JSON objects in a
    # serializable format
    @property
    def serialize(self):

        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
        }


###### insert at end of file ######

# since we are using sqlite3 for this lesson, create_engine will create a new file that we can use
# similarly to a more robust db like mysql or postgres
engine = create_engine('sqlite:///restaurantmenu.db')

# this goes into the db and adds the classes that we will soon create as new tables in the db
Base.metadata.create_all(engine)
