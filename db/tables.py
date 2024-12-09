from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Purchase(Base):
    __tablename__ = "Purchase"
    id_purchase = Column(Integer, primary_key=True, index=True)
    buyer_number = Column(String, unique=True)
    date = Column(String)
    full_price = Column(Integer)

class Products(Base):
    __tablename__ = "Products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)


class PurchasedProducts(Base):
    __tablename__ = "PurchasedProducts"
    id_purchase = Column(Integer, ForeignKey('Purchase.id_purchase'), primary_key=True)
    id_product = Column(Integer, ForeignKey('Products.id'), primary_key=True)
    count = Column(Integer)

class Buyers(Base):
    __tablename__ = "Buyers"
    telephone_number = Column(String, primary_key=True)
    name = Column(String)
    surname = Column(String)
    lastname = Column(String)