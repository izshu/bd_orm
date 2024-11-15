import sqlalchemy as sq
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = Column(Integer, primary_key=True)
    name = Column(String(250))

    books = relationship("Book", back_populates="publisher")


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    title = Column(String(250))
    id_publisher = Column(Integer, ForeignKey("publisher.id"))

    publisher = relationship("Publisher", back_populates="books")
    stock = relationship("Stock", back_populates="book")


class Shop(Base):
    __tablename__ = "shop"

    id = Column(Integer, primary_key=True)
    name = Column(String(250))

    stock = relationship("Stock", back_populates="shop")


class Stock(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey("book.id"))
    id_shop = Column(Integer, ForeignKey("shop.id"))
    count = Column(Integer)

    book = relationship("Book", back_populates="stock")
    shop = relationship("Shop", back_populates="stock")
    sales = relationship("Sale", back_populates="stock")


class Sale(Base):
    __tablename__ = "sale"

    id = Column(Integer, primary_key=True)
    price = Column(Numeric)
    date_sale = Column(Date)
    id_stock = Column(Integer, ForeignKey("stock.id"))
    count = Column(Integer)

    stock = relationship("Stock", back_populates="sales")


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
