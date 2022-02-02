from pathlib import Path

data = Path("data")
csv_1 = "population.csv"

pd.read_csv(data/csv_1)


import pandas as pd
import json
import plotly.express as px


class VisualMap:
    def __init__ (self):
        self.df = pd.DataFrame()
        self.population = pd.DataFrame
        self.daytime_population = pd.DataFrame()
        #self.geo = json.load(open("london_boroughs.json"))
        self.get_data()
        self.reformat()

    def get_data(self):
        datafolder = Path('data')
        csvfile = "crime_data.csv"
        self.df = pd.read_csv(datafolder/csvfile)

    def reformat(self):
        self.df = self.df.drop(["Unnamed: 0"], axis=1).melt(id_vars=["Borough","Major Class Description"])
        self.df = self.df.pivot_table(values="value", index=["Borough", "variable"],
                            columns="Major Class Description").reset_index()
        self.df = self.df.rename({"variable": "Date"}, axis=1)
        self.df["Total Crime"] = self.df.iloc[:,2:].sum(axis=1)

    def borough_list(self):
        return(self.df["Borough"].unique())

    def crimes(self):
        return(self.df["Major Class Description"].unique())

    def map(self):
        #change area input = color change
        df = self.reformat(self.df)
        fig = px.choropleth(data_frame=df,
                            geojson=self.geo,
                            featureidkey='properties.name',
                            locations="Borough",
                            color='Total Crime',
                            color_continuous_scale="Viridis",
                            animation_frame="Date",
                            hover_data=['Burglary', 'Criminal Damage', 'Drugs',
                                        'Fraud or Forgery', 'Other Notifiable Offences', 'Robbery',
                                        'Sexual Offences', 'Theft and Handling', 'Violence Against the Person'],
                            title="Crime in London")
        fig.update_geos(fitbounds="locations", visible=False)
        return(fig)

    def statistics(self):
        #showcase statistics for selected area and selected year (year to year change, % change compared to
        #total, create linear regression (facebooks prophet seasonal mode, or annova seasonal with confidence
        #intervals) to showcase forecast for next few months
        pass