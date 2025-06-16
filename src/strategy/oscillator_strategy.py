from src.model.event import TechnicalAnalysisOfflineEvent_BuyAndSell, TechnicalAnalysisOfflineEvent_OverSoldAndBought
from src.core.data import TimeSeriesData
from src.strategy.base_strategy import BaseStrategy
from src.core.oscillator import moving_average_convergence_divergence, relative_strength_index
from src.core.compute import intersection
from src.model.event_enum import EventCategory


class MacdBuy(BaseStrategy):

    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_array([x["close"] for x in price_data], [x["publish_date"] for x in price_data])

        fast_macd, slow_macd, macd_diff = moving_average_convergence_divergence(t)

        signal = intersection(fast_macd, slow_macd, "up")

        res = []

        for date_index in signal.dataframe.index:
            price_level = float(t.dataframe.loc[date_index]["value"])
            e = TechnicalAnalysisOfflineEvent_BuyAndSell.create(
                category_name=EventCategory.OSCILLATOR.value,
                strategy_name="MacdBuy",
                ticker_name=ticker_name,
                indicator="MACD",
                indicator_value=fast_macd.dataframe.loc[date_index]["value"],
                price=price_level,
                action_item="Buy",
                action_date=date_index
            )
            res.append(e)

        return res


class MacdSell(BaseStrategy):

    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_array([x["close"] for x in price_data], [x["publish_date"] for x in price_data])

        fast_macd, slow_macd, macd_diff = moving_average_convergence_divergence(t)

        signal = intersection(fast_macd, slow_macd, "down")

        res = []

        for date_index in signal.dataframe.index:
            price_level = float(t.dataframe.loc[date_index]["value"])
            e = TechnicalAnalysisOfflineEvent_BuyAndSell.create(
                category_name=EventCategory.OSCILLATOR.value,
                strategy_name="MacdSell",
                ticker_name=ticker_name,
                indicator="MACD",
                indicator_value=fast_macd.dataframe.loc[date_index]["value"],
                price=price_level,
                action_item="Sell",
                action_date=date_index
            )
            res.append(e)

        return res


class Rsi6OverSold(BaseStrategy):
    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_array([x["close"] for x in price_data], [x["publish_date"] for x in price_data])

        rsi_time_series_data = relative_strength_index(t, 6)

        rsi_df = rsi_time_series_data.dataframe

        signal = TimeSeriesData.from_dataframe(rsi_df[rsi_df.values < 20])

        res = []

        for date_index in signal.dataframe.index:
            indicator_value = float(signal.dataframe.loc[date_index])
            e = TechnicalAnalysisOfflineEvent_OverSoldAndBought.create(
                category_name=EventCategory.OSCILLATOR.value,
                strategy_name="Rsi6OverSold",
                ticker_name=ticker_name,
                indicator="RSI6",
                indicator_value=indicator_value,
                action_item="Oversold",
                action_date=date_index
            )
            res.append(e)

        return res


class Rsi6OverBought(BaseStrategy):
    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_array([x["close"] for x in price_data], [x["publish_date"] for x in price_data])

        rsi_time_series_data = relative_strength_index(t, 6)

        rsi_df = rsi_time_series_data.dataframe

        signal = TimeSeriesData.from_dataframe(rsi_df[rsi_df.values > 80])

        res = []

        for date_index in signal.dataframe.index:
            indicator_value = float(signal.dataframe.loc[date_index])
            e = TechnicalAnalysisOfflineEvent_OverSoldAndBought.create(
                category_name=EventCategory.OSCILLATOR.value,
                strategy_name="Rsi6OverBought",
                ticker_name=ticker_name,
                indicator="RSI6",
                indicator_value=indicator_value,
                action_item="Overbought",
                action_date=date_index
            )
            res.append(e)

        return res
