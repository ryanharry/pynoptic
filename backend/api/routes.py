import os
from flask import jsonify, request
from api import app, local_environment, db
from api.functions import get_stock_data, get_stock_tickers, check_tracker_is_complete, \
check_if_previous_logged, log_tracker_item, create_location, create_item, create_stock, deselect_locations
from api.methods import Item, items_schema, location_schema, Location, stocks_schema, Stocks,\
locations_schema
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


@app.route('/', methods=['GET'])
def check_active():
    return jsonify({'active': True})


@app.route('/credentials', methods=['GET'])
def get_credentials():
    current_dir = os.getcwd()
    file_to_open = current_dir + '/api/data/key.txt'
    with open(file_to_open) as api_key:
        return jsonify({'api_key': api_key.readline()})


@app.route('/stocks', methods=['GET'])
def stock_data():
    tickers = []
    user_tickers = get_stock_tickers()
    tickers += user_tickers
    stock_data_list = []
    for ticker in tickers:
        data = get_stock_data(ticker=ticker)
        stock_data_list.append(data)
    return jsonify(stock_data_list)


@app.route('/stocks/add', methods=['POST'])
def stocks_add():
    ticker = request.json['ticker']
    stock = create_stock(ticker=ticker)
    all_data = Stocks.query.all()
    dump = stocks_schema.dump(all_data)
    if stock:
        return jsonify(dump)
    else:
        return jsonify({'error': 'error with adding ticker', 'data': dump})


@app.route('/stocks/remove', methods=['DELETE'])
def stocks_delete():
    ticker = request.json['ticker_id']
    try:
        stock = Stocks.query.get(ticker)
        db.session.delete(stock)
        db.session.commit()
        all_data = Stocks.query.all()
        dump = stocks_schema.dump(all_data)
        return jsonify(dump)
    except NoResultFound:
        all_data = Stocks.query.all()
        dump = stocks_schema.dump(all_data)
        return jsonify({'error': 'error with removing ticker', 'data': dump})


@app.route('/stocks/select', methods=['GET'])
def stock_selections():
    stocks = Stocks.query.all()
    dump = stocks_schema.dump(stocks)
    return jsonify(dump)


@app.route('/tracker', methods=['GET'])
def tracker_data():
    get_trackers = db.session.query(Item).filter(Item.enabled == 1).all()
    dump = items_schema.dump(get_trackers)
    return jsonify(dump)


@app.route('/tracker/select', methods=['GET'])
def tracker_select():
    get_trackers = Item.query.all()
    dump = items_schema.dump(get_trackers)
    return jsonify(dump)


@app.route('/tracker/add', methods=['POST'])
def tracker_add():
    name = request.json['name']
    tracker = create_item(name=name, enabled=1)
    all_data = Item.query.all()
    dump = items_schema.dump(all_data)
    if tracker:
        return jsonify(dump)
    else:
        return jsonify({'error': 'error with adding item', 'data': dump})


@app.route('/tracker/log', methods=['POST'])
def tracker_log():
    item_id = request.json['item_id']
    date = request.json['date']
    location_id = request.json['location_id']
    log = log_tracker_item(item_id=item_id, date=date, location_id=location_id)
    return jsonify(log)


@app.route('/tracker/status', methods=['POST'])
def tracker_status():
    item_id = request.json['item_id']
    date = request.json['date']
    location_id = request.json['location_id']
    check_if_previous_logged(item_id=item_id, date=date, location_id=location_id)
    status = check_tracker_is_complete(item_id=item_id, date=date)
    return jsonify(status)


@app.route('/tracker/disable', methods=['PUT'])
def tracker_remove():
    item_id = request.json['item_id']
    try:
        item = Item.query.get(item_id)
        item.enabled = 0
        db.session.commit()
        all_data = Item.query.all()
        dump = items_schema.dump(all_data)
        return jsonify(dump)
    except NoResultFound:
        all_data = Item.query.all()
        dump = items_schema.dump(all_data)
        return jsonify({'error': 'item not found', 'data': dump})


@app.route('/tracker/enable', methods=['PUT'])
def tracker_enable():
    item_id = request.json['item_id']
    try:
        item = Item.query.get(item_id)
        item.enabled = 1
        db.session.commit()
        all_data = Item.query.all()
        dump = items_schema.dump(all_data)
        return jsonify(dump)
    except NoResultFound:
        all_data = Item.query.all()
        dump = items_schema.dump(all_data)
        return jsonify({'error': 'item not found', 'data': dump})


@app.route('/location', methods=['GET'])
def location_data():
    try:
        location = db.session.query(Location).filter(Location.enabled == 1).one()
        dump = location_schema.dump(location)
        return jsonify(dump)
    except NoResultFound:
        return jsonify({'error': 'error with location selection'})
    except MultipleResultsFound:
        deselect_locations()
        return jsonify({'error': 'error with location selection'})


@app.route('/locations', methods=['GET'])
def locations_data():
    locations = Location.query.all()
    dump = locations_schema.dump(locations)
    return jsonify(dump)


@app.route('/location/add', methods=['POST'])
def location_add():
    location_id = request.json['location_id']
    name = request.json['name']
    deselect_locations()
    location = create_location(name=name, location=location_id, enabled=1)
    if location:
        dump = location_schema.dump(location)
        return jsonify(dump)
    else:
        return jsonify({'error': 'Error with location creation'})


@app.route('/location/select', methods=['PUT'])
def location_select():
    location_id = request.json['location_id']
    deselect_locations()
    try:
        select = Location.query.get(location_id)
        select.enabled = 1
        db.session.commit()
        dump = location_schema.dump(select)
        return jsonify(dump)
    except NoResultFound:
        return jsonify({'error': 'Location does not exist'})
