from marshmallow import validates, fields, ValidationError
from marshmallow_sqlalchemy import ModelSchema
from product_app.models import Product, Category
from app import db
from datetime import date, timedelta


class CategorySchema(ModelSchema):
    class Meta:
        model = Category
        sqla_session = db.session
        fields = ['id', 'name']


class ProductSchema(ModelSchema):
    class Meta:
        model = Product
        sqla_session = db.session

    name = fields.String()
    expiration_date = fields.Date(null=True)
    rating = fields.Integer()
    featured = fields.Boolean()
    categories = fields.Nested(CategorySchema, many=True)

    @validates('expiration_date')
    def validate_expiration_date(self, expiration_date):
        if expiration_date:
            if not isinstance(expiration_date, date):
                msg = 'expiration date has no correct type'
                raise ValidationError(msg)
            if expiration_date > date.today() + timedelta(days=30):
                msg = 'expiration date should be less than 30 days from today'
                raise ValidationError(msg)
        return expiration_date

    @validates('categories')
    def validate_categories(self, categories):
        if 5 > len(categories) < 2:
            msg = 'A product must have from 1 to 5 categories'
            raise ValidationError(msg)
        return categories

    def validate(self, data, *args, **kwargs):
        if data['rating'] >= 8:
            data['featured'] = True
        else:
            data['featured'] = False
        return data
