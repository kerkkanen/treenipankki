CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT
);

CREATE TABLE moves (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users,
    name TEXT,
    muscles TEXT,
    description TEXT
);

CREATE TABLE sets (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users,
    name TEXT,
    description TEXT
);

CREATE TABLE movesets (
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
