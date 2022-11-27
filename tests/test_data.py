import pandas as pd
import pytest

from octopus_dash.data import data_getter


@pytest.fixture
def test_data_at_time_zone_shift():
    return pd.DataFrame(
        {
            "consumption": [
                0.829,
                0.606,
                0.63,
                0.371,
                0.11,
                0.693,
                0.119,
                0.913,
                0.067,
                0.339,
                0.749,
            ],
            "interval_start": [
                "2022-10-30T02:30:00Z",
                "2022-10-30T02:00:00Z",
                "2022-10-30T01:30:00Z",
                "2022-10-30T01:00:00Z",
                "2022-10-30T01:30:00+01:00",
                "2022-10-30T01:00:00+01:00",
                "2022-10-30T00:30:00+01:00",
                "2022-10-30T00:00:00+01:00",
                "2022-10-29T23:30:00+01:00",
                "2022-10-29T23:00:00+01:00",
                "2022-10-29T22:30:00+01:00",
            ],
            "interval_end": [
                "2022-10-30T03:00:00Z",
                "2022-10-30T02:30:00Z",
                "2022-10-30T02:00:00Z",
                "2022-10-30T01:30:00Z",
                "2022-10-30T01:00:00Z",
                "2022-10-30T01:30:00+01:00",
                "2022-10-30T01:00:00+01:00",
                "2022-10-30T00:30:00+01:00",
                "2022-10-30T00:00:00+01:00",
                "2022-10-29T23:30:00+01:00",
                "2022-10-29T23:00:00+01:00",
            ],
        }
    )


def test_enrich(test_data_at_time_zone_shift):
    d = data_getter(api_key="abc", mpan="123", serial_no="123", date_from="2022-10-29")

    d._data = d.type_dataframe(test_data_at_time_zone_shift)

    d.enrich_data()

    # do some tests
