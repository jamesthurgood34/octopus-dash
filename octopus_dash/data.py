from typing import Tuple

import pandas as pd
import requests
from pandas import Timestamp

import octopus_dash.transformatons as t


class data_getter:
    def __init__(
        self, api_key: str, mpan: str, serial_no: str, date_from: str, **kwargs
    ) -> None:
        self.mpan = mpan
        self.serial_no = serial_no
        self.base_url = f"https://api.octopus.energy/v1/electricity-meter-points/{mpan}/meters/{serial_no}/consumption/"

        self.date_from = pd.to_datetime(date_from)
        self.session = requests.Session()
        self.session.auth = (api_key, "")
        self._data = None
        self.tariff = t.Tariff(
            off_peak_rate=7.50 / 100,
            peak_rate=30.83 / 100,
            standing_day_charge=24.86 / 100,
            reading_hour_interval=0.5,
        )
        self.year = None
        self.moth = None

    @staticmethod
    def type_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        return df.assign(
            interval_start=lambda x: pd.to_datetime(x.interval_start),
            interval_end=lambda x: pd.to_datetime(x.interval_end),
        )

    def _get_data(self, url: str) -> Tuple[pd.DataFrame, Timestamp, str]:
        response = self.session.get(url)
        resp_j = response.json()
        df = pd.DataFrame(resp_j["results"])
        df = self.type_dataframe(df)
        earliest_date = df.interval_start.min()

        return (
            df,
            earliest_date,
            resp_j["next"],
        )

    def load_electric_data(self):
        """
        Get
        """
        data = []
        url = self.base_url
        earliest_date = pd.to_datetime("2100-01-01 00:00:00 UTC")

        while self.date_from < earliest_date:
            df, earliest_date, url = self._get_data(url)
            data.append(df)
            # print(f"earliest_date={earliest_date}")

        self._data = pd.concat(data)

        earliest_date = self._data.interval_start.min()
        latest_date = self._data.interval_start.max()
        time_diff = latest_date - earliest_date

        # Values to annualise / make monthly
        self.year = 365 / time_diff.days
        self.month = 30.437 / time_diff.days

        return self

    def enrich_data(self):
        self._data = self._data.assign(
            hour=lambda x: x.interval_start.apply(t.hour),
            day=lambda x: x.interval_start.apply(lambda y: y.day),
            month=lambda x: x.interval_start.apply(lambda y: y.month),
            off_peak=lambda x: x.interval_start.apply(t.off_peak),
            off_grid=lambda x: x.consumption == 0.0,
            unit_rate=lambda x: self.tariff.unit_rate(x),
            cost=lambda x: self.tariff.cost(x),
        )

        return self

    def get_dataframe(self):
        return self._data

    def get_cost(self):
        total = self.enrich_data().get_dataframe().groupby("off_peak")["cost"].sum()
        total["Total"] = total.sum()
        return total

    def get_monthly_cost(self):
        return self.get_cost() * self.month

    def get_yearly_cost(self):
        return self.get_cost() * self.year
