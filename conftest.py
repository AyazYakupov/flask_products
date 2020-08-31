import os
import tempfile
from datetime import date, timedelta

import pytest

from product_app import models
from product_app import schema
from app import create_app

import pytest


@pytest.fixture
def app():
    return create_app({'TEST': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    from app import db
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()
        db.session.commit()


@pytest.fixture
def session(db):
    return db.session


@pytest.fixture
def categories(session):
    categories = [models.Category(name=i) for i in ('phone', 'tablet', 'e-book', 'movie', 'music', 'electronic')]
    session.add_all(categories)
    session.commit()
    return categories


@pytest.fixture
def product(session, categories):
    product = models.Product(name='phone', expiration_date=date.today() + timedelta(days=30), rating=7,
                             categories=[categories[0], categories[-1]])
    session.add(product)
    session.commit()
    return product


@pytest.fixture
def product_json(categories):
    return dict(
        name="iphone",
        rating=9,
        categories=schema.CategorySchema(many=True).dump([categories[0], categories[5]])
    )
