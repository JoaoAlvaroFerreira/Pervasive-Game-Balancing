DROP TABLE IF EXISTS Player;
DROP TABLE IF EXISTS Demographic;
DROP TABLE IF EXISTS PlayerLocationInfo;
DROP TABLE IF EXISTS GameplayMoments; --to do
DROP TABLE IF EXISTS PlayerStats; ---to do
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


-- projects table
CREATE TABLE IF NOT EXISTS Game (
	id SERIAL PRIMARY KEY,
	name text NOT NULL,
	locationbased boolean NOT NULL,
	timebased boolean NOT NULL,
	socialexpansion boolean NOT NULL
);

-- tasks table
CREATE TABLE IF NOT EXISTS ChallengeType (
	id SERIAL PRIMARY KEY,
	gameID int NOT NULL,
	name text NOT NULL,
	temporary boolean NOT NULL,
	narrative boolean NOT NULL,
	uniqueChallenge boolean NOT NULL,
	FOREIGN KEY (gameID) REFERENCES Game (id)
);

CREATE TABLE IF NOT EXISTS Challenge (
	id SERIAL PRIMARY KEY,
	ChallengeTypeID int NOT NULL,
	name text NOT NULL,
	TimeRestraint boolean NOT NULL,
	SpaceRestraint boolean NOT NULL,
	Multiplayer boolean NOT NULL,
	FOREIGN KEY (ChallengeTypeID) REFERENCES ChallengeType (id)
);

CREATE TABLE IF NOT EXISTS ChallengeInstance (
	id SERIAL PRIMARY KEY,
	ChallengeID int NOT NULL,
	name text NOT NULL,
	dateSpawned DATE NOT NULL,
	latitude integer,
	longitude integer,
	completed boolean NOT NULL,
	playerID int NOT NULL,
	playerID2 int,
	FOREIGN KEY (playerID) REFERENCES Player (id),
	FOREIGN KEY (ChallengeID) REFERENCES Challenge (id)
);

CREATE TABLE IF NOT EXISTS ChallengeTarget(
	id SERIAL PRIMARY KEY,
	targetOrder int NOT NULL,
	ChallengeInstanceID SERIAL NOT NULL,
	dateSpawned DATE NOT NULL,
	dateCompleted DATE,
	completed boolean NOT NULL,
	latitudeCompleted integer,
	longitudeCompleted integer,
	FOREIGN KEY (ChallengeInstanceID) REFERENCES ChallengeInstance (id)
);


CREATE TABLE IF NOT EXISTS GameObjectType(
	id SERIAL PRIMARY KEY,
	gameID int NOT NULL,
	name text NOT NULL,
	importance int,
	FOREIGN KEY (gameID) REFERENCES Game (id)
);

CREATE TABLE IF NOT EXISTS GameObject(
	id SERIAL PRIMARY KEY,
	gameObjectTypeID int NOT NULL,
	name text NOT NULL,
	keyItem boolean,
	FOREIGN KEY (gameObjectTypeID) REFERENCES GameObjectType (id)
);

CREATE TABLE IF NOT EXISTS Currency(
	id SERIAL PRIMARY KEY,
	gameID int NOT NULL,
	monetaryValue NOT NULL,
	name text NOT NULL,
	FOREIGN KEY (gameID) REFERENCES Game (id)
);

--this can also be currency
CREATE TABLE IF NOT EXISTS GameObjectInstance(
	id SERIAL PRIMARY KEY,
	gameObjectID int NOT NULL,
	name text NOT NULL,
	quality int,
	spentIn int,
	rewardFor int,
	FOREIGN KEY (rewardFor) REFERENCES ChallengeInstance (id),
	FOREIGN KEY (spentIn) REFERENCES ChallengeInstance (id)
);

CREATE TABLE IF NOT EXISTS Inventory(
	playerID int NOT NULL,
	gameObjectInstanceID int NOT NULL,
	FOREIGN KEY (gameObjectInstanceID) REFERENCES GameObjectInstance (id),
	FOREIGN KEY (playerID) REFERENCES Player (id)
);

CREATE TABLE IF NOT EXISTS Wallet(
	playerID int NOT NULL,
	CurrencyID int NOT NULL,
	FOREIGN KEY (CurrencyID) REFERENCES Currency (id),
	FOREIGN KEY (playerID) REFERENCES Player (id)
);

CREATE TABLE IF NOT EXISTS Player(
	id SERIAL PRIMARY KEY,
	gameID int,
	name text NOT NULL,
	FOREIGN KEY (gameID) REFERENCES Game (id)
);

CREATE TABLE IF NOT EXISTS Demographic(
	playerID int PRIMARY KEY,
	Age int NOT NULL,
	Education text NOT NULL,
	Ethnicity int NOT NULL,
	SocioEconomicStatus int NOT NULL,
	FOREIGN KEY (playerID) REFERENCES Player (id)
);

CREATE TABLE IF NOT EXISTS PlayerLocationInfo(
	playerID int PRIMARY KEY,
	latitude int NOT NULL,
	longitude int NOT NULL,
	city text NOT NULL,
	typicalWeather int NOT NULL,
	FOREIGN KEY (playerID) REFERENCES Player (id)
);


CREATE TABLE IF NOT EXISTS Faction(
	id SERIAL PRIMARY KEY,
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
);