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
	"""
	Create a new category in the database.
	
	Args:
		name: The name for the new category
		description: A description of the new category
		user_id: The id of the user creating the category
	
	Returns:
		Nothing
	"""
	
	newCategory = Category(name=name, description=description, user_id=user_id)
	session.add(newCategory)
	session.commit()

# Create a new item in the database.
def createItem(name, description, category_id, user_id):
	"""
	Create a new item in the database.
	
	Args:
		name: The name of the new item
		description: A description of the new item
		category_id: The id of the item's category
		user_id: The user id of the item's owner
	
	Returns:
		Nothing
	"""
	
	newItem = Item(name=name, description=description, 
		category_id=category_id, user_id=user_id)
	session.add(newItem)
	session.commit()

# Create a new user in the database.
def createUser(name, email, picture):
	"""
	Create a new user in the database.
	
	Args:
		name: The name of the new user
		email: The email address of the new user
		picture: A URL to the user's picture
	
	Returns:
		The id of the newly created user
	"""
	
	newUser = User(name=name, email=email, picture=picture)
	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(email=email).one()
	return user.id

# Read the catalog item with the given item id.
def readItem(item_id):
	"""
	Read the catalog item with the given item id.
	
	Args:
		item_id: The id of item to find
		
	Returns:
		item: The item with the provided id, or None if item 
		doesnt exist
	"""
	
	try:
		item = session.query(Item).filter_by(id=item_id).one()
		return item
	except NoResultFound:
		return None

# Read the list of items for a given category
def readItems(category_id):
	"""
	Read the list of items for a given category
	
	Args:
		category_id: The id of the category
	
	Returns:
		items: a list of all the items in the category
	"""
	
	items = session.query(Item).filter_by(category_id=category_id).all()
	return items

# Read the list of all items in the database.
def readAllItems():
	"""
	Read the list of all items in the databse.
	
	Args:
		None
	
	Returns:
		items: a list of all items in the database
	"""
	
	items = session.query(Item).all()
	return items

# Read the category with the given category id.
def readCategory(category_id):
	"""
	Read the category with the given category id.
	
	Args:
		category_id: The id of the category to read
	
	Returns:
		category: The category with the provided id, or
		None if category doesn't exist
	"""
	
	try:
		category = session.query(Category).filter_by(id=category_id).one()
		return category
	except NoResultFound:
		return None

# Read a list of all of the categories in the database.
def readCategories():
	"""
	Read a list of all the categories in the database.
	
	Args:
		None
	
	Returns:
		categories: a list of all the categories
	"""
	
	categories = session.query(Category).all()
	return categories

# Get a list of the latest items added to the database. max is the maximum
# num of items to return in the list. 
def readLatestItems(max):
	"""
	Get a list of the latest items added to the database.
	
	Args:
		max: maximum num of items to read
	
	Returns:
		items: a list of the latest items (most recent first)
	"""
	
	items = session.query(Item).all()
	if len(items) > max:
		return items[len(items)-1:len(items)-max-1:-1]
	else:
		return items[::-1]

# Read a user from the database.
def readUserInfo(user_id):
	"""
	Read a user from the database.
	
	Args:
		user_id: The id of the user
	
	Returns:
		user: The user with the provided user id, or 
		None of user doesn't exist.
	"""
	
	try:
		user = session.query(User).filter_by(id=user_id).one()
		return user
	except:
		return None

# Get the user id from the database given an email address.
def readUserID(email):
	"""
	Get the user id from the database given an email address.
	
	Args:
		email: The email address of the user to find
	
	Returns:
		user: The user with the provided email address, or 
		None if user doesn't exist.
	"""
	
	try:
		user = session.query(User).filter_by(email=email).one()
		return user.id
	except:
		return None

# Update a category in the database.
def updateCategory(category_id, name, description):
	"""
	Update a category in the database.
	
	Args:
		category_id: The id of the category to update
		name: Name for the category
		description: Description for the category
	
	Returns:
		Nothing
	"""
	
	category = readCategory(category_id)
	category.name = name
	category.description = description
	session.add(category)
	session.commit()

# Update an item in the database.
def updateItem(item_id, name, description):
	"""
	Update an item in the database.
	
	Args:
		item_id: The id of the item to update
		name: Name for the item
		description: Description for the item
	
	Returns:
		Nothing
	"""
	
	item = readItem(item_id)
	item.name = name
	item.description = description
	session.add(item)
	session.commit()

# Delete an item from the database.
def deleteItem(item_id):
	"""
	
	
	Args:
		
	
	Returns:
		
	"""
	
	item = readItem(item_id)
	session.delete(item)
	session.commit()
	
