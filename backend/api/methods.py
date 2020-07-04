from api import db, ma
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    location = db.Column(db.String, unique=True, nullable=False)
    enabled = db.Column(db.Integer, nullable=False)


class LocationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'location', 'enabled')


location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    enabled = db.Column(db.Integer, nullable=False)


class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'enabled')


item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


class ItemLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, ForeignKey(Item.id), nullable=False)
    date = db.Column(db.String, nullable=False)
    log = db.Column(db.Integer, nullable=False)
    location_id = db.Column(db.Integer, ForeignKey(Location.id), nullable=False)

    item = relationship(Item)


class ItemLogSchema(ma.Schema):
    class Meta:
        fields = ('id', 'item_id', 'date', 'log', 'location_id')


item_log_schema = ItemLogSchema()
item_logs_schema = ItemLogSchema(many=True)


class Stocks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String, nullable=False, unique=True)


class StocksSchema(ma.Schema):
    class Meta:
        fields = ('id', 'ticker')


stock_schema = StocksSchema()
stocks_schema = StocksSchema(many=True)


db.create_all()
