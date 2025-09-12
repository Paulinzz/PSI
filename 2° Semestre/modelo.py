from sqlalchemy import create_engine, text, String
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

engine = create_engine('sqlite:///mercado.db')
sessao = Session(bind=engine)

class Base(DeclarativeBase):
    pass

class Produto(Base):
    __tablename__ = 'produtos'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome:Mapped[str] = mapped_column(String(30))

    def __repr__ (self):
        return f"Produto: {self.nome}"

Base.metadata.create_all(bind=engine)


sessao.begin()
sessao.close()