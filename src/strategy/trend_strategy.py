from src.core.compute import moving_average, is_downtrend, is_uptrend
from src.core.data import TimeSeriesData
from src.model.event import TechnicalAnalysisOfflineEvent_PriceTrend
from src.model.event_enum import EventCategory
from src.strategy.base_strategy import BaseStrategy

import numpy as np


class Ma10PriceUpTrendLast5(BaseStrategy):

    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_array([x["close"] for x in price_data], [x["publish_date"] for x in price_data])

        res = []
        last_day = 5
        ma10 = moving_average(t, 10)

        for i in range(last_day, len(ma10)):

            ma10_slice = ma10[:i]

            last_n = ma10_slice[-last_day:]

            if np.isnan(last_n[0].dataframe.values[0]):
                continue

            change_in_ratio = float(last_n[-1].dataframe - last_n[0].dataframe) / float(
                last_n[0].dataframe.values) * 100

            if is_uptrend(last_n) and change_in_ratio > 1.0:
                e = TechnicalAnalysisOfflineEvent_PriceTrend.create(
                    category_name=EventCategory.TREND.value,
                    strategy_name="Ma10PriceUpTrendLast5",
                    ticker_name=ticker_name,
                    trend_type="Uptrend",
                    change_in_ratio=change_in_ratio,
                    action_date=last_n[-1].dataframe.name.to_pydatetime()
                )
                res.append(e)

        return res


class Ma20PriceUpTrendLast7(BaseStrategy):

    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_array([x["close"] for x in price_data], [x["publish_date"] for x in price_data])

        res = []
        last_day = 7
        ma20 = moving_average(t, 20)

        for i in range(last_day, len(ma20)):

            ma20_slice = ma20[:i]

            last_n = ma20_slice[-last_day:]

            if np.isnan(last_n[0].dataframe.values[0]):
                continue

            change_in_ratio = float(last_n[-1].dataframe - last_n[0].dataframe) / float(
                last_n[0].dataframe.values) * 100

            if is_uptrend(last_n) and change_in_ratio > 1.0:
                e = TechnicalAnalysisOfflineEvent_PriceTrend.create(
                    category_name=EventCategory.TREND.value,
                    strategy_name="Ma20PriceUpTrendLast7",
                    ticker_name=ticker_name,
                    trend_type="Uptrend",
                    change_in_ratio=change_in_ratio,
                    action_date=last_n[-1].dataframe.name.to_pydatetime()
                )
                res.append(e)

        return res


class Ma10PriceDownTrendLast5(BaseStrategy):

    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_array([x["close"] for x in price_data], [x["publish_date"] for x in price_data])

        res = []
        last_day = 5
        ma10 = moving_average(t, 10)

        for i in range(last_day, len(ma10)):

            ma10_slice = ma10[:i]

            last_n = ma10_slice[-last_day:]

            if np.isnan(last_n[0].dataframe.values[0]):
                continue

            change_in_ratio = float(last_n[-1].dataframe - last_n[0].dataframe) / float(
                last_n[0].dataframe.values) * 100

            if is_downtrend(last_n) and change_in_ratio < -1.0:
                e = TechnicalAnalysisOfflineEvent_PriceTrend.create(
                    category_name=EventCategory.TREND.value,
                    strategy_name="Ma10PriceDownTrendLast5",
                    ticker_name=ticker_name,
                    trend_type="Downtrend",
                    change_in_ratio=change_in_ratio,
                    action_date=last_n[-1].dataframe.name.to_pydatetime()
                )
                res.append(e)

        return res


class Ma20PriceDownTrendLast7(BaseStrategy):

    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_array([x["close"] for x in price_data], [x["publish_date"] for x in price_data])

        res = []
        last_day = 7
        ma20 = moving_average(t, 20)

        for i in range(last_day, len(ma20)):

            ma20_slice = ma20[:i]

            last_n = ma20_slice[-last_day:]

            if np.isnan(last_n[0].dataframe.values[0]):
                continue

            change_in_ratio = float(last_n[-1].dataframe - last_n[0].dataframe) / float(
                last_n[0].dataframe.values) * 100

            if is_downtrend(last_n) and change_in_ratio < -1.0:
                e = TechnicalAnalysisOfflineEvent_PriceTrend.create(
                    category_name=EventCategory.TREND.value,
                    strategy_name="Ma20PriceDownTrendLast7",
                    ticker_name=ticker_name,
                    trend_type="Downtrend",
                    change_in_ratio=change_in_ratio,
                    action_date=last_n[-1].dataframe.name.to_pydatetime()
                )
                res.append(e)

        return res


class Ma5PriceUpTrendLast3(BaseStrategy):

    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_array([x["close"] for x in price_data], [x["publish_date"] for x in price_data])

        res = []
        last_day = 3
        ma5 = moving_average(t, 5)

        for i in range(last_day, len(ma5)):

            ma5_slice = ma5[:i]

            last_n = ma5_slice[-last_day:]

            if np.isnan(last_n[0].dataframe.values[0]):
                continue

            change_in_ratio = float(last_n[-1].dataframe - last_n[0].dataframe) / float(
                last_n[0].dataframe.values) * 100

            if is_uptrend(last_n) and change_in_ratio > 0.5:
                e = TechnicalAnalysisOfflineEvent_PriceTrend.create(
                    category_name=EventCategory.TREND.value,
                    strategy_name="Ma5PriceUpTrendLast3",
                    ticker_name=ticker_name,
                    trend_type="Uptrend",
                    change_in_ratio=change_in_ratio,
                    action_date=last_n[-1].dataframe.name.to_pydatetime()
                )
                res.append(e)

        return res


class Ma5PriceDownTrendLast3(BaseStrategy):

    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_array([x["close"] for x in price_data], [x["publish_date"] for x in price_data])

        res = []
        last_day = 3
        ma5 = moving_average(t, 5)

        for i in range(last_day, len(ma5)):

            ma5_slice = ma5[:i]

            last_n = ma5_slice[-last_day:]

            if np.isnan(last_n[0].dataframe.values[0]):
                continue

            change_in_ratio = float(last_n[-1].dataframe - last_n[0].dataframe) / float(
                last_n[0].dataframe.values) * 100

            if is_downtrend(last_n) and change_in_ratio < -0.5:
                e = TechnicalAnalysisOfflineEvent_PriceTrend.create(
                    category_name=EventCategory.TREND.value,
                    strategy_name="Ma5PriceDownTrendLast3",
                    ticker_name=ticker_name,
                    trend_type="Downtrend",
                    change_in_ratio=change_in_ratio,
                    action_date=last_n[-1].dataframe.name.to_pydatetime()
                )
                res.append(e)

        return res


class MaPriceStrongUptrend(BaseStrategy):
    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_array([x["close"] for x in price_data], [x["publish_date"] for x in price_data])
        ma_dict = {}

        last_day = 3

        ma_len = [5, 10, 20, 60, 120]
        ma_dict[5] = moving_average(t, 5)
        ma_dict[10] = moving_average(t, 10)
        ma_dict[20] = moving_average(t, 20)
        ma_dict[60] = moving_average(t, 60)

        res = []

        for i in range(0, len(ma_len) - 3):
            for j in range(i + 1, len(ma_len) - 2):
                for k in range(j + 1, len(ma_len) - 1):
                    ma_a = ma_dict[ma_len[i]]
                    ma_b = ma_dict[ma_len[j]]
                    ma_c = ma_dict[ma_len[k]]

                    ma_a_df = ma_a.dataframe.loc[ma_c.dataframe.index]
                    ma_b_df = ma_b.dataframe.loc[ma_c.dataframe.index]
                    ma_c_df = ma_c.dataframe.loc[ma_c.dataframe.index]

                    ma_a_b_df_diff = ma_a_df - ma_b_df
                    ma_b_c_df_diff = ma_b_df - ma_c_df

                    for p in range(0, len(ma_a_b_df_diff) - last_day):

                        if np.isnan(ma_a_b_df_diff.iloc[p].value) or np.isnan(ma_b_c_df_diff.iloc[p].value):
                            continue

                        if is_uptrend(TimeSeriesData.from_dataframe(ma_a_b_df_diff[p:p + last_day])) and \
                                is_uptrend(TimeSeriesData.from_dataframe(ma_b_c_df_diff[p:p + last_day])) and \
                                (ma_a_b_df_diff[p:p + last_day] > 0).all().value and (
                                ma_b_c_df_diff[p:p + last_day] > 0).all().value:
                            date_index = ma_a_b_df_diff.index[p + last_day]
                            price_level = t.dataframe.loc[date_index]["value"]
                            last_n = ma_b_df[p:p + last_day]
                            change_in_ratio = float(last_n.iloc[-1].value - last_n.iloc[0].value) / float(
                                last_n.iloc[0].value) * 100

                            e = TechnicalAnalysisOfflineEvent_PriceTrend.create(
                                category_name=EventCategory.TREND.value,
                                strategy_name=f"MA{ma_len[i]}MA{ma_len[j]}MA{ma_len[k]}StrongUptrendLast{last_day}",
                                ticker_name=ticker_name,
                                trend_type="StrongUptrend",
                                change_in_ratio=change_in_ratio,
                                action_date=date_index
                            )
                            res.append(e)

        return res


class MaPriceStrongDownTrend(BaseStrategy):
    def execute_strategy(self):
        price_data = self.raw_data["data"]
        ticker_name = self.raw_data["name"]
        t = TimeSeriesData.from_array([x["close"] for x in price_data], [x["publish_date"] for x in price_data])
        ma_dict = {}

        last_day = 3

        ma_len = [5, 10, 20, 60]
        ma_dict[5] = moving_average(t, 5)
        ma_dict[10] = moving_average(t, 10)
        ma_dict[20] = moving_average(t, 20)
        ma_dict[60] = moving_average(t, 60)

        res = []

        for i in range(0, len(ma_len) - 3):
            for j in range(i + 1, len(ma_len) - 2):
                for k in range(j + 1, len(ma_len) - 1):
                    ma_a = ma_dict[ma_len[i]]
                    ma_b = ma_dict[ma_len[j]]
                    ma_c = ma_dict[ma_len[k]]

                    ma_a_df = ma_a.dataframe.loc[ma_c.dataframe.index]
                    ma_b_df = ma_b.dataframe.loc[ma_c.dataframe.index]
                    ma_c_df = ma_c.dataframe.loc[ma_c.dataframe.index]

                    ma_a_b_df_diff = ma_a_df - ma_b_df
                    ma_b_c_df_diff = ma_b_df - ma_c_df

                    for p in range(0, len(ma_a_b_df_diff) - last_day):

                        if np.isnan(ma_a_b_df_diff.iloc[p].value) or np.isnan(ma_b_c_df_diff.iloc[p].value):
                            continue

                        if is_downtrend(TimeSeriesData.from_dataframe(ma_a_b_df_diff[p:p + last_day])) and \
                                is_downtrend(TimeSeriesData.from_dataframe(ma_b_c_df_diff[p:p + last_day])) and \
                                (ma_a_b_df_diff[p:p + last_day] < 0).all().value and (
                                ma_b_c_df_diff[p:p + last_day] < 0).all().value:
                            date_index = ma_a_b_df_diff.index[p + last_day]
                            price_level = t.dataframe.loc[date_index]["value"]
                            last_n = ma_b_df[p:p + last_day]
                            change_in_ratio = float(last_n.iloc[-1].value - last_n.iloc[0].value) / float(
                                last_n.iloc[0].value) * 100
                            e = TechnicalAnalysisOfflineEvent_PriceTrend.create(
                                category_name=EventCategory.TREND.value,
                                strategy_name=f"MA{ma_len[i]}MA{ma_len[j]}MA{ma_len[k]}StrongDowntrendLast{last_day}",
                                ticker_name=ticker_name,
                                trend_type="StrongDowntrend",
                                change_in_ratio=change_in_ratio,
                                action_date=date_index
                            )
                            res.append(e)

        return res
