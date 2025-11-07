# app/models/models.py

from sqlalchemy import Column,Integer,String,Float
from database import Base


class Users(Base):   
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name=Column(String(100), unique=False, nullable=False)
    last_name=Column(String(100), unique=False, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(10), unique=True, nullable=False)

class Laptop(Base):
    __tablename__ = "laptops"
    sr_no = Column(Integer, primary_key=True, index=True, autoincrement=True)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    processor = Column(String(100), nullable=False)
    ram = Column(Integer, nullable=False)
    storage = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    count = Column(Integer, nullable=False)
