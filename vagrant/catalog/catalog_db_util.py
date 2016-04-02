from sqlalchemy import create_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from catalog_db import Base, Category, Item

# Create a new category in the database.
def createCategory(name, description):
	newCategory = Category(name, description)
	session.add(newCategory)
	session.commit()

# Create a new item in the database.
def createItem(name, description, category_id):
	newItem = Item(name=name, description=description, category_id=category_id)
	session.add(newItem)
	session.commit()

# Read the catalog item with the given item id.
def readItem(item_id):
	try:
		item = session.query(Item).filter_by(id=item_id).one()
		return item
	except NoResultFound:
		return None

# Read the list of items for a given category
def readItems(category_id):
	items = session.query(Item).filter_by(category_id=category_id).all()
	return items

# Read the list of all items in the database.
def readAllItems():
	items = session.query(Item).all()
	return items

# Read the category with the given category id.
def readCategory(category_id):
	try:
		category = session.query(Category).filter_by(id=category_id).one()
		return category
	except NoResultFound:
		return None
		

# Read a list of all of the categories in the database.
def readCategories():
	categories = session.query(Category).all()
	return categories

# Update a category in the database.
def updateCategory(category_id, name, description):
	category = readCategory(category_id)
	category.name = name
	category.description = description
	session.add(category)
	session.commit()

# Update an item in the database.
def updateItem(item_id, name, description):
	item = readItem(item_id)
	item.name = name
	item.description = description
	session.add(item)
	session.commit()

# Delete an item from the database.
def deleteItem(item_id):
	item = readItem(item_id)
	session.delete(item)
	session.commit()
	
engine = create_engine('sqlite:///catalogitems.db')

Base.metadata.create_all(engine)

engine = create_engine('sqlite:///catalogitems.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
