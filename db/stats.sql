CREATE TABLE team(
	id	INTEGER	PRIMARY KEY	NOT NULL,
	name	TEXT	UNIQUE NOT NULL,
	schedule_link	TEXT,
	wins INTEGER,
	losses INTEGER,
	srs REAL,
	sos REAL,
	pts_scored INTEGER,
	pts_allowed INTEGER,
	fg INTEGER,
	fga INTEGER,
	threes INTEGER,
	threes_att INTEGER,
	ft INTEGER,
	fta INTEGER,
	orb INTEGER,
	trb INTEGER,
	ast INTEGER,
	stl INTEGER,
	blk INTEGER,
	tov INTEGER,
	pf INTEGER,
	rpi	REAL,
	bpi REAL,
	kenpom_rank REAL
);

CREATE TABLE game(
	id	INTEGER	PRIMARY KEY	NOT NULL,
	game_date	DATETIME	NOT NULL,
	school_id	INTEGER 	NOT NULL,
	opponent_id	INTEGER		NOT NULL,
	pts_scored	INTEGER,
	pts_allowed	INTEGER
);