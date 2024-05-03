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
    cmc INTEGER,
    rarity TEXT,
    power INTEGER,
    toughness INTEGER,
    userid INTEGER,
    photo INTEGER
);

CREATE TABLE libraries (
    id SERIAL PRIMARY KEY,
    userid INTEGER REFERENCES users,
    name TEXT
);

CREATE TABLE cardlib (
    card INTEGER REFERENCES cards ON DELETE CASCADE,
    library INTEGER REFERENCES libraries,
);

CREATE TABLE backside (
    id SERIAL PRIMARY KEY,
    frontid INTEGER REFERENCES cards ON DELETE CASCADE,
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