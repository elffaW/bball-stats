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
	cursor.execute("SELECT * FROM game WHERE school_id=? AND pts_scored > 0", (school_id,))
	games = cursor.fetchall()

	#WP = wins / num_games
	wp = calculateWP(school_id, None)

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


	num_opps = len(opponents)
	cumulative_oowp = 0

	for opp in opponents:
		cumulative_oowp += calculateOWP(opp)

	oowp = cumulative_oowp / num_opps

	rpi = (0.25 * wp) + (0.5 * owp) + (0.25 * oowp)

	print 'wp =\t' + str(wp)
	print 'owp =\t' + str(owp)
	print 'oowp =\t' + str(oowp)
	
	return rpi


# takes team_id to calculate winning percentage of, and optionally takes a second id representing a school to remove from WP calc (for OWP)
def calculateWP( team_id, opp_id ):
	#get games for team
	if opp_id is not None:
		cursor.execute("SELECT * FROM game WHERE school_id=? AND pts_scored > 0 AND opponent_id != ?", (team_id,opp_id))
	else:
		cursor.execute("SELECT * FROM game WHERE school_id=? AND pts_scored > 0", (team_id,))
	games = cursor.fetchall()

	num_games = len(games)
	num_losses = 0.0
	num_wins = 0.0

	if(num_games < 1):
		return 0

	for game in games:
		if game['pts_scored'] > game['pts_allowed']:
			if opp_id is None:
				if game['game_location'] == 'home':
					num_wins += 0.6
				elif game['game_location'] == 'away':
					num_wins += 1.4
				else: #'neutral'
					num_wins += 1.0
			else: #WP only differentiates home/away/neutral for WP, not for OWP/OOWP
				num_wins += 1.0
		elif game['pts_scored'] < game['pts_allowed']:
			if opp_id is None:
				if game['game_location'] == 'home':
					num_losses += 1.4
				elif game['game_location'] == 'away':
					num_losses += 0.6
				else: #'neutral'
					num_losses += 1.0
			else: #WP only differentiates home/away/neutral for WP, not for OWP/OOWP
				num_losses += 1.0
	
	return num_wins / (num_wins + num_losses)


def calculateOWP( team_id ):
	#get games for team
	cursor.execute("SELECT * FROM game WHERE school_id=? AND pts_scored > 0", (team_id,))
	games = cursor.fetchall()

	#OWP = sum(all OWP) / num_games
	num_games = len(games)
	cumulative_owp = 0.0
	owp = 0.0

	if num_games < 1:
		return 0

	for game in games:
		if game['pts_scored'] is None:
			num_games -= 1
		else:
			cumulative_owp += calculateWP(game['opponent_id'], team_id)

	owp = cumulative_owp / num_games

	return owp

# wp = calculateWP(getTeamId("Louisville"))
# rpi = calculateRPI("Kansas")
print calculateRPI("Villanova")
print calculateRPI("Kansas")
print calculateRPI("Louisville")

# print 'RPI:\t' + str(rpi)

conn.commit()
cursor.close()