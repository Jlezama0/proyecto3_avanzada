
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base


SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root@localhost/proyecto3'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
meta_data = MetaData()

# def init_db():

#     Base.metadata.create_all(bind=engine)
