sh "./stop_all_script.sh"

python auto_security_updater.py --mode auto&
python auto_intraday_strategy_starter.py --mode auto&
python auto_report_starter.py --mode auto&
python auto_strategy_starter.py --mode auto&
