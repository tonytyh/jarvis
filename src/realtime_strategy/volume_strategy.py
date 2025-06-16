from src.model.event_enum import EventCategory
from src.model.event import TechnicalAnalysisRealtimeEvent_VolumeChange
from src.core.data import TimeSeriesData
from src.strategy.base_strategy import BaseStrategy
from datetime import timezone

import numpy as np


class RealtimeVolumeIncrease(BaseStrategy):

    def execute_strategy(self):
        volume_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_dataframe(volume_data[["Open","Close", "Volume"]])

        volume_df = t.dataframe["Volume"]
        close_price_df = t.dataframe["Close"]
        open_price_df = t.dataframe["Open"]

        last_period = 24
        res = []

        for i in range(last_period, len(volume_df)):
            volume_slice = volume_df[i - last_period:i]
            current_vol = volume_df[i]
            idx = i
            date_index = volume_df.index[idx].to_pydatetime().astimezone(timezone.utc)
            e = None

            direction = None
            if open_price_df.iloc[i] < close_price_df.iloc[i]:
                direction = "Buy"
            else:
                direction = "Sell"

            if (current_vol - np.mean(volume_slice) / np.mean(volume_slice)) * 100 > 20:
                e = TechnicalAnalysisRealtimeEvent_VolumeChange.create(
                    category_name=EventCategory.VOLUME.value,
                    strategy_name="RealtimeVolumeIncrease",
                    ticker_name=ticker_name,
                    trend_type=f"{direction}ExtremeIncrease",
                    volume=volume_df.iloc[idx],
                    action_date=date_index,
                    price=close_price_df.iloc[idx]
                )
            elif (current_vol - np.mean(volume_slice) / np.mean(volume_slice)) * 100 > 10:
                e = TechnicalAnalysisRealtimeEvent_VolumeChange.create(
                    category_name=EventCategory.VOLUME.value,
                    strategy_name="RealtimeVolumeIncrease",
                    ticker_name=ticker_name,
                    trend_type=f"{direction}SharpIncrease",
                    volume=volume_df.iloc[idx],
                    action_date=date_index,
                    price=close_price_df.iloc[idx]
                )
            elif (current_vol - np.mean(volume_slice) / np.mean(volume_slice)) * 100 > 5:
                e = TechnicalAnalysisRealtimeEvent_VolumeChange.create(
                    category_name=EventCategory.VOLUME.value,
                    strategy_name="RealtimeVolumeIncrease",
                    ticker_name=ticker_name,
                    trend_type=f"{direction}BigIncrease",
                    volume=volume_df.iloc[idx],
                    action_date=date_index,
                    price=close_price_df.iloc[idx]
                )
            elif (current_vol - np.mean(volume_slice) / np.mean(volume_slice)) * 100 > 1:
                e = TechnicalAnalysisRealtimeEvent_VolumeChange.create(
                    category_name=EventCategory.VOLUME.value,
                    strategy_name="RealtimeVolumeIncrease",
                    ticker_name=ticker_name,
                    trend_type=f"{direction}Increase",
                    volume=volume_df.iloc[idx],
                    action_date=date_index,
                    price=close_price_df.iloc[idx]
                )
            if e is not None:
                res.append(e)
        return res
