# bball-stats

grab some stats on bball games, and experiment with ways to rank teams

#Pre-reqs
- sqlite3
 - NOTE: database refresh script assumes a linux (bash) environment, but bash shouldn't be required
- python3
- bs4 (beautiful soup)

# How to use
- Setup (or just clear/refresh) database
 - `./dbRefresh.sh`
- Run
 - `python scrape.py`

# Files
/

scrape.py
- code to grab schools and their games and put them into sqlite database
calculate.py
- theoretical file with code to calculate ratings for teams
stats_page.html
- contains contents of page with links to all teams

/db/

stats.sql
- DB schema
stats.sqlite
- SQLite DB file

/test_files/
- just some files that contained output of various runs...
