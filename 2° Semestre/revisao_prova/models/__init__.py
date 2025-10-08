from database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, ForeignKey


# User agora é um modelo
class User(Base):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome:Mapped[str] = mapped_column(String(30))
    email:Mapped[str] = mapped_column(String(100), unique=True)
    produtos = relationship('Product', backref='user')

class Product(Base):
    __tablename__ = "products"
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome:Mapped[str] = mapped_column(String(30))
    valor:Mapped[float] = mapped_column(Float)

    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))

    
