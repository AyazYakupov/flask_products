from product_app.models import Category, Product
from product_app.schema import ProductSchema, CategorySchema
from datetime import date, timedelta


def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'Hello World!' in rv.data


def test_product_create(app, client, db, product_json):
    response = client.post('/products', json=product_json)
    assert response.status_code == 200
    assert db.session.query(Product).first()


def test_product_create_featured_true(app, client, db, product_json):
    response = client.post('/products', json=product_json)
    assert response.json['featured']


def test_product_create_featured_false(app, client, db, product_json):
    product_json['rating'] = 3
    response = client.post('/products', json=product_json)
    assert not response.json['featured']


def test_product_create_expiration_date_none(app, client, db, product_json):
    response = client.post('/products', json=product_json)
    assert not response.json['expiration_date']


def test_product_create_expiration_date(app, client, db, product_json):
    product_json['expiration_date'] = (date.today() + timedelta(days=5)).strftime('%Y-%m-%d')
    response = client.post('/products', json=product_json)
    assert response.status_code == 200
    assert response.json['expiration_date'] == (date.today() + timedelta(days=5)).strftime('%Y-%m-%d')


def test_product_create_expiration_date_top(app, client, db, product_json):
    product_json['expiration_date'] = (date.today() + timedelta(days=40)).strftime('%Y-%m-%d')
    response = client.post('/products', json=product_json)
    assert response.status_code == 400


def test_product_create_no_categories(app, client, db, product_json):
    product_json['categories'] = []
    response = client.post('/products', json=product_json)
    assert response.status_code == 400


def test_products_get(client, product):
    response = client.get('/products')
    product_schema = ProductSchema().dump(product)
    assert [product_schema] == response.json


def test_products_get_optional(client, product):
    response = client.get(f'/products/{product.id}')
    product_schema = ProductSchema().dump(product)
    assert product_schema == response.json


def test_product_update(db, client, product, categories):
    product.rating = 3
    response = client.put(f'/products/{product.id}', json=ProductSchema().dump(product))
    assert response.status_code == 200
    response = client.get(f'/products/{product.id}')
    assert response.status_code == 200
    assert response.json['rating'] == 3
    assert not response.json['featured']


def test_product_delete(db, client, product):
    client.delete(f'/products/{product.id}')
    assert not Product.query.filter_by(id=product.id).first()
