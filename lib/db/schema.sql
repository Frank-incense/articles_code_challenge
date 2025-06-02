
CREATE TABLE IF NOT EXISTS articles(
    id INTEGER PRIMARY KEY,
    author_id INTEGER NOT NULL,
    magazine_id INTEGER NOT NULL,
    title VARCHAR NOT NULL,
    FOREIGN KEY (author_id) REFERENCES authors(id),
    FOREIGN KEY (magazine_id) REFERENCES mgazines(id)
    );

CREATE TABLE IF NOT EXISTS authors(
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL
    );


CREATE TABLE magazines(
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    category VARCHAR
    );