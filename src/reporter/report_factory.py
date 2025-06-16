import json
from datetime import datetime, timezone

from jinja2 import FileSystemLoader, Environment

import pandas as pd

from src.model.event import Event


class GeneralPerformanceReport:

    def __init__(self, df: pd.DataFrame, title: str):
        self.df = df
        self.title = title

    def render(self):

        data = []

        table_header = ["Ticker"]

        for ts in self.df.columns:
            table_header.append(ts.strftime('%m-%d'))

        for idx in self.df.index:
            item = {
                "name": idx,
                "value": self.df.loc[idx].values
            }
            data.append(item)
        env = Environment(loader=FileSystemLoader("./src/reporter/templates/"))
        template = env.get_template("performance_report_grading.html")
        out = template.render(data=data, table_header=table_header, title=self.title, update_date=datetime.now())
        return out


class LongTermPerformanceReport:

    def __init__(self, df: pd.DataFrame, title: str):
        self.df = df
        self.title = title

    def render(self):

        data = []

        table_header = []

        for ts in self.df.columns:
            table_header.append(ts.strftime('%Y-%m-%d'))

        for idx in self.df.index:
            item = {
                "symbol": idx,
                "1d": round(self.df.loc[idx].values[0], 2),
                "5d": round(self.df.loc[idx].values[1], 2),
                "10d": round(self.df.loc[idx].values[2], 2),
                "20d": round(self.df.loc[idx].values[3], 2),
                "60d": round(self.df.loc[idx].values[4], 2),
                "120d": round(self.df.loc[idx].values[5], 2),
                "250d": round(self.df.loc[idx].values[6], 2),
            }
            data.append(item)
        env = Environment(loader=FileSystemLoader("./src/reporter/templates/"))
        template = env.get_template("long_term_performance_report_grading.html")
        out = template.render(data=data, table_header=table_header, title=self.title, update_date=datetime.now())
        return out


class TechnicalPerformanceReport:
    def __init__(self, df: pd.DataFrame, title: str):
        self.df = df
        self.title = title

    def render(self):
        env = Environment(loader=FileSystemLoader("./src/reporter/templates/"))
        template = env.get_template("technical_performance_report.html")
        current_date = datetime.now().astimezone(timezone.utc)
        data = []
        for idx in self.df.index:
            e = self.df.loc[idx]
            item = {
                "ticker": e["ticker"],
                "indicator_value": round(e["indicator_value"], 2),
                "indicator": e["indicator"],
                "price": round(e["price"], 2),
                "action_item": e["action_item"],
                "action_date": e["action_date"].strftime(
                    "%Y-%m-%d")
            }
            data.append(item)

        out = template.render(data=data, title=self.title, update_date=current_date)
        return out


class TrendPerformanceReport:
    def __init__(self, df: pd.DataFrame, title: str):
        self.df = df
        self.title = title

    def render(self):
        env = Environment(loader=FileSystemLoader("./src/reporter/templates/"))
        template = env.get_template("trend_performance_report.html")
        current_date = datetime.now().astimezone(timezone.utc)
        data = []
        for idx in self.df.index:
            e = self.df.loc[idx]
            item = {
                "ticker": e["ticker"],
                "change_in_ratio": round(e["change_in_ratio"], 2),
                "trend_type": e["trend_type"],
                "strategy_name": e["strategy_name"],
                "action_date": e["action_date"].strftime(
                    "%Y-%m-%d")
            }
            data.append(item)

        out = template.render(data=data, title=self.title, update_date=current_date)
        return out


class TrendEventReport:
    def __init__(self, subject, event_list, ):
        self.subject = subject
        self.event_list = event_list

    def _convert(self, event: Event):
        e = json.loads(event.event_data)
        return e

    def render(self):
        env = Environment(loader=FileSystemLoader("./src/reporter/templates/"))
        template = env.get_template("trend_event.html")
        current_date = datetime.now().astimezone(timezone.utc)
        items = []
        for event in self.event_list:
            e = self._convert(event)
            items.append(

                {
                    "symbol": e["ticker"],
                    "change": round(e["change_in_ratio"], 2),
                    "type": e["strategy_name"],
                    "time": datetime.fromtimestamp(e["action_date"] / 1000).astimezone(timezone.utc).strftime(
                        "%Y-%m-%d-%H")
                }
            )

        out = template.render(subject=f"{self.subject}", update_date=current_date, items=items)
        return out


class VolumeAbnormalIncreaseReport:
    def __init__(self, subject, event_list, ):
        self.subject = subject
        self.event_list = event_list

    def _convert(self, event: Event):
        e = json.loads(event.event_data)
        return e

    def render(self):
        env = Environment(loader=FileSystemLoader("./src/reporter/templates/"))
        template = env.get_template("volume_event.html")
        current_date = datetime.now().astimezone(timezone.utc)
        items = []
        for event in self.event_list:
            e = self._convert(event)
            items.append(
                {
                    "symbol": e["ticker"],
                    "type": e["trend_type"],
                    "price": round(e["price"], 3),
                    "volume": e["volume"],
                    "time": datetime.fromtimestamp(e["action_date"] / 1000).astimezone(timezone.utc).strftime(
                        "%Y-%m-%d-%H")
                }
            )

        out = template.render(subject=f"{self.subject}", update_date=current_date, items=items)
        return out


class PriceChangeReport:
    def __init__(self, subject, event_list, ):
        self.subject = subject
        self.event_list = event_list

    def _convert(self, event: Event):
        e = json.loads(event.event_data)
        return e

    def render(self):
        env = Environment(loader=FileSystemLoader("./src/reporter/templates/"))
        template = env.get_template("price_change_event.html")
        current_date = datetime.now().astimezone(timezone.utc)
        items = []
        for event in self.event_list:
            e = self._convert(event)
            items.append(
                {
                    "symbol": e["ticker"],
                    "type": e["trend_type"],
                    "price": round(e["price"], 3),
                    "change_in_ratio": e["change_in_ratio"],
                    "time": datetime.fromtimestamp(e["action_date"] / 1000).astimezone(timezone.utc).strftime(
                        "%Y-%m-%d-%H")
                }
            )

        out = template.render(subject=f"{self.subject}", update_date=current_date, items=items)
        return out
