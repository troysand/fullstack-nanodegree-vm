
# Tournament Results

This project implements a database schema and code for a Swiss pairings
style tournament. The tournament results are stored in a PostgreSQL database
and the pairings for the next round are determined by the previous results.

## Project Files

The project consists of 4 files:
* README.md - This file which explains how to install and run the project.
* tournament.sql - An SQL script which creates the database, tables and 
functions necessary for the project.
* tournament.py - A Python file which contains the code required to register 
players, store the results, get the current standings, and get the next round 
of pairings.
* tournament_test.py - A Python file which contains the test cases for the
functions implemented in tournament.py.

## Installation

To create the database, run **psql** at the command line to start the PostgreSQL
client. Within **psql**, type _\i tournament.sql_ to import the SQL script and
create the database.

Once the database has been created, type _\q_ to exit **psql**. Then run 
**python tournament_test.py** at the command line to run the unit tests. If
tournament_test.py runs without any errors then the database has been installed
correctly.

## Versions

### Python
This program was written and tested using python version 2.7.6. Python can be 
obtained by going to [Python.org][https://www.python.org/downloads] and 
selecting the appropriate version for your operating system.

### PostgreSQL
This program was written and tested using PostgreSQL version 9.3.11. PostgreSQL
can be obtained by going to [postgresql.org][http://www.postresql.org/download]
and selecting the appropriate version for your operating system.