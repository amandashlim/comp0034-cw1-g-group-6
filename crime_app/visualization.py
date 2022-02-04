from pathlib import Path

import pandas as pd
import json
import plotly.express as px


class all:
    def __init__(self):
        # Core data
        self.df = pd.DataFrame()
        self.population = pd.DataFrame()
        self.daytime_population = pd.DataFrame()
        self.geo = object()

        # Starting Functions
        self.get_data()

        # Updated Data
        self.workday_df = pd.DataFrame()
        self.daytime_df = pd.DataFrame()
        self.pop2011_df = pd.DataFrame()
        self.pop2020_df = pd.DataFrame()
        self.true_rate()

        # Reformated Data
        self.df_r = self.reformat(self.df)
        self.workday_df_r = self.reformat(self.workday_df)
        self.daytime_df_r = self.reformat(self.daytime_df)
        self.pop2011_df_r = self.reformat(self.pop2011_df)
        self.pop2020_df_r = self.reformat(self.pop2020_df)

        # Lists
        self.borough_list = []
        self.crime_list = []

        # Statistics
        self.compare_to_total_crimes = 0

        # Functions
        self.boroughs()
        self.crimes()

    def get_data(self):
        datafile = Path('data')
        self.df = pd.read_csv(datafile / "crime_data.csv")
        self.df.loc[(self.df.Borough == "Aviation Security(SO18)"), "Borough"] = "City of London1"
        self.df = self.df.drop(["Unnamed: 0"], axis=1)
        # self.df["Total Crime"] = self.df.iloc[:, 2:len(self.df.columns) - 4].sum(axis=1)
        self.population = pd.read_csv(datafile / "population.csv")
        self.daytime_population = pd.read_csv(datafile / "daytime_population.csv")
        self.geo = json.load(open(datafile / "london_boroughs.json"))

    def true_rate(self):
        df = self.df.merge(self.population, on="Borough")
        df = df.merge(self.daytime_population, on="Borough")
        self.workday_df = df.iloc[:, 3:len(df.columns) - 4]. \
            divide(df.loc[:, "Workday Population"].divide(1000), axis="index"). \
            join(df[["Borough", "Major Class Description"]])
        self.daytime_df = df.iloc[:, 3:len(df.columns) - 4]. \
            divide(df.loc[:, "Total Daytime Population"].divide(1000), axis="index"). \
            join(df[["Borough", "Major Class Description"]])
        self.pop2011_df = df.iloc[:, 3:len(df.columns) - 4]. \
            divide(df.loc[:, "Population - 2011 Census"].divide(1000), axis="index"). \
            join(df[["Borough", "Major Class Description"]])
        self.pop2020_df = df.iloc[:, 3:len(df.columns) - 4]. \
            divide(df.loc[:, "Population - 2020 GLA Estimate"].divide(1000), axis="index"). \
            join(df[["Borough", "Major Class Description"]])

    def reformat(self, i):
        i = i.melt(id_vars=["Borough", "Major Class Description"])
        i = i.pivot_table(values="value", index=["Borough", "variable"],
                          columns="Major Class Description").reset_index()
        i = i.rename({"variable": "Date"}, axis=1)
        i["Total Crime"] = i.iloc[:, 2:].sum(axis=1)
        i["Average Crime"] = i.iloc[:, 2:len(i.columns) - 2].mean(axis=1)
        return i

    def boroughs(self):
        self.borough_list = self.df["Borough"].unique()

    def crimes(self):
        self.crime_list = self.df["Major Class Description"].unique()

    def map(self, crime, df):
        fig = px.choropleth(data_frame=df,
                            geojson=self.geo,
                            featureidkey='properties.name',
                            locations="Borough",
                            color=crime,
                            color_continuous_scale="Viridis",
                            animation_frame="Date",
                            hover_data=self.crime_list,
                            title="Crime in London")
        fig.update_geos(fitbounds="locations", visible=False)
        # fig.update_layout(margin=dict(l=60, r=60, t=50, b=50))
        return fig

    def line(self, crime, df, borough):
        fig = px.line(df[df["Borough"] == borough],
                      x="Date", y=[crime, "Average Crime"],
                      title='Seasonal Crime Data - per 1000 population')
        return fig

    def hist(self, date, df, borough):
        fig = px.histogram(df[df["Borough"] == borough],
                           y="Major Class Description", x=date). \
            update_yaxes(categoryorder="total ascending")
        return fig

    def statistics(self):
        # showcase statistics for selected area and selected year (year to year change, % change compared to
        # total, create linear regression (facebooks prophet seasonal mode, or annova seasonal with confidence
        # intervals) to showcase forecast for next few months
        pass
