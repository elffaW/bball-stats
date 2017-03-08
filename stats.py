from __future__ import division
import sqlite3

conn = sqlite3.connect('db/stats.sqlite')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

def getTeamId( team_name ):
	#get ID of team for link to games table
	cursor.execute("SELECT id FROM team WHERE name=?", (team_name,))
	school_id = cursor.fetchone()[0]
	return school_id

#RPI = 0.25 * team's winning percentage + 0.5 * OWP + 0.25 * OOWP
def calculateRPI( team_name ):
	print 'Calculating RPI for ' + team_name
	school_id = getTeamId(team_name)
	#get games for team
	cursor.execute("SELECT * FROM game WHERE school_id=?", (school_id,))
	games = cursor.fetchall()

	#WP = wins / num_games
	wp = calculateWP(school_id)

	#OWP = sum(all OWP) / num_games
	owp = calculateOWP(school_id)


	#OOWP
	#	for each opp
	#		calculate OWP
	#		add to cumulative_oowp
	#	OOWP = cumulative_oowp / num_opps
	opponents = []

	for game in games:
		opponents.append(game['opponent_id'])

	owp = cumulative_owp / num_games
	
	

	num_opps = len(opponents)
	cumulative_oowp = 0

	for opp in opponents:
		

	print 'wp = ' + str(wp)
	print 'owp = ' + str(owp)
	return 0.25 * wp + 0.5 * owp

def calculateWP( team_id ):
	#get games for team
	cursor.execute("SELECT * FROM game WHERE school_id=?", (team_id,))
	games = cursor.fetchall()

	num_games = len(games)
	num_wins = 0

	for game in games:
		if game['pts_scored'] > game['pts_allowed']:
			num_wins += 1

	return num_wins / num_games

def calculateOWP( team_id ):
	#get games for team
	cursor.execute("SELECT * FROM game WHERE school_id=?", (team_id,))
	games = cursor.fetchall()

	#OWP = sum(all OWP) / num_games
	num_games = len(games)
	cumulative_owp = 0
	owp = 0

	for game in games:
		cumulative_owp += calculateWP(game['opponent_id'])

	owp = cumulative_owp / num_games

	return owp

wp = calculateWP(getTeamId("Louisville"))
rpi = calculateRPI("Louisville")

print 'WP:\t' + str(wp)
print 'RPI:\t' + str(rpi)

conn.commit()
cursor.close()