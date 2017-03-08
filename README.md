# bball-stats

grab some stats on bball games, and experiment with ways to rank teams

#Pre-reqs
- sqlite3
 - NOTE: database refresh script assumes a linux (bash) environment, but bash shouldn't be required
- python 2
- bs4 (beautiful soup)

# How to use
- Setup (or just clear/refresh) database
 - `./dbRefresh.sh`
- Get game and team info and insert into DB
 - `python scrape.py`
- Run stats type things?
 - `python stats.py`

# Files
/

scrape.py
- grab schools and their games and put them into sqlite database

stats.py
- code that processes data already in database to calculate rankings and stats type things

stats_page.html
- contains contents of page with links to all teams

/db/

stats.sql
- DB schema

stats.sqlite
- SQLite DB file
- Contains game info for all teams (includes yet-to-be-played games if they are scheduled - scores are blank)

/test_files/
- just some files that contained output of various runs...
