from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String



user='mbusch'
passwd=open("password.txt").readline().rstrip()
database='insightdb'
table='926969878_T_ONTIME'

Base = declarative_base()
class Flight():
    __tablename__ = table



engine = create_engine('mysql://'+user+':'+str(passwd)+'@localhost/'+database+'.'+table, echo=True)

Session = sessionmaker(bind=engine)
session=Session()
