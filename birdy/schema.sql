DROP TABLE IF EXISTS birdy_user;
DROP TABLE IF EXISTS bird;
DROP TABLE IF EXISTS user_birds;

CREATE TABLE birdy_user (
  id SERIAL PRIMARY KEY,
  latitude TEXT NOT NULL,
  longitude TEXT NOT NULL,
  notify TEXT NOT NULL,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE bird (
  id SERIAL PRIMARY KEY,
  species_code TEXT NOT NULL,
  common_name TEXT NOT NULL,
  sci_name TEXT NOT NULL
);

CREATE TABLE user_birds (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  bird_id INTEGER NOT NULL
);
