from app import db
from . import models
from . import schema
from flask import Response, request, Blueprint, jsonify
from . import error_handler

product_schema = schema.ProductSchema()
product_schemes = schema.ProductSchema(many=True)

products_blueprint = Blueprint('products', 'products', url_prefix='')


@products_blueprint.route('/products', methods=['GET'])
@error_handler
def get_products():
    query = db.session.query(models.Product).all()
    return jsonify(product_schemes.dump(query))


@products_blueprint.route('/products/<int:product_id>', methods=['GET'])
@error_handler
def get_product(product_id):
    query = db.session.query(models.Product).get(product_id)
    return jsonify(product_schema.dump(query))


@products_blueprint.route('/products', methods=['POST'])
@error_handler
def create_product():
    validated_data = product_schema.validate(request.json)
    product = product_schema.load(validated_data)

    db.session.add(product)
    db.session.commit()
    return jsonify(product_schema.dump(product))


@products_blueprint.route('/products/<int:product_id>', methods=['PUT'])
@error_handler
def update_product(product_id):
    product = product_schema.load(request.json)
    db.session.add(product)
    db.session.commit()
    return jsonify(product_schema.dump(product))


@products_blueprint.route('/products/<int:product_id>', methods=['DELETE'])
@error_handler
def delete_product(product_id):
    product = models.Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return Response('OK')
