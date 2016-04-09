# Catalog App

This web application was created for the third project in the 
[Udacity] (http://www.udacity.com) Full Stack nanodegree program. The project
implements a catalog application which allows users to create items to
be stored in a catalog.

## Features
The catalog app has the following features:
* Catalog persistence. Users can create, read, update and delete items in 
the catalog.
* User authentication and authorization. Only registered users can add
items to the catalog and items can only be edited and deleted by the item's
creator.
* JSON endpoints for items and categories.

## Project Files

The project consists of the following types of files:

* Python Files - All of the python files are located in the main project
directory. To execute them you can type `python file` at the command
line.
  * catalog_db_setup.py - This file defines the database structure and sets
up the database.
  * catalog_db_util.py - This file contains functions to read from and write to
the database. All of the CRUD functinality is implemented in this file.
  * catalog_app.py - This file implements the web application.
  * create_categories.py - This file creates some starter categories for the
catalog. 
* HTML and CSS Files - All of the .html files are located in the templates
directory. The .css files are located in the static directory.

## Installation

To install the catalog app, download all of the files in the project. Then 
execute the following commands on your command line:

1. `python catalog_db_setup.py`

   This command will create the database file called catalogitemswithusers.db.

2. `python create_categories.py` **_optional_**

   This command will initialize the database with some categories.
   
3. Obtain client_secrets.json file. This file is obtained by registering
the application at https://console.developers.google.com. The file will contains
the client ID and the secret key. Replace the client ID in the login.html file
with your client ID.

4. `python catalog_app.py`

   This command will start the web application. The application will be running
on the localhost at port 5000. To use the catalog app, go to the following 
URL: http://localhost:5000/catalog

## Versions

### Python
This web application was written and tested using python version 2.7.6. Python can be 
obtained by going to [Python.org](https://www.python.org/downloads) and 
selecting the appropriate version for your operating system.
### Flask
This web application uses the Flask framework version 0.9. 

## Getting Started

