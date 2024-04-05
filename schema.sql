DROP TABLE IF EXISTS cards CASCADE;
DROP TABLE IF EXISTS libraries CASCADE;
DROP TABLE IF EXISTS cardlib CASCADE;
DROP TABLE IF EXISTS backside CASCADE;
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE cards (
    id SERIAL PRIMARY KEY,
    name TEXT,
    twofaced BOOLEAN,
    colour TEXT,
    cmc TEXT,
    rarity TEXT,
    power TEXT,
    toughness TEXT,
    userid INTEGER,
    photo INTEGER
);

CREATE TABLE libraries (
    id SERIAL PRIMARY KEY,
    userid INTEGER,
    name TEXT
);

CREATE TABLE cardlib (
    card INTEGER,
    library INTEGER,
    visible BOOLEAN
);

CREATE TABLE backside (
    id SERIAL PRIMARY KEY,
    frontid INTEGER,
    name TEXT,
    cmc TEXT,
    power TEXT,
    toughness TEXT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);