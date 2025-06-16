import numpy as np

from src.core.compute import is_uptrend, moving_average, is_downtrend
from src.core.data import TimeSeriesData
from src.model.event import TechnicalAnalysisOfflineEvent_PriceTrend, TechnicalAnalysisRealtimeEvent_PriceTrend
from src.model.event_enum import EventCategory
from src.strategy.base_strategy import BaseStrategy

from datetime import datetime, timezone


class RealtimeMa20PriceUpTrendLast3(BaseStrategy):

    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_array([x for x in price_data["Close"]], [x for x in price_data.index])

        res = []
        last_period = 3
        ma20 = moving_average(t, 20)

        for i in range(last_period, len(ma20)):

            ma20_slice = ma20[:i]

            last_n = ma20_slice[-last_period:]

            if np.isnan(last_n[0].dataframe.values[0]):
                continue

            change_in_ratio = float(last_n[-1].dataframe - last_n[0].dataframe) / float(
                last_n[0].dataframe.values) * 100

            if is_uptrend(last_n) and change_in_ratio > 0.3:
                action_date = last_n[-1].dataframe.name.to_pydatetime()
                e = TechnicalAnalysisRealtimeEvent_PriceTrend.create(
                    category_name=EventCategory.TREND.value,
                    strategy_name="RealtimeMa20PriceUpTrendLast3",
                    ticker_name=ticker_name,
                    trend_type="uptrend",
                    change_in_ratio=change_in_ratio,
                    action_date=action_date.astimezone(tz=timezone.utc)
                )
                res.append(e)

        return res


class RealtimeMa20PriceDownTrendLast3(BaseStrategy):

    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]

        t = TimeSeriesData.from_array([x for x in price_data["Close"]], [x for x in price_data.index])

        res = []
        last_period = 3
        ma20 = moving_average(t, 20)

        for i in range(last_period, len(ma20)):

            ma20_slice = ma20[:i]

            last_n = ma20_slice[-last_period:]

            if np.isnan(last_n[0].dataframe.values[0]):
                continue

            change_in_ratio = float(last_n[-1].dataframe - last_n[0].dataframe) / float(
                last_n[0].dataframe.values) * 100

            if is_downtrend(last_n) and change_in_ratio < -0.3:
                action_date = last_n[-1].dataframe.name.to_pydatetime()
                e = TechnicalAnalysisRealtimeEvent_PriceTrend.create(
                    category_name=EventCategory.TREND.value,
                    strategy_name="RealtimeMa20PriceDownTrendLast3",
                    ticker_name=ticker_name,
                    trend_type="downtrend",
                    change_in_ratio=change_in_ratio,
                    action_date=action_date.astimezone(tz=timezone.utc)
                )
                res.append(e)

        return res


class RealtimeMa20PriceUpTrendLast5(BaseStrategy):

    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_array([x for x in price_data["Close"]], [x for x in price_data.index])

        res = []
        last_period = 5
        ma20 = moving_average(t, 20)

        for i in range(last_period, len(ma20)):

            ma20_slice = ma20[:i]

            last_n = ma20_slice[-last_period:]

            if np.isnan(last_n[0].dataframe.values[0]):
                continue

            change_in_ratio = float(last_n[-1].dataframe - last_n[0].dataframe) / float(
                last_n[0].dataframe.values) * 100

            if is_uptrend(last_n) and change_in_ratio > 0.5:
                action_date = last_n[-1].dataframe.name.to_pydatetime()
                e = TechnicalAnalysisRealtimeEvent_PriceTrend.create(
                    category_name=EventCategory.TREND.value,
                    strategy_name="RealtimeMa20PriceUpTrendLast5",
                    ticker_name=ticker_name,
                    trend_type="uptrend",
                    change_in_ratio=change_in_ratio,
                    action_date=action_date.astimezone(tz=timezone.utc)
                )
                res.append(e)

        return res


class RealtimeMa20PriceDownTrendLast5(BaseStrategy):

    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]

        t = TimeSeriesData.from_array([x for x in price_data["Close"]], [x for x in price_data.index])

        res = []
        last_period = 5
        ma20 = moving_average(t, 20)

        for i in range(last_period, len(ma20)):

            ma20_slice = ma20[:i]

            last_n = ma20_slice[-last_period:]

            if np.isnan(last_n[0].dataframe.values[0]):
                continue

            change_in_ratio = float(last_n[-1].dataframe - last_n[0].dataframe) / float(
                last_n[0].dataframe.values) * 100

            if is_downtrend(last_n) and change_in_ratio < -0.5:
                action_date = last_n[-1].dataframe.name.to_pydatetime()
                e = TechnicalAnalysisRealtimeEvent_PriceTrend.create(
                    category_name=EventCategory.TREND.value,
                    strategy_name="RealtimeMa20PriceDownTrendLast5",
                    ticker_name=ticker_name,
                    trend_type="downtrend",
                    change_in_ratio=change_in_ratio,
                    action_date=action_date.astimezone(tz=timezone.utc)
                )
                res.append(e)

        return res
