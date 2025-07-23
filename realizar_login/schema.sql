
create table if not exists users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    senha TEXT NOT NULL
)

create table if not exists livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);
