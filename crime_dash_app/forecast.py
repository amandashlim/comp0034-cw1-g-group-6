# Conda environment with C++ compiler required,
# to setup follow: https://pystan2.readthedocs.io/en/latest/windows.html

from pathlib import Path

import pandas as pd
import visualization as v
from prophet import Prophet
import json

v = v.all()

def forecast(borough, crime, df):
    df["Date"] = pd.to_datetime(df["Date"], format="%Y%m").dt.strftime("%Y-%m")
    dummy = pd.DataFrame(df[df["Borough"] == borough][["Date", crime]]).reset_index(drop=True).rename(
        columns={"Date": "ds", crime: "y"})
    m = Prophet()
    m.fit(dummy)
    future = m.make_future_dataframe(periods=6, freq="MS")
    forecast = m.predict(future)
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m").dt.strftime("%Y%m")
    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(6)

def all_forecasts(data):
    dict = {}
    for i in v.crime_list:
        a = {}
        for j in v.borough_list:
            a[j] = forecast(j, i, data)
        dict[i] = a
    return dict

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_json'):
            return obj.to_json(orient='records')
        return json.JSONEncoder.default(self, obj)

def save_data():
    df_r = all_forecasts(v.df_r)
    pop2020_df_r = all_forecasts(v.pop2020_df_r)
    pop2011_df_r = all_forecasts(v.pop2011_df_r)
    workday_df_r = all_forecasts(v.workday_df_r)
    daytime_df_r = all_forecasts(v.daytime_df_r)

    path = Path("data/forecast")
    with open(path/'df_r.json', 'w') as fp:
        json.dump(df_r, fp, cls=JSONEncoder)
    with open(path/'pop2020_df_r.json', 'w') as fp:
        json.dump(pop2020_df_r, fp, cls=JSONEncoder)
    with open(path/'pop2011_df_r.json', 'w') as fp:
        json.dump(pop2011_df_r, fp, cls=JSONEncoder)
    with open(path/'workday_df_r.json', 'w') as fp:
        json.dump(workday_df_r, fp, cls=JSONEncoder)
    with open(path/'daytime_df_r.json', 'w') as fp:
        json.dump(daytime_df_r, fp, cls=JSONEncoder)

def get_forecast(data,crime, borough):
    path = Path("data/forecast")
    pepe = pd.read_json(path/data)
    pepe_final = pd.DataFrame(eval(pepe[crime][borough]))
    return pepe_final
