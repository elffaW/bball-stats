import urllib2
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('db/stats.sqlite')
db = conn.cursor()

# stats = "http://www.sports-reference.com/cbb/seasons/2017-school-stats.html"
stats = "file:///mnt/e/Coding/Python/bball-stats/stats_page.html"

page = urllib2.urlopen(stats)

soup = BeautifulSoup(page)

stats_table = soup.find(id="basic_school_stats")

links = stats_table.find_all('a')

for l in links:
	rating = 0
	school_name = l.string
	schedule_link = 'http://www.sports-reference.com' + l['href'][:-5] + '-schedule.html'
	#TODO save school_name and schedule_link
	db.execute("INSERT INTO team (name,rating) VALUES (?,?)", (school_name,rating))
	
	schedule_page = urllib2.urlopen(schedule_link)
	soup_sched = BeautifulSoup(schedule_page)

	sched_table = soup_sched.find(id="schedule")

	rows = sched_table.find_all('tr')

	# print 'school_name' + ' | ' + 'date_game' + ' | ' + 'opp_name' + ' | ' + 'game_result' + ' | ' + 'pts' + ' | ' + 'opp_pts' + ' | ' + 'game_location'
	for r in rows:
		cols = r.find_all('td')
		relevant_data = unicode(school_name)
		
		for c in cols:
			if c['data-stat'] == "date_game" or c['data-stat'] == "opp_name" or c['data-stat'] == "game_result" or c['data-stat'] == "pts" or c['data-stat'] == "opp_pts" or c['data-stat'] == "game_location":
				str = '' if (unicode(c.string) == 'None') else unicode(c.string)
				relevant_data = relevant_data + ' | ' + str



		print relevant_data
		
	break



# print links