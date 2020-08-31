from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean, Date, MetaData
from sqlalchemy.orm import relationship

product_category = Table(
    'products_categories', db.Model.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)


class Category(db.Model):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)


class Product(db.Model):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    expiration_date = Column(Date)
    rating = Column(Integer, default=1)
    featured = Column(Boolean, default=False)
    categories = relationship('Category', secondary=product_category, lazy='subquery', backref='products')
