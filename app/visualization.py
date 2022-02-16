from pathlib import Path

import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import statistics
import numpy as np

# Pycharm show plotly plots in browser
# import plotly.io as pio
# pio.renderers.default = "browser"

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

        # Functions
        self.boroughs()
        self.crimes()
        self.dates()

    def get_data(self):
        # Import the main data (crime_data), supporting datasets (population, daytime_population), and geojson
        datafile = Path(__file__).parent.joinpath("data")
        self.df = pd.read_csv(datafile / "crime_data.csv")
        self.df = self.df[self.df["Borough"] != "Aviation Security(SO18)"] #drop heathrow and city airport as not needed
        self.df = self.df.drop(["Unnamed: 0"], axis=1)
        self.population = pd.read_csv(datafile / "population.csv")
        self.daytime_population = pd.read_csv(datafile / "daytime_population.csv")
        self.geo = json.load(open(datafile / "london_boroughs.json"))

    def true_rate(self):
        # create datasets with appropriate crime rates per 1000 population (standard crime measurement metrics)
        # create by manipulating the main dataset and dividing with supporting columns respectively
        # have created datasets be run class variables and the function run with the class
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
        # reformat data from dates as columns and crimes as rows to crimes as columns and dates in a row
        # add Total and Average Crime columns
        # this dataformat will be usefull to create map and line visual
        i = i.melt(id_vars=["Borough", "Major Class Description"])
        i = i.pivot_table(values="value", index=["Borough", "variable"],
                          columns="Major Class Description").reset_index()
        i = i.rename({"variable": "Date"}, axis=1)
        i["Total Crime"] = i.iloc[:, 2:].sum(axis=1)
        i["Average Crime"] = i.iloc[:, 2:len(i.columns) - 2].mean(axis=1)
        return i

    def boroughs(self):
        # returns the list of boroughs
        self.borough_list = self.df["Borough"].unique()

    def crimes(self):
        # returns the list of crime types
        self.crime_list = self.df["Major Class Description"].unique()

    def dates(self):
        # returns the list of dates (in %Y%m format)
        self.date_list = self.df_r["Date"].unique()

    def get_highlights(self, selections):
        # Returns the filtered geojson for selected areas (boroughs)
        # Adapted from: https://towardsdatascience.com/highlighting-click-data-on-plotly-choropleth-map-377e721c5893
        geo_highlight = dict()
        for k in self.geo.keys():
            if k != "features":
                geo_highlight[k] = self.geo[k]
            else:
                geo_highlight[k] = [self.district_lookup[selection] for selection in selections]
        return geo_highlight

    def map_2_layer(self, df, selections, crime):
        # Map visual used in the dash app
        # has the property to include selections (which will be implemented with click callback in dashapp)
        # it has two layers the DEFAULT layer with all boroughs and lower opacity
        # the SELECTABLE layer has higher opacity and only applies to boroughs in the selections
        # some of the code adapted from: https://towardsdatascience.com/highlighting-click-data-on-plotly-choropleth-map-377e721c5893

        # Default layer
        fig = px.choropleth_mapbox(df, geojson=self.geo,
                                   color=crime,
                                   locations="Borough",
                                   featureidkey="properties.name",
                                   opacity=0.5)

        # Selectable layer
        if len(selections) > 0:
            highlights = self.get_highlights(selections) # filtered geojson with selected boroughs
            fig.add_trace(
                px.choropleth_mapbox(df, geojson=highlights,
                                     color=crime,
                                     locations="Borough",
                                     featureidkey="properties.name",
                                     opacity=1).data[0])

        fig.update_layout(mapbox_style="carto-positron",
                          mapbox_zoom=8.5,
                          mapbox_center={"lat": 51.5072, "lon": -0.1076},
                          margin={"r": 0, "t": 0, "l": 0, "b": 0},
                          uirevision='constant')
        fig.update_geos(scope="europe", fitbounds="geojson")
        return fig

    def map(self, crime, df):
        # Simple map visual with interactive dates - NOT USED
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
        return fig

    def line(self, crime, df, borough):
        # Simple line visual without forecasts - NOT USED
        fig = px.line(df[df["Borough"].isin(borough)],
                      x=df["Date"].unique(), y=[list(df[df["Borough"] == i][crime]) for i in borough] +
                                               [df.groupby(["Date"]).mean()[crime].tolist()],
                      title='Seasonal Crime Data - per 1000 population',
                      markers=True)
        return fig

    def get_forecast(self, data, crime, borough):
        # returns a dataframe of forecasts made with FB Prophet seasonality algorithm which were stored as .json
        # and subsets by selected crime and borough
        path = Path(__file__).parent.joinpath("data/forecast")
        pepe = pd.read_json(path / data)
        pepe_final = pd.DataFrame(eval(pepe[crime][borough]))
        pepe_final["ds"] = pd.to_datetime(pepe_final["ds"]).dt.strftime("%Y%m")
        return pepe_final

    def line_2(self, crime, df, borough):
        # Line visual used in the dash app
        # creates a line visual with both the real data and the forecasts made with FB Prophet seasonality algorithm

        title = "Seasonal Crime Data - per 1000 population"
        # assigns file names - done in this way because prophet is difficult to setup and the predictions can take
        # a while to run, so they were calculated before and stored in .json files

        # if statements check to determine which dataset is given
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

        color_list = ["#ba1414", "#eb7d2f", "#222138", "#3db00c", "#167f94", "#d669cd", "#3a4a8c", "#a3e6a9", "#73c8d9",
                      "#32d990", "#8ab00c",
                      "#8200e6", "#8f8000", "#3b2691", "#222138", "#FF5CCD", "#ed7bde", "#111f5c", "#d6697d", "#e3d452",
                      "#390661", "#6e1727",
                      "#cc18bd", "#f78383", "#17362e", "#b95eff", "#8a76db", "#031a05", "#08264a", "#59693e", "#111a03",
                      "#c0e87d"]

        fig = go.Figure()

        # Traces for selected boroughs and their forecasts with confidence intervals
        for i in range(0, len(borough)):
            fig.add_trace(go.Scatter(x=df["Date"].unique(), y=list(df[df["Borough"] == borough[i]][crime]),
                                     mode='lines',
                                     name=borough[i],
                                     line=dict(width=1.5, color=color_list[i]),
                                     ))

            # get forecast data and use the last real datapoint as first to 'merge' predictions and real data
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
                                     line=dict(color=color_list[i]),
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

        # add average crime rate
        fig.add_trace(go.Scatter(x=df["Date"].unique(), y=df.groupby(["Date"]).mean()[crime].tolist(),
                                 mode='lines',
                                 name=f"Average {crime} Crimes",
                                 line=dict(color="darkgray", width=3, dash="dash")
                                 ))
        fig.update_xaxes(tickangle=45, tickfont={"size": 10})
        fig.update_layout(legend={"orientation": "h", "font": {"size": 10},
                                  "bgcolor": 'rgba(0,0,0,0)',
                                  "itemclick": False, "itemdoubleclick": False})
        return fig

    def hist(self, date, df, borough):
        # returns the histogram of crime rates by different crime types
        # filters by given date range and borough
        fig = px.histogram(df[df["Borough"].isin(borough)],
                           y="Major Class Description", x=date,
                           labels={"x": "Crime Rate"}). \
            update_yaxes(categoryorder="total ascending")
        fig.update_layout(showlegend=False)
        return fig

    def statistics_map(self, df, month, selected_areas, crime, m=0, mmm=0, y=0):
        # returns percent changes from last month, last three months, last year
        # includes exceptions for 0 crime rate and not enough data

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

    def statistics_hist(self, time_range, df, borough):
        # returns a correlation matrix between crime types
        # adapted from: https://stackoverflow.com/questions/66572672/correlation-heatmap-in-plotly

        correlation_m = df[(df["Date"].isin(time_range)) & (df["Borough"].isin(borough))][self.crime_list].corr()
        mask = np.triu(np.ones_like(correlation_m, dtype=bool))
        rLT = correlation_m.mask(mask)

        heat = go.Heatmap(
            z=rLT, x=rLT.columns.values, y=rLT.columns.values,
            zmin=-1, zmax=1, xgap=1, ygap=1,
            colorscale='RdBu')

        title = 'Crime Type Correlation Matrix'

        layout = go.Layout(title_text=title, title_x=0.5, xaxis_showgrid=False,
            yaxis_showgrid=False, yaxis_autorange='reversed')

        fig = go.Figure(data=[heat], layout=layout)
        fig.update_xaxes(tickangle=90, tickfont={"size": 10})
        fig.update_yaxes(tickangle=45, tickfont={"size": 10})
        return fig

    def statistics_line(self,crime,df):
        # returns various statistics (understandable by name)

        worst_average_borough = df.groupby("Borough").mean()[crime].idxmax()
        average_bad = df.groupby("Borough").mean()[crime].loc[worst_average_borough]

        best_average_borough = df.groupby("Borough").mean()[crime].idxmin()
        average_good = df.groupby("Borough").mean()[crime].loc[best_average_borough]

        worst_instance_borough = df.loc[df[crime].idxmax()]["Borough"]
        year_max = df.loc[df[crime].idxmax()]["Date"]
        max = df[crime].max()

        best_borough = df.loc[df[crime].idxmin()]["Borough"]
        year_min = df.loc[df[crime].idxmin()]["Date"]
        min = df[crime].min()

        return worst_average_borough, average_bad, best_average_borough, average_good,\
               worst_instance_borough,\
               year_max, max, best_borough, year_min, min