#
# This file implements the CRUD functions for the 
# catalog app.
#

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from catalog_db_setup import Base, Category, Item, User

engine = create_engine('sqlite:///catalogitemswithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create a new category in the database.
def createCategory(name, description, user_id):
	newCategory = Category(name=name, description=description, user_id=user_id)
	session.add(newCategory)
	session.commit()

# Create a new item in the database.
def createItem(name, description, category_id, user_id):
	newItem = Item(name=name, description=description, 
		category_id=category_id, user_id=user_id)
	session.add(newItem)
	session.commit()

# Create a new user in the database.
def createUser(name, email, picture):
	newUser = User(name=name, email=email, picture=picture)
	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(email=email).one()
	return user.id

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

# Get a list of the latest items added to the database. max is the maximum
# num of items to return in the list. 
def readLatestItems(max):
	items = session.query(Item).all()
	if len(items) > max:
		return items[len(items)-1:len(items)-max-1:-1]
	else:
		return items[::-1]

# Read a user from the database.
def readUserInfo(user_id):
	try:
		user = session.query(User).filter_by(id=user_id).one()
		return user
	except:
		return None

# Get the user id from the database given an email address.
def readUserID(email):
	try:
		user = session.query(User).filter_by(email=email).one()
		return user.id
	except:
		return None

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
	

