from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker   


engine = create_engine('mysql+pymysql://root:@localhost:3306/test') # utilizando extensoes como mysql e pymysql e config basic como user root, sem senhas, ip localhost e porta padrao

Base = declarative_base() # class (variavel) python para modelo para as outras tabelas

_Sessao = sessionmaker(engine)

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String(40))

Base.metadata.create_all(engine)    

sessao = _Sessao()
usuario = Usuario(nome='joao')
sessao.add(usuario)
sessao.commit()