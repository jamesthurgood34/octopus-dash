import json

from octopus_dash import data

with open("./donttrack/config.json") as tf:
    config = json.load(tf)

df = data.data_getter(**config).get_all_electric_data()
