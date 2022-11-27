import datetime

import pandas as pd

import octopus_dash.transformatons as t


def test_hour():
    test_series = [
        datetime.time(1, 0),
        datetime.time(2, 15),
        datetime.time(3, 30),
        datetime.time(4, 45),
        datetime.time(5, 0),
        datetime.time(6, 30),
    ]

    expected = [1.0, 2.25, 3.5, 4.75, 5.0, 6.5]

    actual = [t.hour(x) for x in test_series]

    assert actual == expected


def test_off_peak():

    test_series = [
        datetime.datetime(year=2020, month=1, day=1, hour=1, minute=0),
        datetime.datetime(year=2020, month=1, day=1, hour=2, minute=15),
        datetime.datetime(year=2020, month=1, day=1, hour=3, minute=30),
        datetime.datetime(year=2020, month=1, day=1, hour=4, minute=45),
        datetime.datetime(year=2020, month=1, day=1, hour=5, minute=0),
        datetime.datetime(year=2020, month=1, day=1, hour=6, minute=30),
    ]

    expected = [True, True, True, False, False, False]

    actual = [t.off_peak(x) for x in test_series]

    assert actual == expected
