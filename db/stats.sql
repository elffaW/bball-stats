CREATE TABLE team(
	id	INTEGER	PRIMARY KEY	NOT NULL,
	name	TEXT	UNIQUE NOT NULL,
	rating	REAL
);

CREATE TABLE game(
	id	INTEGER	PRIMARY KEY	NOT NULL,
	game_date	DATETIME	NOT NULL,
	school_id	INT 	NOT NULL,
	opponent_id	INT		NOT NULL,
	pts_scored	INT,
	pts_allowed	INT
);