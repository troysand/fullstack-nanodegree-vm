import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Category(Base):
	__tablename__ = 'category'
	
	id = Column(Integer, primary_key=True)
	name = Column(String(80), nullable=False)
	description = Column(String(250))
	
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
	
	@property
	def serialize(self):
		"""Return object data in an easily serializable format"""
		return {
			'name': self.name,
			'id': self.id,
			'description': self.description,
			'category_id': self.category_id,
		}

