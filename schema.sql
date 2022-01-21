CREATE TABLE trainer (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT,
);

CREATE TABLE moves (
    id SERIAL PRIMARY KEY,
    name TEXT,
    muscles TEXT,
    description TEXT
);

CREATE TABLE sets (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT
);

CREATE TABLE setmoves (
    set_id INTEGER REFERENCES sets,
    move_id INTEGER REFERENCES moves
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    set_id INTEGER REFERENCES sets,
    trainer_level TEXT,
    dumbells INTEGER,
    comment TEXT
);
