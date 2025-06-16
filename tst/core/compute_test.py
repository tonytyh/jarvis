from src.core.compute import relative_index
from src.core.data import TimeSeriesData


def test_intersection():
    a = TimeSeriesData.from_array([1, 2, 3, 5, 3],
                                  ["2000-01-01", "2000-01-02", "2000-01-03", "2000-01-04", "2000-01-05"])


    relative_index(a,window_size=10)

