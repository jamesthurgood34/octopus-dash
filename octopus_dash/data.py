import requests
import json
import pandas as pd

class data_getter:
    def __init__(self, api_key, mpan, serial_no, date_from, **kwargs) -> None:
        self.mpan = mpan
        self.serial_no = serial_no
        ## TODO: making this general not just elec
        self.base_url = f"https://api.octopus.energy/v1/electricity-meter-points/{mpan}/meters/{serial_no}/consumption/"
        
        self.date_from = pd.to_datetime(date_from)
        self.session = requests.Session()
        self.session.auth = (api_key, "")
    
    @staticmethod
    def type_dataframe(df):
        return df.assign(
                    # TODO: Fix GMT/BST issue
                    interval_start = lambda x: pd.to_datetime(x.interval_start, utc=True),
                    interval_end = lambda x: pd.to_datetime(x.interval_end, utc=True)
                    )

    def get_data(self, url):
        response = self.session.get(url)
        resp_j = response.json()
        df = pd.DataFrame(resp_j["results"])
        df = self.type_dataframe(df)
        earliest_date = df.interval_start.min()
        return df, earliest_date, resp_j["next"],

    def get_all_electric_data(self):
        data = []
        url = self.base_url
        earliest_date = pd.to_datetime("2100-01-01 00:00:00 UTC")
        
        while self.date_from < earliest_date:
            df, earliest_date, url = self.get_data(url)
            data.append(df)
            print(f"earliest_date={earliest_date}")

        data = pd.concat(data)

        return self.type_dataframe(data)
