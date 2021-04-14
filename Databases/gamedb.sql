DROP TABLE IF EXISTS Player;
DROP TABLE IF EXISTS Personality;
DROP TABLE IF EXISTS Demographic;
DROP TABLE IF EXISTS PlayerLocationInfo;
DROP TABLE IF EXISTS CommuteLocationInfo;
DROP TABLE IF EXISTS PlayMoment;
------
DROP TABLE IF EXISTS Game;
DROP TABLE IF EXISTS ChallengeType;
DROP TABLE IF EXISTS Challenge;
DROP TABLE IF EXISTS ChallengeInstance;
DROP TABLE IF EXISTS GameObjectType;
DROP TABLE IF EXISTS GameObject;
DROP TABLE IF EXISTS Currency;
DROP TABLE IF EXISTS GameObjectInstance;
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS Wallet;
DROP TABLE IF EXISTS PlayerConnection;
DROP TABLE IF EXISTS Faction;
DROP TABLE IF EXISTS FactionMember;



CREATE TABLE IF NOT EXISTS Game (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	name text NOT NULL,
	locationbased boolean NOT NULL,
	timebased boolean NOT NULL,
	socialexpansion boolean NOT NULL
);

CREATE TABLE IF NOT EXISTS Player(
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	gameID int,
	name text NOT NULL UNIQUE,
	FOREIGN KEY (gameID) REFERENCES Game (id)
);


CREATE TABLE IF NOT EXISTS PlayerLocationInfo(
	playerID int PRIMARY KEY,
	latitude int NOT NULL,
	longitude int NOT NULL,
	country text NOT NULL,
	FOREIGN KEY (playerID) REFERENCES Player (id)
);

CREATE TABLE IF NOT EXISTS CommuteLocationInfo(
	playerID int PRIMARY KEY,
	latitude int NOT NULL,
	longitude int NOT NULL,
	country text NOT NULL,
	FOREIGN KEY (playerID) REFERENCES Player (id)
);


CREATE TABLE IF NOT EXISTS Demographic(
	playerID int PRIMARY KEY,
	Age int NOT NULL,
	Gender text NOT NULL,
	SocioEconomicStatus int NOT NULL,
	FOREIGN KEY (playerID) REFERENCES Player (id)
);


CREATE TABLE IF NOT EXISTS Personality(
	playerID int PRIMARY KEY,
	Concentration int NOT NULL,
	Competitiveness int NOT NULL,
	PlayerSkills int NOT NULL,
	UserControl int NOT NULL,
	ClearGoals int NOT NULL,
	Feedback int NOT NULL,
	Immersion int NOT NULL,
	SocialInteraction int NOT NULL,
	Free2Play int NOT NULL,
	PersonalityType text NOT NULL,
	FOREIGN KEY (playerID) REFERENCES Player (id)
);


CREATE TABLE IF NOT EXISTS ChallengeType (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	gameID int,
	name text NOT NULL UNIQUE,
	temporary boolean NOT NULL,
	narrative boolean NOT NULL,
	locationRelevant boolean NOT NULL,
	uniqueChallenge boolean NOT NULL,
	FOREIGN KEY (gameID) REFERENCES Game (id)
);

CREATE TABLE IF NOT EXISTS Challenge (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	ChallengeTypeID int NOT NULL,
	name text NOT NULL,
	startDateAvailable DATE NOT NULL,
    endDateAvailable DATE NOT NULL,
    radiusLocationAvailable int,
    radiusLocationVisible int,
	latitude int,
	longitude int,
	itemReward int,
	itemSpend int,
	Multiplayer boolean NOT NULL,
	FOREIGN KEY (ChallengeTypeID) REFERENCES ChallengeType (id)
);



CREATE TABLE IF NOT EXISTS GameObjectType(
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	gameID int,
	name text NOT NULL,
	importance int
);

CREATE TABLE IF NOT EXISTS GameObject(
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	gameObjectTypeID int NOT NULL,
	name text NOT NULL,
	keyItem boolean,
	FOREIGN KEY (gameObjectTypeID) REFERENCES GameObjectType (id)
);

CREATE TABLE IF NOT EXISTS PlayMoment(
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	playerID int NOT NULL,
	gameSession int NOT NULL,
	latitude int NOT NULL,
	longitude int NOT NULL,
	play_timestamp DATE NOT NULL,
	FOREIGN KEY (playerID) REFERENCES Player(id)
);


CREATE TABLE IF NOT EXISTS ChallengeInstance (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	ChallengeID int NOT NULL,
	attempted boolean NOT NULL,
	success boolean NOT NULL,
	playerID int NOT NULL,
	ch_timestamp DATE NOT NULL,
	FOREIGN KEY (playerID) REFERENCES Player (id),
	FOREIGN KEY (ChallengeID) REFERENCES Challenge (id)
);

CREATE TABLE IF NOT EXISTS Inventory(
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	playerID int NOT NULL,
	GameObjectID int NOT NULL,
	FOREIGN KEY (GameObjectID) REFERENCES GameObject (id),
	FOREIGN KEY (playerID) REFERENCES Player (id)
);

CREATE TABLE IF NOT EXISTS Purchase();


/*
CREATE TABLE IF NOT EXISTS ChallengeTarget(
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	targetOrder int NOT NULL,
	ChallengeInstanceID int NOT NULL,
	dateSpawned DATE NOT NULL,
	dateCompleted DATE,
	completed boolean NOT NULL,
	latitudeCompleted integer,
	longitudeCompleted integer,
	FOREIGN KEY (ChallengeInstanceID) REFERENCES ChallengeInstance (id)
);


CREATE TABLE IF NOT EXISTS Currency(
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	gameID int NOT NULL,
	monetaryValue NOT NULL,
	name text NOT NULL
);

--this can also be currency
CREATE TABLE IF NOT EXISTS GameObjectInstance(
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	gameObjectID int NOT NULL,
	name text NOT NULL,
	quality int,
	spentIn int,
	rewardFor int,
	FOREIGN KEY (rewardFor) REFERENCES ChallengeInstance (id),
	FOREIGN KEY (spentIn) REFERENCES ChallengeInstance (id)
);


CREATE TABLE IF NOT EXISTS Wallet(
	playerID int NOT NULL,
	CurrencyID int NOT NULL,
	FOREIGN KEY (CurrencyID) REFERENCES Currency (id),
	FOREIGN KEY (playerID) REFERENCES Player (id)
);



CREATE TABLE IF NOT EXISTS Faction(
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	name text NOT NULL
);

CREATE TABLE IF NOT EXISTS FactionMember(
	playerID int NOT NULL,
	factionID int NOT NULL,
	PRIMARY KEY (playerID, factionID)
);

CREATE TABLE IF NOT EXISTS PlayerConnection(
	playerID int NOT NULL,
	playerID2 int NOT NULL,
	PRIMARY KEY (playerID, playerID2)
); */