from src.realtime_strategy.volume_strategy import RealtimeVolumeIncrease
from src.util.dao_util import get_realtime_strategy_data_config
from src.updater.security_data_updater import parse_history


def test():
    data = get_realtime_strategy_data_config("KE=F", "5d", "1h")

    strategy = RealtimeVolumeIncrease(
        data=data
    )

    strategy.execute_strategy()


