import json


class SecurityData:
    def __init__(self, id_name, ticker_name, publish_date, open_price, high_price, low_price, close_price, volume, dividends,
                 stock_splits, update_date):
        self.id = id_name
        self.ticker = ticker_name.upper()
        self.publish_date = publish_date
        self.open = open_price
        self.high = high_price
        self.low = low_price
        self.close = close_price
        self.volume = volume
        self.dividends = dividends
        self.stock_splits = stock_splits
        self.update_date = update_date

    def __str__(self):
        return json.dumps(self.__dict__, indent=4, sort_keys=True, default=str)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
