create table usuarios (
    id integer primary key autoincrement, 
    nome text
);

create table livros(
    id integer primary key autoincrement,
    titulo text,
    usuario_id integer references usuarios(id) on delete cascade on update cascade
);