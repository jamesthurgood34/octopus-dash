import datetime
from dataclasses import dataclass

import pandas as pd


def hour(x: pd.Series) -> pd.Series:
    return x.hour + x.minute / 60


def off_peak(x: pd.Series) -> pd.Series:
    t = x.time()
    return (t >= datetime.time(0, 30)) & (t <= datetime.time(4, 30))


@dataclass
class Tariff:
    off_peak_rate: float = 7.50 / 100
    peak_rate: float = 30.83 / 100
    standing_day_charge: float = 24.86 / 100
    reading_hour_interval: float = 0.5

    def __post_init__(self):
        self.standing_interval_charge: float = self.standing_day_charge / (
            24 / self.reading_hour_interval
        )

    def unit_rate(self, x):
        return x.off_peak.map({True: self.off_peak_rate, False: self.peak_rate})

    def cost(self, x):
        return x.consumption * x.unit_rate + self.standing_interval_charge
