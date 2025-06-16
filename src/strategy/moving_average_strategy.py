from src.core.compute import intersection, is_uptrend, is_downtrend, moving_average
from src.core.data import TimeSeriesData
from src.strategy.base_strategy import BaseStrategy
from src.model.event import TechnicalAnalysisOfflineEvent_BuyAndSell
from src.model.event_enum import EventCategory

import numpy as np


class Ma20Ma60Buy(BaseStrategy):

    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_array([x["close"] for x in price_data], [x["publish_date"] for x in price_data])

        ma20 = moving_average(t, 20)
        ma60 = moving_average(t, 60)

        buy_intersections = intersection(ma20, ma60, "up")
        buy_df = buy_intersections.dataframe

        res = []
        for date_index in buy_df.index:
            price_level = buy_df.loc[date_index]["value"]
            e = TechnicalAnalysisOfflineEvent_BuyAndSell.create(
                category_name=EventCategory.MOVING_AVERAGE.value,
                strategy_name="Ma20Ma60Buy",
                ticker_name=ticker_name,
                indicator="MA20MA60",
                indicator_value=ma20.dataframe.loc[date_index]["value"],
                price=price_level,
                action_item="Buy",
                action_date=date_index
            )
            res.append(e)
        return res


class Ma20Ma60Sell(BaseStrategy):

    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_array([x["close"] for x in price_data], [x["publish_date"] for x in price_data])

        ma20 = moving_average(t, 20)
        ma60 = moving_average(t, 60)

        sell_intersections = intersection(ma20, ma60, "down")
        sell_df = sell_intersections.dataframe

        res = []
        for date_index in sell_df.index:
            price_level = sell_df.loc[date_index]["value"]
            e = TechnicalAnalysisOfflineEvent_BuyAndSell.create(
                category_name=EventCategory.MOVING_AVERAGE.value,
                strategy_name="Ma20Ma60Sell",
                ticker_name=ticker_name,
                indicator="MA20MA60",
                indicator_value=ma20.dataframe.loc[date_index]["value"],
                price=price_level,
                action_item="Sell",
                action_date=date_index
            )
            res.append(e)

        return res


class Ma5Ma20Buy(BaseStrategy):

    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_array([x["close"] for x in price_data], [x["publish_date"] for x in price_data])

        ma5 = moving_average(t, 5)
        ma20 = moving_average(t, 20)

        buy_intersections = intersection(ma5, ma20, "up")
        buy_df = buy_intersections.dataframe

        res = []
        for date_index in buy_df.index:
            price_level = buy_df.loc[date_index]["value"]
            e = TechnicalAnalysisOfflineEvent_BuyAndSell.create(
                category_name=EventCategory.MOVING_AVERAGE.value,
                strategy_name="Ma5Ma20Buy",
                ticker_name=ticker_name,
                indicator="MA5MA20",
                indicator_value=ma20.dataframe.loc[date_index]["value"],
                price=price_level,
                action_item="Buy",
                action_date=date_index
            )
            res.append(e)
        return res


class Ma5Ma20Sell(BaseStrategy):

    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_array([x["close"] for x in price_data], [x["publish_date"] for x in price_data])

        ma5 = moving_average(t, 5)
        ma20 = moving_average(t, 20)

        sell_intersections = intersection(ma5, ma20, "down")
        sell_df = sell_intersections.dataframe

        res = []
        for date_index in sell_df.index:
            price_level = sell_df.loc[date_index]["value"]
            e = TechnicalAnalysisOfflineEvent_BuyAndSell.create(
                category_name=EventCategory.MOVING_AVERAGE.value,
                strategy_name="Ma5Ma20Sell",
                ticker_name=ticker_name,
                indicator="MA5MA20",
                indicator_value=ma20.dataframe.loc[date_index]["value"],
                price=price_level,
                action_item="Sell",
                action_date=date_index
            )
            res.append(e)

        return res


class Ma10Ma20Buy(BaseStrategy):

    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_array([x["close"] for x in price_data], [x["publish_date"] for x in price_data])

        ma10 = moving_average(t, 10)
        ma20 = moving_average(t, 20)

        buy_intersections = intersection(ma10, ma20, "up")
        buy_df = buy_intersections.dataframe

        res = []
        for date_index in buy_df.index:
            price_level = buy_df.loc[date_index]["value"]
            e = TechnicalAnalysisOfflineEvent_BuyAndSell.create(
                category_name=EventCategory.MOVING_AVERAGE.value,
                strategy_name="Ma10Ma20Buy",
                ticker_name=ticker_name,
                indicator="MA10MA20",
                indicator_value=ma20.dataframe.loc[date_index]["value"],
                price=price_level,
                action_item="Buy",
                action_date=date_index
            )
            res.append(e)
        return res


class Ma10Ma20Sell(BaseStrategy):

    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_array([x["close"] for x in price_data], [x["publish_date"] for x in price_data])

        ma10 = moving_average(t, 10)
        ma20 = moving_average(t, 20)

        sell_intersections = intersection(ma10, ma20, "down")
        sell_df = sell_intersections.dataframe

        res = []
        for date_index in sell_df.index:
            price_level = sell_df.loc[date_index]["value"]
            e = TechnicalAnalysisOfflineEvent_BuyAndSell.create(
                category_name=EventCategory.MOVING_AVERAGE.value,
                strategy_name="Ma10Ma20Sell",
                ticker_name=ticker_name,
                indicator="MA10MA20",
                indicator_value=ma20.dataframe.loc[date_index]["value"],
                price=price_level,
                action_item="Sell",
                action_date=date_index
            )
            res.append(e)

        return res


class Ma5Ma10Buy(BaseStrategy):

    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_array([x["close"] for x in price_data], [x["publish_date"] for x in price_data])

        ma5 = moving_average(t, 5)
        ma10 = moving_average(t, 10)

        buy_intersections = intersection(ma5, ma10, "up")
        buy_df = buy_intersections.dataframe

        res = []
        for date_index in buy_df.index:
            price_level = buy_df.loc[date_index]["value"]
            e = TechnicalAnalysisOfflineEvent_BuyAndSell.create(
                category_name=EventCategory.MOVING_AVERAGE.value,
                strategy_name="Ma5Ma10Buy",
                ticker_name=ticker_name,
                indicator="MA5MA10",
                indicator_value=ma10.dataframe.loc[date_index]["value"],
                price=price_level,
                action_item="Buy",
                action_date=date_index
            )
            res.append(e)
        return res


class Ma5Ma10Sell(BaseStrategy):

    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_array([x["close"] for x in price_data], [x["publish_date"] for x in price_data])

        ma5 = moving_average(t, 5)
        ma10 = moving_average(t, 10)

        sell_intersections = intersection(ma5, ma10, "down")
        sell_df = sell_intersections.dataframe

        res = []
        for date_index in sell_df.index:
            price_level = sell_df.loc[date_index]["value"]
            e = TechnicalAnalysisOfflineEvent_BuyAndSell.create(
                category_name=EventCategory.MOVING_AVERAGE.value,
                strategy_name="Ma5Ma10Sell",
                ticker_name=ticker_name,
                indicator="MA5MA10",
                indicator_value=ma10.dataframe.loc[date_index]["value"],
                price=price_level,
                action_item="Sell",
                action_date=date_index
            )
            res.append(e)

        return res


