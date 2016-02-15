-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- First get rid of the database if it already exists.
DROP DATABASE IF EXISTS tournament;

-- Create the tournament database.
CREATE DATABASE tournament;

-- Connect to the newly created database before creating the 
-- tables and functions.
\connect tournament;

-- Create the Players table. This table stores information
-- about each player.
CREATE TABLE Players (
	player_id	serial PRIMARY KEY,
	name		varchar(80),
	wins		smallint DEFAULT 0,
	matches		smallint DEFAULT 0
);

-- Create the Matches table. This table stores information about
-- each match.
CREATE TABLE Matches (
	match_id	serial PRIMARY KEY,
	winner_id	integer REFERENCES Players,
	loser_id	integer REFERENCES Players
);

-- Create the report_match_result() function. This function adds the
-- match to the Matches table and also updates the number of wins
-- and total matches for the winner and updates the total matches
-- for the loser.
CREATE OR REPLACE FUNCTION report_match_result(winner integer, loser integer) 
	RETURNS void AS $$
BEGIN
	INSERT INTO Matches (winner_id, loser_id) VALUES (winner, loser);
	UPDATE Players SET wins = wins + 1, matches = matches + 1
		WHERE player_id = winner;
	UPDATE Players SET matches = matches + 1
		WHERE player_id = loser;
END
$$ LANGUAGE plpgsql;

-- Create the delete_all_players() function. This function deletes all 
-- players from the Players table.
CREATE OR REPLACE FUNCTION delete_all_players()
	RETURNS void AS $$
BEGIN
	DELETE FROM Players;
END
$$ LANGUAGE plpgsql;

-- Create the delete_all_matches() function. This function deletes all
-- matches from the Matches table. Additionally, it resets the wins and
-- total matches for each player back to zero.
CREATE OR REPLACE FUNCTION delete_all_matches()
	RETURNS void AS $$
BEGIN
	DELETE FROM Matches;
	UPDATE Players SET wins = 0, matches = 0;
END
$$ LANGUAGE plpgsql;

