from pathlib import Path

import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import statistics

# Pycharm show plotly plots in browser
# import plotly.io as pio
# pio.renderers.default = "browser"

'''
TODO:
add statistics
add 2nd selectable layer to map chart
add forecast
colors
'''


class all:
    def __init__(self):
        # Core data
        self.df = pd.DataFrame()
        self.population = pd.DataFrame()
        self.daytime_population = pd.DataFrame()
        self.geo = object()

        # Starting Functions
        self.get_data()
        self.district_lookup = {feature['properties']['name']: feature for feature in self.geo['features']}

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
        self.date_list = []

        # Statistics
        self.compare_to_total_crimes = 0
        self.year_to_year_change = 0
        self.compare_to_last_month = 0
        self.compare_to_last_year_average = 0
        self.correlation = 0

        # Functions
        self.boroughs()
        self.crimes()
        self.dates()

    def get_data(self):
        datafile = Path('data')
        self.df = pd.read_csv(datafile / "crime_data.csv")
        self.df = self.df[self.df["Borough"] != "Aviation Security(SO18)"]
        self.df = self.df.drop(["Unnamed: 0"], axis=1)
        self.population = pd.read_csv(datafile / "population.csv")
        self.daytime_population = pd.read_csv(datafile / "daytime_population.csv")
        self.geo = json.load(open(datafile / "london_boroughs.json"))

    def true_rate(self):
        df = self.df.merge(self.population, on="Borough")
        df = df.merge(self.daytime_population, on="Borough")
        self.workday_df = df.iloc[:, 2:len(df.columns) - 4]. \
            divide(df.loc[:, "Workday Population"].divide(1000), axis="index"). \
            join(df[["Borough", "Major Class Description"]])
        self.daytime_df = df.iloc[:, 2:len(df.columns) - 4]. \
            divide(df.loc[:, "Total Daytime Population"].divide(1000), axis="index"). \
            join(df[["Borough", "Major Class Description"]])
        self.pop2011_df = df.iloc[:, 2:len(df.columns) - 4]. \
            divide(df.loc[:, "Population - 2011 Census"].divide(1000), axis="index"). \
            join(df[["Borough", "Major Class Description"]])
        self.pop2020_df = df.iloc[:, 2:len(df.columns) - 4]. \
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

    def dates(self):
        self.date_list = self.df_r["Date"].unique()

    def get_highlights(self, selections):
        geo_highlight = dict()
        for k in self.geo.keys():
            if k != "features":
                geo_highlight[k] = self.geo[k]
            else:
                geo_highlight[k] = [self.district_lookup[selection] for selection in selections]
        return geo_highlight

    def map_2_layer(self, df, selections, crime):

        fig = px.choropleth_mapbox(df, geojson=self.geo,
                                   color=crime,
                                   locations="Borough",
                                   featureidkey="properties.name",
                                   opacity=0.5)

        # Second layer - Highlights ----------#
        if len(selections) > 0:
            # highlights contain the geojson information for only
            # the selected districts
            highlights = self.get_highlights(selections)

            fig.add_trace(
                px.choropleth_mapbox(df, geojson=highlights,
                                     color=crime,
                                     locations="Borough",
                                     featureidkey="properties.name",
                                     opacity=1).data[0]
            )

        # ------------------------------------#
        fig.update_layout(mapbox_style="carto-positron",
                          mapbox_zoom=8.5,
                          mapbox_center={"lat": 51.5072, "lon": -0.1076},
                          margin={"r": 0, "t": 0, "l": 0, "b": 0},
                          uirevision='constant')
        return fig

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
        fig = px.line(df[df["Borough"].isin(borough)],
                      x=df["Date"].unique(), y=[list(df[df["Borough"] == i][crime]) for i in borough] +
                                               [df.groupby(["Date"]).mean()[crime].tolist()],
                      title='Seasonal Crime Data - per 1000 population',
                      markers=True)
        return fig

    def get_forecast(self, data, crime, borough):
        path = Path("data/forecast")
        pepe = pd.read_json(path / data)
        pepe_final = pd.DataFrame(eval(pepe[crime][borough]))
        pepe_final["ds"] = pd.to_datetime(pepe_final["ds"]).dt.strftime("%Y%m")
        return pepe_final

    def line_2(self, crime, df, borough):
        title = "Seasonal Crime Data - per 1000 population"
        if df.iloc[6, 3] == self.df_r.iloc[6, 3]:
            forecast_df = "df_r.json"
        if df.iloc[6, 3] == self.pop2020_df_r.iloc[6, 3]:
            forecast_df = "pop2020_df_r.json"
        if df.iloc[6, 3] == self.pop2011_df_r.iloc[6, 3]:
            forecast_df = "pop2011_df_r.json"
        if df.iloc[6, 3] == self.workday_df_r.iloc[6, 3]:
            forecast_df = "workday_df_r.json"
        if df.iloc[6, 3] == self.daytime_df_r.iloc[6, 3]:
            forecast_df = "daytime_df_r.json"

        color_list = ["#ba1414","#eb7d2f","#222138","#3db00c","#167f94","#d669cd","#3a4a8c","#a3e6a9","#73c8d9","#32d990","#8ab00c",
                      "#8200e6","#8f8000","#3b2691","#222138","#FF5CCD","#ed7bde","#111f5c","#d6697d","#e3d452","#390661","#6e1727",
                      "#cc18bd","#f78383","#17362e","#b95eff","#8a76db","#031a05","#08264a","#59693e","#111a03","#c0e87d"]

        # labels = borough + ["Average Selected Crime"]
        fig = go.Figure()
        for i in range(0, len(borough)):
            fig.add_trace(go.Scatter(x=df["Date"].unique(), y=list(df[df["Borough"] == borough[i]][crime]),
                                     mode='lines',
                                     name=borough[i],
                                     line=dict(width=1.5, color = color_list[i]),
                                     # connectgaps=True,
                                     ))
            forecast = self.get_forecast(data=forecast_df, crime=crime, borough=borough[i])
            forecast["ds"] = ["202110", "202111", "202112", "202201", "202202", "202203"]
            last = df[(df["Borough"] == borough[i]) & (df["Date"] == "202109")][crime].iloc[0]
            forecast.loc[-1] = ["202109", last, last, last]
            forecast.index = forecast.index + 1
            forecast.sort_index(inplace=True)
            fig.add_trace(go.Scatter(name="Forecast",
                                     x=forecast["ds"],
                                     y=forecast["yhat"],
                                     mode="lines",
                                     line = dict(color=color_list[i]),
                                     showlegend=False))
            fig.add_trace(go.Scatter(
                name='Upper Bound',
                x=forecast["ds"],
                y=forecast['yhat_upper'],
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=0),
                showlegend=False
            ))
            fig.add_trace(go.Scatter(
                name='Lower Bound',
                x=forecast['ds'],
                y=forecast["yhat_lower"],
                marker=dict(color="#444"),
                line=dict(width=0),
                mode='lines',
                fillcolor='rgba(138, 138, 138, 0.3)',
                fill='tonexty',
                showlegend=False
            ))
        fig.add_trace(go.Scatter(x=df["Date"].unique(), y=df.groupby(["Date"]).mean()[crime].tolist(),
                                 mode='lines',
                                 name=f"Average {crime} Crimes",
                                 line=dict(color="darkgray", width=3, dash="dash")
                                 ))
        fig.update_xaxes(tickangle=45, tickfont={"size": 10})
        fig.update_layout(legend={"orientation": "h", "font": {"size": 10},
                                  "bgcolor": 'rgba(0,0,0,0)',
                                  "itemclick":False, "itemdoubleclick":False})
        return fig

    def hist(self, date, df, borough):
        fig = px.histogram(df[df["Borough"].isin(borough)],
                           y="Major Class Description", x=date). \
            update_yaxes(categoryorder="total ascending")
        return fig

    def statistics_map(self, df, month, selected_areas, crime, m=0, mmm=0, y=0):

        # Percent change from last month
        if m == 1:
            compare_to_last_month = {}
            if month == "201910":
                for i in selected_areas:
                    compare_to_last_month[i] = "No data for previous months please select a different date"
                return compare_to_last_month
            else:
                for i in selected_areas:
                    if df[(df["Date"] == self.date_list[self.date_list.tolist().index(month) - 1]) & (
                            df["Borough"] == i)][crime].tolist()[0] == 0:
                        a = 0
                    else:
                        a = ((df[(df["Date"] == self.date_list[self.date_list.tolist().index(month)]) & (
                                df["Borough"] == i)][crime].tolist()[0] -
                              df[(df["Date"] == self.date_list[self.date_list.tolist().index(month) - 1]) & (
                                      df["Borough"] == i)][crime].tolist()[0]) / \
                             df[(df["Date"] == self.date_list[self.date_list.tolist().index(month) - 1]) & (
                                     df["Borough"] == i)][crime].tolist()[0])
                    compare_to_last_month[i] = a
                return compare_to_last_month

        # Percent change from last three months
        if mmm == 1:
            compare_to_last_three_months = {}
            if month in self.date_list.tolist()[:self.date_list.tolist().index("202001")]:
                for i in selected_areas:
                    compare_to_last_three_months[i] = "No data for previous months please select a different date"
                return compare_to_last_three_months
            else:
                for i in selected_areas:
                    if statistics.mean(df[(df["Date"].isin(self.date_list[self.date_list.tolist().index(
                            month) - 3:self.date_list.tolist().index(month)].tolist())) & (df["Borough"] == i)][
                                           crime].tolist()) == 0:
                        a = 0
                    else:
                        a = ((df[(df["Date"] == str(int(month))) & (df["Borough"] == i)][crime].tolist()[0] -
                              statistics.mean(df[(df["Date"].isin(self.date_list[self.date_list.tolist().index(
                                  month) - 3:self.date_list.tolist().index(month)].tolist())) & (df["Borough"] == i)][
                                                  crime].tolist())) / \
                             statistics.mean(df[(df["Date"].isin(self.date_list[self.date_list.tolist().index(
                                 month) - 3:self.date_list.tolist().index(month)].tolist())) & (df["Borough"] == i)][
                                                 crime].tolist()))
                    compare_to_last_three_months[i] = a
                return compare_to_last_three_months

        # Percent change from last year
        if y == 1:
            compare_to_last_year = {}
            if month in self.date_list.tolist()[:self.date_list.tolist().index("202010")]:
                for i in selected_areas:
                    compare_to_last_year[i] = "No data for previous months please select a different date"
                return compare_to_last_year
            else:
                for i in selected_areas:
                    if statistics.mean(df[(df["Date"].isin(self.date_list[self.date_list.tolist().index(
                            month) - 12:self.date_list.tolist().index(month)].tolist())) & (df["Borough"] == i)][
                                           crime].tolist()) == 0:
                        a = 0
                    else:
                        a = ((df[(df["Date"] == str(int(month))) & (df["Borough"] == i)][crime].tolist()[0] -
                              statistics.mean(df[(df["Date"].isin(self.date_list[self.date_list.tolist().index(
                                  month) - 12:self.date_list.tolist().index(month)].tolist())) & (df["Borough"] == i)][
                                                  crime].tolist())) / \
                             statistics.mean(df[(df["Date"].isin(self.date_list[self.date_list.tolist().index(
                                 month) - 12:self.date_list.tolist().index(month)].tolist())) & (df["Borough"] == i)][
                                                 crime].tolist()))
                    compare_to_last_year[i] = a
                return compare_to_last_year
