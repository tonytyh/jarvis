from enum import Enum


class EventCategory(Enum):
    TREND = "Trend"
    VOLUME = "Volume"
    PRICE = "Price"
    MOVING_AVERAGE = "MovingAverage"
    OSCILLATOR = "Oscillator"

