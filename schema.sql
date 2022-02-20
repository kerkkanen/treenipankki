CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR (30) UNIQUE,
    password TEXT
);

CREATE TABLE moves (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users,
    name VARCHAR (30) UNIQUE,
    muscles TEXT[],
    description TEXT
);

CREATE TABLE sets (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users,
    name VARCHAR (30) UNIQUE,
    description TEXT
);

CREATE TABLE moves_in_set (
    set_id INTEGER REFERENCES sets,
    move_id INTEGER REFERENCES moves
);

CREATE TABLE favourite_sets (
    user_id INTEGER REFERENCES users,
    set_id INTEGER REFERENCES sets
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users,
    set_id INTEGER REFERENCES sets,
    trainer_level TEXT,
    dumbells INTEGER,
    comment TEXT
);
