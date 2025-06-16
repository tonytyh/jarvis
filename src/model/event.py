import uuid
from datetime import datetime, timezone
import json


class Event:

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.event_data = None
        self.event_category = None
        self.event_type = None
        self.event_name = None
        self.event_date = None
        self.update_date = None

    def __str__(self):
        return json.dumps(self.__dict__, indent=4, sort_keys=True, default=str)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class TechnicalAnalysisOfflineEvent_BuyAndSell(Event):

    @staticmethod
    def create(category_name: str, strategy_name: str, ticker_name: str, price: float, action_item: str, indicator: str,
               indicator_value: float,
               action_date: datetime) -> Event:
        e = TechnicalAnalysisOfflineEvent_BuyAndSell()
        e.event_category = category_name
        e.event_type = f"{action_date.strftime('%Y-%m-%d')}_{strategy_name}_{ticker_name}"
        e.event_item = f"{ticker_name}"
        e.event_date = int(action_date.timestamp() * 1000)
        e.event_name = f"[{ticker_name}][{action_date.strftime('%Y-%m-%d')}][{category_name}][{strategy_name}] {action_item} the {ticker_name} at price {price}"
        e.event_data = json.dumps({
            "strategy_name": strategy_name,
            "ticker": ticker_name,
            "price": price,
            "indicator": indicator,
            "indicator_value": indicator_value,
            "action_item": action_item,
            "action_date": int(action_date.timestamp() * 1000)
        })
        e.update_date = int(datetime.now().timestamp() * 1000)
        return e


class TechnicalAnalysisOfflineEvent_PriceTrend(Event):
    @staticmethod
    def create(category_name: str, strategy_name: str, ticker_name: str, trend_type: str, change_in_ratio: float,
               action_date: datetime) -> Event:
        e = TechnicalAnalysisOfflineEvent_PriceTrend()
        e.event_category = category_name
        e.event_type = f"{action_date.strftime('%Y-%m-%d')}_{strategy_name}_{ticker_name}"
        e.event_item = f"{ticker_name}"
        e.event_date = int(action_date.timestamp() * 1000)
        e.event_name = f"[{ticker_name}][{action_date.strftime('%Y-%m-%d')}][{category_name}][{strategy_name}] {ticker_name} is at the {trend_type.upper()} trend, and the change ratio is {change_in_ratio} % "

        e.event_data = json.dumps({
            "strategy_name": strategy_name,
            "ticker": ticker_name,
            "indicator": "TREND",
            "indicator_value": change_in_ratio,
            "change_in_ratio": change_in_ratio,
            "trend_type": trend_type,
            "action_date": int(action_date.timestamp() * 1000)
        })
        e.update_date = int(datetime.now().timestamp() * 1000)
        return e


class TechnicalAnalysisOfflineEvent_OverSoldAndBought(Event):
    @staticmethod
    def create(category_name: str, strategy_name: str, ticker_name: str, action_item: str, indicator: str,
               indicator_value: float,
               action_date: datetime) -> Event:
        e = TechnicalAnalysisOfflineEvent_PriceTrend()
        e.event_category = category_name
        e.event_type = f"{action_date.strftime('%Y-%m-%d')}_{strategy_name}_{ticker_name}"
        e.event_item = f"{ticker_name}"
        e.event_date = int(action_date.timestamp() * 1000)
        e.event_name = f"[{ticker_name}][{action_date.strftime('%Y-%m-%d')}][{category_name}][{strategy_name}] " \
                       f"{ticker_name} is {action_item.upper()}. The {indicator} value is {indicator_value}"

        e.event_data = json.dumps({
            "strategy_name": strategy_name,
            "ticker": ticker_name,
            "indicator": indicator,
            "indicator_value": indicator_value,
            "action_item": action_item,
            "action_date": int(action_date.timestamp() * 1000)
        })
        e.update_date = int(datetime.now().timestamp() * 1000)
        return e


class TechnicalAnalysisRealtimeEvent_PriceTrend(Event):
    @staticmethod
    def create(category_name: str, strategy_name: str, ticker_name: str, trend_type: str, change_in_ratio: float,
               action_date: datetime) -> Event:
        e = TechnicalAnalysisRealtimeEvent_PriceTrend()
        e.event_category = category_name
        e.event_type = f"{action_date.strftime('%Y-%m-%d-%H')}_{strategy_name}_{ticker_name}"
        e.event_item = f"{ticker_name}"
        e.event_date = int(action_date.timestamp() * 1000)
        e.event_name = f"[{ticker_name}][{action_date.strftime('%Y-%m-%d-%H')}][{category_name}][{strategy_name}] {ticker_name} is at the {trend_type.upper()} trend, and the change ratio is {round(change_in_ratio, 3)} % "

        e.event_data = json.dumps({
            "strategy_name": strategy_name,
            "ticker": ticker_name,
            "change_in_ratio": change_in_ratio,
            "trend_type": trend_type,
            "action_date": int(action_date.timestamp() * 1000)
        })
        e.update_date = int(datetime.now().timestamp() * 1000)
        return e


class TechnicalAnalysisRealtimeEvent_VolumeChange(Event):
    @staticmethod
    def create(category_name: str, strategy_name: str, ticker_name: str, trend_type: str, volume: int, price: float,
               action_date: datetime) -> Event:
        e = TechnicalAnalysisRealtimeEvent_VolumeChange()
        e.event_category = category_name
        e.event_type = f"{action_date.strftime('%Y-%m-%d-%H')}_{strategy_name}_{ticker_name}"
        e.event_item = f"{ticker_name}"
        e.event_date = int(action_date.timestamp() * 1000)
        e.event_name = f"[{ticker_name}][{action_date.strftime('%Y-%m-%d-%H')}][{category_name}][{strategy_name}] {ticker_name}'s volume is {trend_type.upper()} "

        e.event_data = json.dumps({
            "strategy_name": strategy_name,
            "ticker": ticker_name,
            "trend_type": trend_type,
            "price": price,
            "volume": int(volume),
            "action_date": int(action_date.timestamp() * 1000)
        })
        e.update_date = int(datetime.now().timestamp() * 1000)
        return e


class TechnicalAnalysisRealtimeEvent_PriceChange(Event):
    @staticmethod
    def create(category_name: str, strategy_name: str, ticker_name: str, trend_type: str, change_in_ratio: int,
               price: float,
               action_date: datetime) -> Event:
        e = TechnicalAnalysisRealtimeEvent_VolumeChange()
        e.event_category = category_name
        e.event_type = f"{action_date.strftime('%Y-%m-%d-%H')}_{strategy_name}_{ticker_name}"
        e.event_item = f"{ticker_name}"
        e.event_date = int(action_date.timestamp() * 1000)
        e.event_name = f"[{ticker_name}][{action_date.strftime('%Y-%m-%d-%H')}][{category_name}][{strategy_name}] {ticker_name}'s Change is {trend_type.upper()} "

        e.event_data = json.dumps({
            "strategy_name": strategy_name,
            "ticker": ticker_name,
            "trend_type": trend_type,
            "price": price,
            "change_in_ratio": change_in_ratio,
            "action_date": int(action_date.timestamp() * 1000)
        })
        e.update_date = int(datetime.now().timestamp() * 1000)
        return e
