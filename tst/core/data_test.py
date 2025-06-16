from src.core.compute import intersection, lowest_row, highest_row, is_uptrend
from src.core.data import TimeSeriesData


def test_intersection():
    a = TimeSeriesData.from_array([1, 2, 3, 5, 6],
                                  ["2000-01-01", "2000-01-02", "2000-01-03", "2000-01-04", "2000-01-05"])
    b = TimeSeriesData.from_array([-10, -2, 3, 10, 20],
                                  ["2000-01-01", "2000-01-02", "2000-01-03", "2000-01-04", "2000-01-05"])
    assert len(intersection(a, b, "down").dataframe) > 0


def test_highest():
    a = TimeSeriesData.from_array([1, 2, 3, 5, 6],
                                  ["2000-01-01", "2000-01-02", "2000-01-03", "2000-01-04", "2000-01-05"])

    highest_row(a)


def test_last():
    a = TimeSeriesData.from_array([1, 2, 3, 5, 6],
                                  ["2000-01-01", "2000-01-02", "2000-01-03", "2000-01-04", "2000-01-05"])

    print(a[-2:].dataframe)
    print(a.dataframe.iloc[3:])
    assert len(a[-2:].dataframe) == 2


def test_get_item():
    a = TimeSeriesData.from_array([1, 2, 3, 5, 6],
                                  ["2000-01-01", "2000-01-02", "2000-01-03", "2000-01-04", "2000-01-05"])

    print(a[0].dataframe.values)


def test_is_uptrend():
    a = TimeSeriesData.from_array([1, 2, 3, 5, 6],
                                  ["2000-01-01", "2000-01-02", "2000-01-03", "2000-01-04", "2000-01-05"])

    assert is_uptrend(a) == True


def test_change_in_ratio():
    a = TimeSeriesData.from_array([1, 2, 3, 5, 6],
                                  ["2000-01-01", "2000-01-02", "2000-01-03", "2000-01-04", "2000-01-05"])

    print(a[4].dataframe - a[0].dataframe)

