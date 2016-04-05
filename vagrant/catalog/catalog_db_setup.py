import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'
	
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	email = Column(String(250), unique=True)
	picture = Column(String(250))

class Category(Base):
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
		

class Item(Base):
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

engine = create_engine('sqlite:///catalogitemswithusers.db')
Base.metadata.create_all(engine)

