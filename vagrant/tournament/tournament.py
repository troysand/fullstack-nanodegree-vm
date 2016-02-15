#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")
	

def deleteMatches():
	"""Remove all the match records from the database."""
	db = connect()
	c = db.cursor()
	c.execute("SELECT delete_all_matches()")
	db.commit()
	db.close()

def deletePlayers():
	"""Remove all the player records from the database."""
	db = connect()
	c = db.cursor()
	c.execute("SELECT delete_all_players()")
	db.commit()
	db.close()


def countPlayers():
	"""Returns the number of players currently registered."""
	db = connect()
	c = db.cursor()
	query = "SELECT COUNT(*) FROM Players"
	c.execute(query)
	count = c.fetchone()[0]
	db.commit()
	db.close()
	return count

	
def registerPlayer(name):
	"""Adds a player to the tournament database.
  
     The database assigns a unique serial id number for the player.  (This
     should be handled by your SQL database schema, not in your Python code.)
  
     Args:
       name: the player's full name (need not be unique).
	"""
	db = connect()
	c = db.cursor()
	c.execute("INSERT INTO Players (name) VALUES (%s)", (name,))
	db.commit()
	db.close()
	
def playerStandings():
	"""Returns a list of the players and their win records, sorted by wins.

    # The first entry in the list should be the player in first place, or a player
    # tied for first place if there is currently a tie.

    # Returns:
      # A list of tuples, each of which contains (id, name, wins, matches):
        # id: the player's unique id (assigned by the database)
        # name: the player's full name (as registered)
        # wins: the number of matches the player has won
        # matches: the number of matches the player has played
	"""
	db = connect()
	c = db.cursor()
	c.execute("SELECT * FROM get_player_standings()")
	standings = []
	for row in c.fetchall():
		standings.append(row)
	
	db.close()
	return standings


def reportMatch(winner, loser):
	"""Records the outcome of a single match between two players.

    # Args:
      # winner:  the id number of the player who won
      # loser:  the id number of the player who lost
	"""
	db = connect()
	c = db.cursor()
	# Use the stored function report_match_result() to update the results.
	# This function will make sure that both tables get updated.
	c.execute("SELECT report_match_result(%s,%s)", (winner, loser))
	db.commit()
	db.close()
 

def swissPairings():
	"""Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
	"""
	standings = playerStandings()
	pairings = []
	player1 = []
	# Create the pairings for the tournament. Each pairing requires two
	# players, so save the first player's id and name and combine with the 
	# second player's info to create the pairing tuple.
	for player in standings:
		if player1:
			# now have two players, so create the pairing
			pairings.append((player1[0], player1[1], player[0], player[1]))
			player1 = []
		else:
			# first player in the pair, save the info and move on to
			# the next player.
			player1 = (player[0], player[1])
			
		
	return pairings
	
