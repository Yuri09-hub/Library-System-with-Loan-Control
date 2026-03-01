from sqlalchemy import Column,ForeignKey, Float, Boolean, Integer, String,create_engine
from sqlalchemy.orm import relationship, declarative_base

db = create_engine('sqlite:///data.db')

base = declarative_base()


