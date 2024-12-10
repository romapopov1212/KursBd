from sqlalchemy import Column, Integer, String, Boolean, Text, DOUBLE
from sqlalchemy.orm import declarative_base
Base = declarative_base()

class Products(Base):
    __tablename__ = "Products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)