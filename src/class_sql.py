from sqlalchemy import create_engine, Column, Integer,Text, Date
from sqlalchemy.orm import sessionmaker,declarative_base

Base = declarative_base()

class sncf(Base):
    __tablename__= "sncf"
    OBJECT = Column(Text, primary_key=True)
    DATE = Column(Date)
    FULL_DATE = Column(Date, primary_key=True)
    YEAR = Column(Text)
    MONTH = Column(Text)
    TIME = Column(Text)