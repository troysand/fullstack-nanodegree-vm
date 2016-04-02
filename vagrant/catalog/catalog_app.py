from flask import Flask, render_template, request, redirect, jsonify, url_for
from catalog_db_setup import Category, Item
from catalog_db_util import readItem, readItems, readAllItems, readCategory, readCategories
from catalog_db_util import createCategory, createItem, updateItem, updateCategory, deleteItem

app = Flask(__name__)

# Show all categories
@app.route('/')
@app.route('/catalog/')
def showCategories():
	#return "This page will show all the categories (plus latest items)"
	categories = readCategories()
	return render_template('catalog.html', categories=categories)

# Create a new category
@app.route('/catalog/category/newcategory/', methods=['GET', 'POST'])
def newCategory():
	if request.method == 'POST':
		createCategory(request.form['name'], request.form['description'])
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
	return render_template('show_category.html', items=items, category=category)

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
	category = readCategory(item.category_id)
	return render_template('show_item.html', item=item, category=category)

# Create a new item
@app.route('/catalog/category/<int:category_id>/newitem/', 
           methods=['GET', 'POST'])
def newItem(category_id):
	category = readCategory(category_id)
	if request.method == 'POST':
		createItem(request.form['name'], request.form['description'], 
			category_id)
		return redirect(url_for('showCategory', category_id=category_id))
	else:
		return render_template('new_item.html', category=category)

# Edit an item
@app.route('/catalog/item/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(item_id):
	item = readItem(item_id)
	category = readCategory(item.category_id)
	if request.method == 'POST':
		updateItem(item_id, request.form['name'], request.form['description'])
		return redirect(url_for('showItem', item_id=item_id))
	else:
		return render_template('edit_item.html', item=item, category=category)

# Edit a category
@app.route('/catalog/category/<int:category_id>/edit/', methods=['GET','POST'])
def editCategory(category_id):
	category = readCategory(category_id)
	if request.method == 'POST':
		updateCategory(category_id, request.form['name'], request.form['description'])
		return redirect(url_for('showCategory', category_id=category_id))
	else:
		return render_template('edit_category.html', category = category)

# Delete an item
@app.route('/catalog/item/<int:item_id>/delete/', methods=['GET', 'POST'])
def removeItem(item_id):
	item = readItem(item_id)
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
	app.debug = True
	app.run(host='0.0.0.0', port=5000)

	