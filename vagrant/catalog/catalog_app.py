import random
import string
import httplib2
import json
import requests
from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import flash, make_response
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from catalog_db_setup import Category, Item
from catalog_db_util import readItem, readItems, readAllItems, readCategory
from catalog_db_util import createCategory, createItem, updateItem
from catalog_db_util import readCategories, updateCategory, deleteItem
from catalog_db_util import createUser, readUserID, readUserInfo
from catalog_db_util import readLatestItems

app = Flask(__name__)

CLIENT_ID = json.loads(
	open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"

@app.route('/login')
def showLogin():
	# Set the session state id
	state = ''.join(random.choice(string.ascii_uppercase + string.digits)
		for x in xrange(32))
	login_session['state'] = state
	#return "The current session state is %s" % login_session['state']
	return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	# Obtain authorization code
	code = request.data
	try:
		# Upgrade the authorization code into a credentials object
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
		
	#Check that the access token is valid.
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])
	# If there was an error in the access token info, abort.
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'

	# Verify that the access token is used for the intended user.
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(
			json.dumps("Token's user ID doesn't match given user ID."), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify that the access token is valid for this app.
	if result['issued_to'] != CLIENT_ID:
		response = make_response(
			json.dumps("Token's client ID does not match app's."), 401)
		print "Token's client ID does not match app's."
		response.headers['Content-Type'] = 'application/json'
		return response

	stored_credentials = login_session.get('credentials')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_credentials is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'),
                                 200)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Store the access token in the session for later use.
	login_session['access_token'] = credentials.access_token
	login_session['gplus_id'] = gplus_id

	# Get user info
	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, params=params)

	data = answer.json()

	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']
	login_session['provider'] = 'google'
	
	# Check to see if the user exists in the database
	user_id = readUserID(data['email'])
	if not user_id:
		user_id = createUser(data['name'], data['email'], data['picture'])
	login_session['user_id'] = user_id

	output = ''
	output += '<h1>Welcome, '
	output += login_session['username']
	output += '!</h1>'
	output += '<img src="'
	output += login_session['picture']
	output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
	flash("you are now logged in as %s" % login_session['username'])
	print "done!"
	return output

# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
	access_token = login_session['access_token']
	print 'In gdisconnect access token is %s', access_token
	print 'User name is: ' 
	print login_session['username']
	if access_token is None:
		print 'Access Token is None'
		response = make_response(json.dumps('Current user not connected.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]
	print 'result is '
	print result
	if result['status'] == '200':
		del login_session['access_token'] 
		del login_session['gplus_id']
		del login_session['username']
		del login_session['email']
		del login_session['picture']
		response = make_response(json.dumps('Successfully disconnected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response
	else:
		response = make_response(json.dumps('Failed to revoke token for given user.', 400))
		response.headers['Content-Type'] = 'application/json'
		return response

@app.route('/disconnect')
def disconnect():
	if login_session['provider'] == 'google':
		return gdisconnect()

# Show all categories
@app.route('/')
@app.route('/catalog/')
def showCategories():
	categories = readCategories()
	latestItems = readLatestItems(10)
	if 'username' not in login_session:
		return render_template('public_catalog.html', categories=categories,
			latestItems=latestItems)
	else:
		return render_template('catalog.html', categories=categories,
			latestItems=latestItems)

# Create a new category
@app.route('/catalog/category/newcategory/', methods=['GET', 'POST'])
def newCategory():
	if 'username' not in login_session:
		return redirect('/login')
	if request.method == 'POST':
		createCategory(request.form['name'], request.form['description'],
			login_session['user_id'])
		return redirect(url_for('showCategories'))
	else:
		return render_template('new_category.html')
	
# Show all the items in a category, given a category id
@app.route('/catalog/category/<int:category_id>/')
def showCategory(category_id):
	category = readCategory(category_id)
	if category == None:
		return showError("There is no category with id=%s" % category_id)
	items = readItems(category_id)
	if 'username' not in login_session:
		return render_template('public_show_category.html', items = items, 
			category=category)
	else:
		return render_template('show_category.html', items=items, 
			category=category)

# Show all categories
@app.route('/catalog/category/all/')
def showAllCategories():
	categories = readCategories()
	return render_template('show_all_categories.html', categories=categories)

# Show all items
@app.route('/catalog/item/all/')
def showAllItems():
	items = readAllItems()
	return render_template('show_all_items.html', items=items)

# Show an item and its description
@app.route('/catalog/item/<int:item_id>/')
def showItem(item_id):
	item = readItem(item_id)
	if item == None:
		return showError("There is no item with id=%s" % item_id)
	creator = readUserInfo(item.user_id)
	category = readCategory(item.category_id)
	if 'username' not in login_session or creator.id != login_session['user_id']:
		return render_template('public_show_item.html', item=item, 
			category=category, creator=creator)
	else:
		return render_template('show_item.html', item=item, category=category,
			creator=creator)

# Create a new item
@app.route('/catalog/category/<int:category_id>/newitem/', 
           methods=['GET', 'POST'])
def newItem(category_id):
	if 'username' not in login_session:
		return redirect('/login')
	user_id = login_session['user_id']
	category = readCategory(category_id)
	if request.method == 'POST':
		createItem(request.form['name'], request.form['description'], 
			category_id, user_id)
		return redirect(url_for('showCategory', category_id=category_id))
	else:
		return render_template('new_item.html', category=category)

# Edit an item
@app.route('/catalog/item/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(item_id):
	if 'username' not in login_session:
		return redirect('/login')
	item = readItem(item_id)
	if login_session['user_id'] != item.user_id:
		return "<script>function myFunction() {alert('You are not authorized to edit this item.');}</script><body onload='myFunction()''>"
	category = readCategory(item.category_id)
	if request.method == 'POST':
		updateItem(item_id, request.form['name'], request.form['description'])
		return redirect(url_for('showItem', item_id=item_id))
	else:
		return render_template('edit_item.html', item=item, category=category)

# Edit a category
@app.route('/catalog/category/<int:category_id>/edit/', methods=['GET','POST'])
def editCategory(category_id):
	if 'username' not in login_session:
		return redirect('/login')
	category = readCategory(category_id)
	if login_session['user_id'] != category.user_id:
		return "<script>function myFunction() {alert('You are not authorized to edit this category.');}</script><body onload='myFunction()''>"
	if request.method == 'POST':
		updateCategory(category_id, request.form['name'], request.form['description'])
		return redirect(url_for('showCategory', category_id=category_id))
	else:
		return render_template('edit_category.html', category = category)

# Delete an item
@app.route('/catalog/item/<int:item_id>/delete/', methods=['GET', 'POST'])
def removeItem(item_id):
	if 'username' not in login_session:
		return redirect('/login')
	item = readItem(item_id)
	if login_session['user_id'] != item.user_id:
		return "<script>function myFunction() {alert('You are not authorized to delete this item.');}</script><body onload='myFunction()''>"
	if request.method == 'POST':
		deleteItem(item_id)
		return redirect(url_for('showCategory', category_id=item.category_id))
	else:
		return render_template('delete_item.html', item=item)

@app.route('/catalog/category/JSON/')
def showCategoriesJSON():
	categories = readCategories()
	return jsonify(categories=[c.serialize for c in categories])

@app.route('/catalog/item/all/JSON/')
def showAllItemsJSON():
	items = readAllItems()
	return jsonify(items=[i.serialize for i in items])

# 
@app.route('/catalog/category/<int:category_id>/JSON/')
def showCategoryJSON(category_id):
	category = readCategory(category_id)
	if category == None:
		return showError("There is no category with id=%s" % category_id)
	items = readItems(category_id)
	return jsonify(items=[i.serialize for i in items])

# 
@app.route('/catalog/item/<int:item_id>/JSON/')
def showItemJSON(item_id):
	item = readItem(item_id)
	if item == None:
		return showError("There is no item with id=%s" % item_id)
	return jsonify(item=item.serialize)

def showError(message):
	return render_template('show_error.html', message=message)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)

	