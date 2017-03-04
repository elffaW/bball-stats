import urllib2
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('db/stats.sqlite')
cursor = conn.cursor()

# stats = "http://www.sports-reference.com/cbb/seasons/2017-school-stats.html"
stats = "file:///home/ubuntu/workspace/stats_page.html"

page = urllib2.urlopen(stats)

soup = BeautifulSoup(page, "html5lib")

stats_table = soup.find(id="basic_school_stats")

links = stats_table.find_all('a')

for l in links:
	rating = 0
	school_name = l.string
	
	#insert teams into DB (IntegrityError is thrown when UNIQUE constraint is violated - we'll just swallow it)
	try:
		cursor.execute("INSERT INTO team (name,rating) VALUES (?,?)", (school_name,rating))
	except sqlite3.IntegrityError as ie:
		pass

	school_id = cursor.lastrowid
	
	if school_id is None:
		cursor.execute("SELECT id FROM team WHERE name=?", (school_name,))
		school_id = cursor.fetchone()[0]
		
	#link in the table is to stats page, but schedule page just adds "-schedule" to the URL before .html
	schedule_link = 'http://www.sports-reference.com' + l['href'][:-5] + '-schedule.html'
	
	schedule_page = urllib2.urlopen(schedule_link)
	soup_sched = BeautifulSoup(schedule_page, "html5lib")

	sched_table = soup_sched.find(id="schedule")

	rows = sched_table.find_all('tr')

	for r in rows:
		cols = r.find_all('td')
		relevant_data = unicode(school_name)
		
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
				cursor.execute("INSERT INTO team (name,rating) VALUES (?,?)", (opponent_name,rating))
				opponent_id = cursor.lastrowid
				
			if date_time is not None and school_id is not None and opponent_id is not None:
				try:
					cursor.execute("INSERT INTO game (game_date,school_id,opponent_id,pts_scored,pts_allowed) VALUES (?,?,?,?,?)",(full_date,school_id,opponent_id,pts_scored,pts_allowed))
				except sqlite3.InterfaceError as e:
					print e.args

		conn.commit()

conn.commit()

# print links