from src.model.event_enum import EventCategory
from src.model.event import TechnicalAnalysisRealtimeEvent_PriceChange
from src.core.data import TimeSeriesData
from src.strategy.base_strategy import BaseStrategy
from datetime import timezone

import numpy as np

from src.updater.market_symbol import forex_ticker_dict


class RealtimePriceChange(BaseStrategy):

    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_dataframe(price_data[["Open", "Close", "Volume"]])

        close_price_df = t.dataframe["Close"]
        open_price_df = t.dataframe["Open"]

        price_df = t.dataframe

        last_period = 20
        res = []

        scale = 1

        if ticker_name in forex_ticker_dict:
            scale = 10

        for i in range(last_period, len(price_df)):
            price_slice = close_price_df[i - last_period:i]
            current_price = close_price_df[i]
            idx = i
            date_index = close_price_df.index[idx].to_pydatetime().astimezone(timezone.utc)
            e = None
            change_in_ratio = round((close_price_df.iloc[i] - open_price_df.iloc[i]) / open_price_df.iloc[i] * 100, 3)

            if np.abs(change_in_ratio) > 10 / scale:
                e = TechnicalAnalysisRealtimeEvent_PriceChange.create(
                    category_name=EventCategory.PRICE.value,
                    strategy_name="RealtimePriceChange",
                    ticker_name=ticker_name,
                    trend_type=f" ExtremeChangePeriod",
                    change_in_ratio=change_in_ratio,
                    action_date=date_index,
                    price=close_price_df.iloc[idx]
                )
            elif np.abs(change_in_ratio) > 5 / scale:
                e = TechnicalAnalysisRealtimeEvent_PriceChange.create(
                    category_name=EventCategory.PRICE.value,
                    strategy_name="RealtimePriceChange",
                    ticker_name=ticker_name,
                    trend_type=f"SharpChangePeriod",
                    change_in_ratio=change_in_ratio,
                    action_date=date_index,
                    price=close_price_df.iloc[idx]
                )
            elif np.abs(change_in_ratio) > 2 / scale:
                e = TechnicalAnalysisRealtimeEvent_PriceChange.create(
                    category_name=EventCategory.PRICE.value,
                    strategy_name="RealtimePriceChange",
                    ticker_name=ticker_name,
                    trend_type=f"BigChangePeriod",
                    change_in_ratio=change_in_ratio,
                    action_date=date_index,
                    price=close_price_df.iloc[idx]
                )
            elif np.abs(change_in_ratio) > 1 / scale:
                e = TechnicalAnalysisRealtimeEvent_PriceChange.create(
                    category_name=EventCategory.PRICE.value,
                    strategy_name="RealtimePriceChange",
                    ticker_name=ticker_name,
                    trend_type=f"ChangePeriod",
                    change_in_ratio=change_in_ratio,
                    action_date=date_index,
                    price=close_price_df.iloc[idx]
                )
            if e is not None:
                res.append(e)
        return res


class RealtimePriceChangeAggregate(BaseStrategy):

    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_dataframe(price_data[["Open", "Close", "Volume"]])

        close_price_df = t.dataframe["Close"]
        price_df = t.dataframe

        scale = 1
        if ticker_name in forex_ticker_dict:
            scale = 10

        step = 4
        res = []

        for i in range(len(price_df) - 1, step, -step):
            idx = i
            date_index = close_price_df.index[idx].to_pydatetime().astimezone(timezone.utc)
            e = None
            for j in [4, 8]:
                change_in_ratio = round(
                    (close_price_df.iloc[i] - close_price_df.iloc[i - j]) / close_price_df.iloc[i - j] * 100, 3)
                strategy_name = f"RealtimePriceChangeAggregateLast{j}"
                if np.abs(change_in_ratio) > 10 / scale:
                    e = TechnicalAnalysisRealtimeEvent_PriceChange.create(
                        category_name=EventCategory.PRICE.value,
                        strategy_name=strategy_name,
                        ticker_name=ticker_name,
                        trend_type=f" ExtremeChangeLast{j}",
                        change_in_ratio=change_in_ratio,
                        action_date=date_index,
                        price=close_price_df.iloc[idx]
                    )
                elif np.abs(change_in_ratio) > 5 / scale:
                    e = TechnicalAnalysisRealtimeEvent_PriceChange.create(
                        category_name=EventCategory.PRICE.value,
                        strategy_name=strategy_name,
                        ticker_name=ticker_name,
                        trend_type=f"SharpChangeLast{j}",
                        change_in_ratio=change_in_ratio,
                        action_date=date_index,
                        price=close_price_df.iloc[idx]
                    )
                elif np.abs(change_in_ratio) > 2 / scale:
                    e = TechnicalAnalysisRealtimeEvent_PriceChange.create(
                        category_name=EventCategory.PRICE.value,
                        strategy_name=strategy_name,
                        ticker_name=ticker_name,
                        trend_type=f"BigChangeLast{j}",
                        change_in_ratio=change_in_ratio,
                        action_date=date_index,
                        price=close_price_df.iloc[idx]
                    )
                elif np.abs(change_in_ratio) > 1 / scale:
                    e = TechnicalAnalysisRealtimeEvent_PriceChange.create(
                        category_name=EventCategory.PRICE.value,
                        strategy_name=strategy_name,
                        ticker_name=ticker_name,
                        trend_type=f"ChangeLast{j}",
                        change_in_ratio=change_in_ratio,
                        action_date=date_index,
                        price=close_price_df.iloc[idx]
                    )
                if e is not None:
                    res.append(e)
        return res
