#
#  Defines the database tables and the ORM for the catalog app.
#
from sqlalchemy import (
    Column,
    create_engine,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

#
# The User class represents a registered user of the catalog application.
#


class User(Base):
    """
    The User class represents a registered user of the catalog
    application.

    Fields:
            id: The user id
            name: The name of the user
            email: The email of the user
            picture: A picture representing the user
    """

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), unique=True)
    picture = Column(String(250))

#
# The Category class represents a category in the catalog.
#


class Category(Base):
    """
    The Category class represents a category in the catalog. Every
    item in the catalog belongs to exactly one category.

    Fields:
            id: The category id
            name: The category name
            description: A description of the category (optional)
            user_id: The id of the user that created the category
    """

    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in an easily serializable format"""
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
        }


#
# The Item class represents an item in the catalog.
#
class Item(Base):
    """
    The Item class represents an item in the catalog. Each item 
    belongs to a category. The user that created the item is the
    item's owner and only the owner can delete or modify the item.

    Fields:
            id: The item id
            name: The item name
            description: A description of the item (optional)
            category_id: The id of the item's category
            user_id: The id of the item's owner
    """

    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in an easily serializable format"""
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'category_id': self.category_id,
        }

# Create the database
engine = create_engine('sqlite:///catalogitemswithusers.db')
Base.metadata.create_all(engine)
