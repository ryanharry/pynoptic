import requests


class Setup:
    def __init__(self):
        self.state = self.check_state()
        self.quick_start()
        self.run()

    def quick_start(self):
        for key, value in self.state.items():
            if key == 'location':
                if len(value) == 0:
                    self.add_location()
            elif key == 'tickers':
                if len(value) == 0:
                    self.add_tickers()
            elif key == 'items':
                if len(value) == 0:
                    self.add_items()

    def check_state(self):
        try:
            get_location = requests.get(url='http://127.0.0.1:5555/location').json()
            get_tickers = requests.get(url='http://127.0.0.1:5555/stocks/select').json()
            get_items = requests.get(url='http://127.0.0.1:5555/tracker').json()
            try:
                location = get_location['location']
            except KeyError:
                location = []
            tickers = []
            for data in get_tickers:
                tickers.append(data['ticker'])
            items = []
            for item in get_items:
                if item['enabled'] == 1:
                    items.append(item['name'])
            print('---')
            print(f'Current Location: {location}')
            print(f'Current Stock Tickers: {tickers}')
            print(f'Current Items: {items}')
            print('---')
            return {'location': location, 'tickers': tickers, 'items': items}
        except requests.exceptions.ConnectionError:
            print('No connection to the application, run the api container before trying again')
            exit()

    def locations(self):
        print('\t/// LOCATION ///')
        print('\t0 : Back')
        print('\t1 : Create New Location')
        print('\t2 : Update Current Location')
        choice = input('Input: ')
        if choice == '1':
            self.add_location()
        elif choice == '2':
            print('Input the location id for the city of interest below')
            locations = requests.get(url='http://127.0.0.1:5555/locations').json()
            for location in locations:
                name = location['name']
                location_id = location['id']
                print(f'\tId: {location_id}\t|City: {name}')
            location_id = input('Location id: ')
            requests.put(url='http://127.0.0.1:5555/location/select',
                         json={'location_id': location_id})
        elif choice == '0':
            pass
        else:
            print('Please select an available option')
            self.locations()

    def stocks(self):
        print('\t/// STOCKS ///')
        print('\t0 : Back')
        print('\t1 : Create New Ticker')
        print('\t2 : Remove Existing Ticker')
        choice = input('Input: ')
        if choice == '1':
            self.current_stock_tickers()
            self.add_tickers()
        elif choice == '2':
            print('Input the ticker id(s) to remove in a comma separated list:')
            ticker_selection = requests.get(url='http://127.0.0.1:5555/stocks/select').json()
            for ticker in ticker_selection:
                ticker_id = ticker['id']
                ticker_name = ticker['ticker']
                print(f'\tId: {ticker_id}\t|Ticker: {ticker_name}')
            ticker_ids = input('Ticker Id: ')
            ticker_ids_split = ticker_ids.split(',')
            for ticker_id in ticker_ids_split:
                if ticker_id.strip() != '':
                    requests.delete(url='http://127.0.0.1:5555/stocks/remove', json={'ticker_id': ticker_id.strip()})
            self.current_stock_tickers()
        elif choice == '0':
            pass
        else:
            print('Please select an available option')

    def items(self):
        print('\t/// ITEMS ///')
        print('\t0 : Back')
        print('\t1 : Create New Item')
        print('\t2 : Enable Item')
        print('\t3 : Disable Item')
        choice = input('Input: ')
        if choice == '1':
            self.current_item_status()
            self.add_items()
        elif choice == '2':
            print('Enter items from list below that you want to enable for tracking:')
            all_items = requests.get(url='http://127.0.0.1:5555/tracker/select').json()
            for item in all_items:
                if item['enabled'] == 0:
                    item_id = item['id']
                    item_name = item['name']
                    print(f'\tId: {item_id}\t|Item: {item_name}')
            items = input('Item(s):')
            items_split = items.split(',')
            for item in items_split:
                if item.strip() != '':
                    requests.put(url='http://127.0.0.1:5555/tracker/enable', json={'item_id': item.strip()})
            self.current_item_status()
        elif choice == '3':
            print('Enter items from list below that you want to disable from tracking:')
            all_items = requests.get(url='http://127.0.0.1:5555/tracker/select').json()
            for item in all_items:
                if item['enabled'] == 1:
                    item_id = item['id']
                    item_name = item['name']
                    print(f'\tId: {item_id}\t|Item: {item_name}')
            items = input('Item(s):')
            items_split = items.split(',')
            for item in items_split:
                if item.strip() != '':
                    requests.put(url='http://127.0.0.1:5555/tracker/disable', json={'item_id': item.strip()})
            self.current_item_status()
        elif choice == '0':
            pass
        else:
            print('Please select an available option')

    def add_location(self):
        print('Navigate to https://openweathermap.org/find?q=')
        print('Search for the city of interest and paste the id at the end of the url')
        print('https://openweathermap.org/city/this_id_here')
        location_id = input('City Id: ')
        print('Input the city name below')
        name = input('City Name: ')
        try:
            new_location = requests.post(url='http://127.0.0.1:5555/location/add',
                                         json={'name': name, 'location_id': location_id})
            location = new_location.json()
            name = location['name']
            location_id = location['location']
            print(f'\tCity: {name}\t|Location Id: {location_id}')
            return location
        except KeyError:
            print('Error with location creation')

    def add_tickers(self):
        print('Enter the stock tickers you want to track in a comma separated list:')
        tickers = input('Ticker(s): ')
        tickers_split = tickers.split(',')
        for ticker in tickers_split:
            if ticker.strip() != '':
                requests.post(url='http://127.0.0.1:5555/stocks/add', json={'ticker': ticker.strip()})
        current = self.current_stock_tickers()
        return current

    def add_items(self):
        print('Enter in the items you want to track in a comma separated list')
        items = input('Item(s):')
        items_split = items.split(',')
        for item in items_split:
            if item.strip() != '':
                requests.post(url='http://127.0.0.1:5555/tracker/add', json={'name': item.strip()})
        current = self.current_item_status()
        return current

    def current_item_status(self):
        current_enabled = []
        current_disabled = []
        all_items = requests.get(url='http://127.0.0.1:5555/tracker/select').json()
        for item in all_items:
            if item['enabled'] == 1:
                current_enabled.append(item['name'])
            else:
                current_disabled.append(item['name'])
        print(f'Currently Enabled: {current_enabled}')
        print(f'Currently Disabled: {current_disabled}')
        return {'enabled': current_enabled, 'disabled': current_disabled}

    def current_stock_tickers(self):
        print('Current Tickers:')
        current = []
        all_tickers = requests.get(url='http://127.0.0.1:5555/stocks/select').json()
        for ticker in all_tickers:
            current.append(ticker['ticker'])
        print(current)
        return current

    def run(self):
        print('What do you want to do?')
        print('\t0 : Exit')
        print('\t1 : Location')
        print('\t2 : Stocks')
        print('\t3 : Items')
        choice = input('Input: ')
        if choice == '0':
            exit()
        elif choice == '1':
            self.locations()
            self.check_state()
            self.run()
        elif choice == '2':
            self.stocks()
            self.check_state()
            self.run()
        elif choice == '3':
            self.items()
            self.check_state()
            self.run()
        else:
            print('Please select an available option')
            self.check_state()
            self.run()


if __name__ == '__main__':
    a = Setup()
