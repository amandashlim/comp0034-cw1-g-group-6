# Conda environment with C++ compiler required,
# to setup follow: https://pystan2.readthedocs.io/en/latest/windows.html

from pathlib import Path

import pandas as pd
import visualization as v
from prophet import Prophet
from datetime import datetime

v = v.all()

df = v.df_r
dummy = pd.DataFrame(df[df["Borough"] == "Camden"][["Date", "Drugs"]]).reset_index(drop=True).rename(
    columns={"Date": "ds", "Drugs": "y"})

m = Prophet(seasonality_mode="multiplicative")
m.fit(dummy)

future = m.make_future_dataframe(periods=6, freq="MS")
forecast = m.predict(future)
fig = m.plot_components(forecast)
fig.show()
forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]


class forecast:
    pass
