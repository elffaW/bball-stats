CREATE TABLE team(
	id	INTEGER	PRIMARY KEY	NOT NULL,
	name	TEXT	NOT NULL,
	rating	REAL
);

CREATE TABLE game(
	id	INTEGER	PRIMARY KEY	NOT NULL,
	date	DATETIME	NOT NULL,
	school_id	INT	NOT NULL,
	opponent_id	INT	NOT NULL,
	pts_scored	INT,
	pts_allowed	INT,
	home_game	BOOLEAN
);