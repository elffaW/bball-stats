import urllib2
from bs4 import BeautifulSoup
import sqlite3

#just change 'season' variable if you want to get a different season's stats 
#	NOTE: it'll put it into a diff DB which needs to exist already (so check out the dbRefresh.sh script)
season = 2017
print 'Getting team and game info for ' + str(season) + ' season'
conn = sqlite3.connect('db/stats_' + str(season) + '.sqlite')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

stats = "http://www.sports-reference.com/cbb/seasons/" + str(season) + "-school-stats.html"

page = urllib2.urlopen(stats)

soup = BeautifulSoup(page, "html5lib")

stats_table = soup.find(id="basic_school_stats")
stats_table_body = stats_table.find('tbody')

teams = stats_table_body.find_all('tr')

num_teams = str(len(teams))
i = 1;
for t in teams:
	if t.has_attr('class'):
		continue
	school_id = None
	school_name = ''
	schedule_link = ''
	wins = 0
	losses = 0
	srs = 0
	sos = 0
	pts_scored = 0
	pts_allowed = 0
	fg = 0
	fga = 0
	threes = 0
	threes_att = 0
	ft = 0
	fta = 0
	orb = 0
	trb = 0
	ast = 0
	stl = 0
	blk = 0
	tov = 0
	pf = 0
	rpi = 0
	bpi = 0
	kenpom_rank = 0

	team_cols = t.find_all('td')
	for tc in team_cols:
		if tc['data-stat'] == 'school_name':
			temp = tc.a
			#link in the table is to stats page, but schedule page just adds "-schedule" to the URL before .html
			school_sublink = temp['href'][:-5]	#remove .html
			#we can get the schedule year from school_sublink[:-4] (if we want it)
			
			schedule_link = 'http://www.sports-reference.com' + school_sublink + '-schedule.html'
			school_name = temp.string
		elif tc['data-stat'] == 'wins':
			wins = tc.string
		elif tc['data-stat'] == 'losses':
			losses = tc.string
		elif tc['data-stat'] == 'srs':
			srs = tc.string
		elif tc['data-stat'] == 'sos':
			sos = tc.string
		elif tc['data-stat'] == 'pts':
			pts_scored = tc.string
		elif tc['data-stat'] == 'opp_pts':
			pts_allowed = tc.string
		elif tc['data-stat'] == 'fg':
			fg = tc.string
		elif tc['data-stat'] == 'fga':
			fga = tc.string
		elif tc['data-stat'] == 'fg3':
			threes = tc.string
		elif tc['data-stat'] == 'fg3a':
			threes_att = tc.string
		elif tc['data-stat'] == 'ft':
			ft = tc.string
		elif tc['data-stat'] == 'fta':
			fta = tc.string
		elif tc['data-stat'] == 'orb':
			orb = tc.string
		elif tc['data-stat'] == 'trb':
			trb = tc.string
		elif tc['data-stat'] == 'ast':
			ast = tc.string
		elif tc['data-stat'] == 'stl':
			stl = tc.string
		elif tc['data-stat'] == 'blk':
			blk = tc.string
		elif tc['data-stat'] == 'tov':
			tov = tc.string
		elif tc['data-stat'] == 'pf':
			pf = tc.string
	
	
	#insert teams into DB (IntegrityError is thrown when UNIQUE constraint is violated - we'll just swallow it)
	try:
		cursor.execute("INSERT INTO team (name, schedule_link, wins, losses, srs, sos, pts_scored, pts_allowed, fg, fga, threes, threes_att, ft, fta, orb, trb, ast, stl, blk, tov, pf, rpi, bpi, kenpom_rank) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (school_name, schedule_link, wins, losses, srs, sos, pts_scored, pts_allowed, fg, fga, threes, threes_att, ft, fta, orb, trb, ast, stl, blk, tov, pf, rpi, bpi, kenpom_rank))
	except sqlite3.IntegrityError as ie:
		cursor.execute("SELECT id FROM team WHERE name=?", (school_name,))
		school_id = cursor.fetchone()[0]
		pass

	if school_id is None:
		school_id = cursor.lastrowid
		
	print 'Processed team ' + str(i) + ' of ' + str(num_teams) + ' [' + str(school_id) + ', ' + str(school_name) + ']'
	i += 1

#commit teams, then get game info for each team
conn.commit()

#for each team
j = 1
cursor.execute("SELECT id, name, schedule_link FROM team")
all_teams = cursor.fetchall()
num_teams = len(all_teams)
for row in all_teams:
	school_id = row['id']
	school_name = row['name']

	print 'Processing team ' + str(j) + ' (' + school_name + ') of ' + str(num_teams) + '\'s schedule'
	j += 1

	schedule_page = urllib2.urlopen(row['schedule_link'])
	soup_sched = BeautifulSoup(schedule_page, "html5lib")

	sched_table = soup_sched.find(id="schedule")

	rows = sched_table.find_all('tr')

	print '\tProcessing ' + str(len(rows)) + ' games'

	for r in rows:
		cols = r.find_all('td')
		
		game_date = ''
		game_time = ''
		opponent_name = ''
		pts_scored = -1
		pts_allowed = -1

		for c in cols:
			if c['data-stat'] == "date_game":
				game_date = c.string
			elif c['data-stat'] == "time_game":
				game_time = c.string
			elif c['data-stat'] == "opp_name":
				temp = c.a
				if c.a is not None:
					opponent_name = temp.string
				else :
					opponent_name = c.string
			elif c['data-stat'] == "pts":
				pts_scored = c.string
			elif c['data-stat'] == "opp_pts":
				pts_allowed = c.string

		if game_date is not '' and school_id is not None and opponent_name is not '':
			game_time = game_time[:-4] + ' EST'
			date_time = game_date + ' ' + game_time
			split_time = date_time.split( )
			months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

			month = months.index(split_time[1]) + 1
			month_str = str(month) if month > 9 else '0' + str(month)

			day = str(split_time[2])
			day = day[:-1]

			year = str(split_time[3])

			full_date = year + '-' + month_str + '-' + day

			cursor.execute("SELECT id FROM team WHERE name=?", (opponent_name,))
			opponent_id = cursor.fetchone()
			if opponent_id is not None:
				opponent_id = opponent_id[0]

			if opponent_id is None and opponent_name is not None:
				cursor.execute("INSERT INTO team (name,rpi) VALUES (?,?)", (opponent_name,rpi))
				opponent_id = cursor.lastrowid
				
			if date_time is not None and school_id is not None and opponent_id is not None:
				try:
					print '\tInserting new game: ' + str(game_date) + ' [ ' + str(school_id) + ', ' + school_name + ' ][ ' + str(opponent_id) + ', ' + opponent_name + ' ]'
					cursor.execute("INSERT INTO game (game_date,school_id,opponent_id,pts_scored,pts_allowed) VALUES (?,?,?,?,?)",(full_date,school_id,opponent_id,pts_scored,pts_allowed))
				except sqlite3.InterfaceError as e:
					print e.args

conn.commit()
cursor.close()