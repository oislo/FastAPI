from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Using PostgreSQ
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:<InsertThePasswordHere>@localhost/TodoApplicationDatabase"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()




"""The below are uses for sqlite3"""
# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()



"""The below are uses for mysql. pip install pymysql """
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:<InsertThePasswordHere>.0.0.1:3333/todoapp"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
