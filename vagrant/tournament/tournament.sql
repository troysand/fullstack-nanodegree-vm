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
	name		varchar(80)
);

-- Create the Matches table. This table stores information about
-- each match.
CREATE TABLE Matches (
	match_id	serial PRIMARY KEY,
	winner_id	integer REFERENCES Players,
	loser_id	integer REFERENCES Players
);

-- Create the NumPlayers view, which will be used to get the number
-- of players currently registered.
CREATE VIEW NumPlayers AS
	SELECT COUNT(*)
	FROM Players;

-- Create the report_match_result() function. This function adds the
-- match to the Matches table.
CREATE OR REPLACE FUNCTION report_match_result(winner integer, loser integer) 
	RETURNS void AS $$
BEGIN
	INSERT INTO Matches (winner_id, loser_id) VALUES (winner, loser);
END;
$$ LANGUAGE plpgsql;

-- Create the delete_all_players() function. This function deletes all 
-- players from the Players table.
CREATE OR REPLACE FUNCTION delete_all_players()
	RETURNS void AS $$
BEGIN
	DELETE FROM Players;
END;
$$ LANGUAGE plpgsql;

-- Create the delete_all_matches() function. This function deletes all
-- matches from the Matches table. 
CREATE OR REPLACE FUNCTION delete_all_matches()
	RETURNS void AS $$
BEGIN
	DELETE FROM Matches;
END;
$$ LANGUAGE plpgsql;

-- Create the get_player_standings() function. This function gets the 
-- player standings returned in a table of the format:
--     player_id integer - the player id
--     name varchar(80)  - the player name
--     wins integer      - the number of wins for the player
--     matches integer   - the total number of matches for the player
--
-- The rows are sorted by wins from high to low.
CREATE OR REPLACE FUNCTION get_player_standings()
	RETURNS TABLE(player_id integer, name varchar(80), 
                  wins bigint, matches bigint) AS $$
BEGIN
	-- This query gets the number of wins and matches for each player.
	-- Wins are calculated by counting the number of wins in the Matches table
	-- and total matches are calculated by getting the count of wins and losses
	-- combined.
	RETURN QUERY 
	SELECT Players.player_id AS player_id, Players.name AS name, 
		(SELECT COUNT(*) FROM Matches 
			WHERE Players.player_id = Matches.winner_id )
		AS wins,
		(SELECT COUNT(*) FROM Matches 
			WHERE Players.player_id = Matches.winner_id 
			OR Players.player_id = Matches.loser_id)
		AS matches
	FROM Players
	ORDER BY wins;
END;
$$ LANGUAGE plpgsql;
