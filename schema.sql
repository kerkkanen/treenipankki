CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR (30) UNIQUE,
    password TEXT,
    admin BOOLEAN
);

CREATE TABLE moves (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users (id) ON DELETE CASCADE,
    name VARCHAR (30) UNIQUE,
    muscles TEXT[],
    description TEXT
);

CREATE TABLE sets (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users (id) ON DELETE CASCADE,
    name VARCHAR (30) UNIQUE,
    description TEXT
);

CREATE TABLE moves_in_set (
    set_id INTEGER REFERENCES sets (id) ON DELETE CASCADE,
    move_id INTEGER REFERENCES moves (id) ON DELETE CASCADE
);

CREATE TABLE favourite_sets (
    user_id INTEGER REFERENCES users (id) ON DELETE CASCADE,
    set_id INTEGER REFERENCES sets (id) ON DELETE CASCADE
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users (id) ON DELETE CASCADE,
    set_id INTEGER REFERENCES sets (id) ON DELETE CASCADE,
    trainer_level TEXT,
    dumbells INTEGER,
    comment TEXT
);
