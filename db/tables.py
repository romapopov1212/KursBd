from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, Numeric
from sqlalchemy.orm import declarative_base, relationship
Base = declarative_base()


class Buyers(Base):
    __tablename__ = "Buyers"
    telephone_number = Column(String, primary_key=True)
    name = Column(String)
    surname = Column(String)
    lastname = Column(String)
   # is_admin = Column(Boolean)
    purchases = relationship("Purchase", back_populates="buyer")


class Purchase(Base):
    __tablename__ = "Purchase"
    id_purchase = Column(Integer, primary_key=True, index=True)
    buyer_number = Column(String, ForeignKey('Buyers.telephone_number'), nullable=False)
    date = Column(String)
    full_price = Column(Numeric)

    buyer = relationship("Buyers", back_populates="purchases")
    purchased_products = relationship("PurchasedProducts", back_populates="purchase")


class Products(Base):
    __tablename__ = "Products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Numeric)
    count = Column(Integer)

    purchased_products = relationship("PurchasedProducts", back_populates="product")


class PurchasedProducts(Base):
    __tablename__ = "PurchasedProducts"
    id_purchase = Column(Integer, ForeignKey('Purchase.id_purchase'), primary_key=True)
    id_product = Column(Integer, ForeignKey('Products.id'), primary_key=True)

    count = Column(Integer)

    purchase = relationship("Purchase", back_populates="purchased_products")
    product = relationship("Products", back_populates="purchased_products")
    