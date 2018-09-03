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
    item = db.relationship('Item', backref=db.backref('category', lazy='dynamic'), secondary=item_category)


class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(1024))
    feature = db.relationship('Feature', backref=db.backref('feature_item', lazy='dynamic'), secondary=item_feature)
    skus = db.relationship('Sku', backref=db.backref('sku_item', uselist=True))


class Feature(db.Model):
    __tablename__ = 'feature'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)


class Sku(db.Model):
    __tablename__ = 'sku'
    id = db.Column(db.Integer, primary_key=True)
    color = db.column(db.String(32))
    size = db.column(db.String(8))
    price = db.column(db.String(16))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    image_urls = db.relationship('ImageUrl', backref=db.backref('image_sku', uselist=True))


class ImageUrl(db.Model):
    __tablename__ = 'imageurl'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1024))
    sku_id = db.Column(db.Integer, db.ForeignKey('sku.id'))


