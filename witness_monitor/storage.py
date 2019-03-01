from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine("sqlite:///witness_monitor.sqlite", echo=False)
Base.metadata.create_all(engine)

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()


class Cache(Base):
    __tablename__ = "cache"
    id = Column(Integer, primary_key=True)
    key = Column(String(50))
    value = Column(Text)
