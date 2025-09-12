from sqlalchemy import create_engine, text

# ORM - Object Relaticional Mapper
# pip install sqlalchemy

SQLITE = "sqlite://database.db"
engine = create_engine(SQLITE)

