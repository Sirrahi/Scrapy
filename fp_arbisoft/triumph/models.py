from triumph import db
from sqlalchemy import PrimaryKeyConstraint

item_category = db.Table('item_category', db.metadata,
                         db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
                         db.Column('item_id', db.Integer, db.ForeignKey('item.id'))
                         )

item_feature = db.Table('item_feature', db.metadata,
                        db.Column('item_id', db.Integer, db.ForeignKey('item.id')),
                        db.Column('feature_id', db.Integer, db.ForeignKey('feature.id'))
                        )


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    items = db.relationship('Item', backref=db.backref('category', lazy='dynamic'), secondary=item_category)

    def __init__(self, name):
        self.name = name


class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer)
    name = db.Column(db.String(64))
    brand = db.Column(db.String(64))
    description = db.Column(db.String(1024))
    # url = db.Column(db.String(1024))
    features = db.relationship('Feature', backref=db.backref('feature_item', lazy='dynamic'), secondary=item_feature)
    skus = db.relationship('Sku', backref=db.backref('sku_item'))
    image_urls = db.relationship('ImageUrl', backref=db.backref('image_item'))

    __table_args__ = (
        PrimaryKeyConstraint("id", name="id"),
    )

    def __init__(self, item_id, name, brand, description):
        self.id = item_id
        self.name = name
        self.brand = brand
        self.description = description
        # self.url =url


class Feature(db.Model):
    __tablename__ = 'feature'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __init__(self, name):
        self.name = name


class Sku(db.Model):
    __tablename__ = 'sku'

    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(32))
    size = db.Column(db.String(16))
    price = db.Column(db.String(16))
    currency = db.Column(db.String(16))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    image_urls = db.relationship('ImageUrl', backref=db.backref('image_sku'))

    def __init__(self, color, size, price, currency):
        self.color = color
        self.size = size
        self.price = price
        self.currency = currency


class ImageUrl(db.Model):
    __tablename__ = 'skuimageurl'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1024))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    sku_id = db.Column(db.Integer, db.ForeignKey('sku.id'))

    def __init__(self, url):
        self.url = url



