from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy import Integer, String, create_engine, ForeignKey, Table, Column
from flask_login import UserMixin

engine = create_engine('sqlite:///app.db')
SessionLocal = sessionmaker(bind=engine)

# Base declarativa
class Base(DeclarativeBase):
    pass

# Tabela de associação para o relacionamento N:N
user_livros = Table(
    'user_livros', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('livro_id', Integer, ForeignKey('livros.id'), primary_key=True)
)

class User(Base, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)

    # Relacionamento N:N entre users e livros
    livros: Mapped[list["Livro"]] = relationship(
        'Livro', 
        secondary=user_livros, 
        back_populates='autores'
    )


class Livro(Base):
    __tablename__ = 'livros'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(120), nullable=False)
    ano: Mapped[int] = mapped_column(Integer, nullable=True)
    
    # REMOVIDO: autor_id (relacionamento antigo 1:N)
    # O relacionamento agora é apenas N:N através da tabela user_livros

    # Relacionamento N:N entre livros e users
    autores: Mapped[list['User']] = relationship(
        'User', 
        secondary=user_livros, 
        back_populates='livros'
    )