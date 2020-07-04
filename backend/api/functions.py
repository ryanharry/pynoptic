from yahoo_finance_api2 import share
import math
from api.methods import Stocks, Item, ItemLog, Location
from api import db
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
import datetime as d


class DateFromJSToPy:
    def __init__(self, js_date_string):
        self.js_date_string = js_date_string
        self.py_date = self.convert_js_to_py()

    def convert_js_to_py(self):
        month_string = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month_int = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        month_dict = dict(zip(month_string, month_int))
        split_js = self.js_date_string.split(' ')
        py_date = d.date(year=int(split_js[3]), month=int(month_dict[split_js[1]]), day=int(split_js[2]))
        return py_date


def get_stock_data(ticker):
    stock = share.Share(ticker)
    stock_info = stock.get_historical(share.PERIOD_TYPE_DAY, 1, share.FREQUENCY_TYPE_DAY, 1)
    open_value = None
    close_value = None
    try:
        for key, value in stock_info.items():
            if key == 'open':
                open_value = value[0]
            if key == 'close':
                close_value = value[0]
        current = close_value
        change = ((close_value - open_value) / open_value) * 100
        current_rounded = math.ceil(current * 100)/100
        change_rounded = math.ceil(change * 100)/100
        return {'ticker': ticker, 'current': current_rounded, 'change': change_rounded}
    except AttributeError:
        return {'ticker': ticker, 'current': '-', 'change': '-'}


def get_stock_tickers():
    stocks = db.session.query(Stocks).all()
    tickers = [stock.ticker for stock in stocks]
    return tickers


def check_tracker_is_complete(item_id, date):
    py_date = DateFromJSToPy(js_date_string=date)
    try:
        db.session.query(ItemLog).filter(and_(ItemLog.item_id == item_id, ItemLog.date == py_date.py_date)).one()
        return {'status': True}
    except NoResultFound:
        return {'status': False}


def check_if_previous_logged(item_id, date, location_id):
    py_date = DateFromJSToPy(js_date_string=date)
    previous = py_date.py_date - d.timedelta(days=1)
    try:
        db.session.query(ItemLog).filter(and_(ItemLog.item_id == item_id, ItemLog.date == previous)).one()
        return None
    except NoResultFound:
        try:
            location = db.session.query(Location).filter(Location.location == location_id).one()
            log = ItemLog(item_id=item_id, date=previous, log=0, location_id=location.id)
        except NoResultFound:
            log = ItemLog(item_id=item_id, date=previous, log=0, location_id=0)
        db.session.add(log)
        db.session.commit()
        return None


def log_tracker_item(item_id, date, location_id):
    py_date = DateFromJSToPy(js_date_string=date)
    try:
        db.session.query(ItemLog).filter(and_(ItemLog.item_id == item_id, ItemLog.date == py_date.py_date)).one()
        return {'status': True}
    except NoResultFound:
        try:
            location = db.session.query(Location).filter(Location.location == location_id).one()
            log = ItemLog(item_id=item_id, date=py_date.py_date, log=1, location_id=location.id)
        except NoResultFound:
            log = ItemLog(item_id=item_id, date=py_date.py_date, log=1, location_id=0)
        db.session.add(log)
        db.session.commit()
        return {'status': True}


def deselect_locations():
    current = db.session.query(Location).all()
    if len(current) > 0:
        for location in current:
            if location.enabled == 1:
                location.enabled = 0
                db.session.commit()
    return True


def create_location(name, location, enabled):
    try:
        new = Location(name=name, location=location, enabled=enabled)
        db.session.add(new)
        db.session.commit()
        return new
    except IntegrityError:
        return None


def create_item(name, enabled):
    try:
        new = Item(name=name, enabled=enabled)
        db.session.add(new)
        db.session.commit()
        return new
    except IntegrityError:
        return None


def create_stock(ticker):
    try:
        new = Stocks(ticker=ticker)
        db.session.add(new)
        db.session.commit()
        return new
    except IntegrityError:
        return None
