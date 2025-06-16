import pandas as pd
import numpy as np


class TimeSeriesData:

    @staticmethod
    def from_array(data_input=None, time_input=None):
        t = TimeSeriesData()
        t.dataframe = pd.DataFrame(data={"value": data_input}, index=[pd.Timestamp(x) for x in time_input])
        return t

    @staticmethod
    def from_dataframe(dataframe: pd.DataFrame):
        t = TimeSeriesData()
        t.dataframe = dataframe
        return t

    def __init__(self):
        self.dataframe = None

    def __sub__(self, other):
        return TimeSeriesData.from_dataframe(self.dataframe - other.dataframe)

    def __getitem__(self, item):
        return TimeSeriesData.from_dataframe(self.dataframe.iloc[item])

    def __len__(self):
        return len(self.dataframe)
