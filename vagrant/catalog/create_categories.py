from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from catalog_db_setup import Category, Base, Item, User
from catalog_db_util import createUser, createCategory, readUserID

engine = create_engine('sqlite:///catalogitemswithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

categories = [ 
	{ "name": "Appliances", "description": "New and used appliances for sale." },
	{ "name": "Automobiles", "description": "New and used automobiles for sale." },
	{ "name": "Bicycles", "description": "New and used bicycles for sale." },
	{ "name": "Boats", "description": "New and used boats for sale." },
	{ "name": "Books", "description": "New and used books for sale." },
	{ "name": "Clothing", "description": "New and used clothing for sale." },
	{ "name": "Computers", "description": "New and used computers for sale." },
	{ "name": "Furniture", "description": "New and used furniture for sale." },
	{ "name": "Household Items", "description": "New and used household items for sale." },
	{ "name": "Jewelry", "description": "New and used jewelry for sale." },
	{ "name": "Photography", "description": "New and used cameras and equipment for sale." },
	{ "name": "Motorcycles", "description": "New and used motorcycles for sale." },
	{ "name": "Musical Instruments", "description": "New and used musical instruments for sale." },
	{ "name": "Sporting Goods", "description": "New and used sporting goods for sale." },
	]

	
#
#  Add a user who will own the initial categories
#
user_id = readUserID("catalog@app")
if not user_id:
	createUser("Catalog App", "catalog@app", "")
	user_id = readUserID("catalog@app")

#
# Add some categories
#
numCategories = 0
for category in categories:
	createCategory(category['name'], category['description'], user_id) 
	numCategories += 1


print "Done. %s categories added." % numCategories
