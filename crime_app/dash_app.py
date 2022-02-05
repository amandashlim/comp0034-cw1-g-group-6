# Copied from the Dash tutorial documentation at https://dash.plotly.com/layout on 24/05/2021
# Import section modified 10/10/2021 to comply with changes in the Dash library.

# Run this app with `python dash_app.py` and visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_bootstrap_components as dbc
from dash import dcc, Output, Input
from dash import html
import visualization as v
import pandas as pd

'''
TODO:
add interactivity (multiple selectable dropdown, checkbox, dropdown)
figure out how to get data from map on selected year
reformat UI layout
'''

# Define a list of one or more stylesheets here
v = v.all()
data = {"Raw": v.df,
        "Population - 2020 GLA Estimate": v.pop2020_df,
        "Population - 2011 Census": v.pop2011_df,
        "Workday Population": v.workday_df,
        "Total Daytime Population": v.daytime_df}

external_stylesheets = [dbc.themes.BOOTSTRAP]

date_slider_dict = {}
for i in range(0, len(v.date_list)):
    date_slider_dict[i] = {"label": v.date_list[i], "style": {"transform": "rotate(45deg)"}}

selections = set()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame see https://plotly.com/python/px-arguments/ for more options
app.layout = html.Div(children=[
    dbc.Row(children=[
        html.H1(children='London Crime Rate'),
        html.Div(children='''
        WebApp showcasing the reported crime rates in London
    ''')]),
    dbc.Row([
        dbc.Col([
            dbc.Row(id="chart_select_row", children=[
                # Selecting which dataset will be used to display the data
                dcc.RadioItems(id="data_select",
                               options=["Raw", "Population - 2020 GLA Estimate",
                                        "Population - 2011 Census",
                                        "Workday Population", "Total Daytime Population"],
                               value="Raw", inline=True),
                # Selecting which chart will be displayed
                dcc.Dropdown(id="chart_select",
                             options=["Map", "Histogram", "Line"],
                             value="Map")
            ]),

            dbc.Row(id="map_row", children=[
                # Dropdown to select which crime to show a map for
                dcc.Dropdown(id="crime_select",
                             options=[{"label": x, "value": x} for x in v.crime_list],
                             value="Total Crime"),
                html.H2("Map Chart"),
                dcc.Graph(id="map",
                          figure=v.map_2_layer(df=v.pop2020_df_r,
                                               selections=selections,
                                               crime="Total Crime")),
                # Slider to select the showcased year
                dcc.Slider(id="map_slider",
                           min=0, max=len(v.date_list) - 1, step=1,
                           marks=date_slider_dict)
            ]),
            dbc.Row(id="hist_row", children=[
                html.H2("Histogram"),
                # Checklist to select the Borough
                dcc.Checklist(id="hist_checklist",
                              options=v.borough_list,
                              value=["Camden"]),
                dcc.Graph(id="hist",
                          figure=v.hist(date="202109",
                                        df=v.pop2020_df, borough=["Camden"])),
                # Slider to select the time frame
                dcc.RangeSlider(id="hist_slider",
                                min=0, max=len(v.date_list) - 1, step=1,
                                marks=date_slider_dict)
            ]),
            dbc.Row(id="line_row", children=[
                html.H2("Line Chart"),
                dcc.Graph(id="line",
                          figure=v.line(crime="Drugs",
                                        df=v.pop2020_df_r, borough="Camden"))
            ])
        ])
    ])
])


@app.callback(
    # Show/Hide different charts
    Output("map_row", "style"),
    Output("hist_row", "style"),
    Output("line_row", "style"),
    Input("chart_select", "value")
)
def hide(chart_select):
    if chart_select == "Map":
        return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}
    if chart_select == "Histogram":
        return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}
    if chart_select == "Line":
        return {'display': 'none'}, {'display': 'none'}, {'display': 'block'}


@app.callback(
    # Interactivity for histogram (data, borough, timeframe)
    Output("hist", "figure"),
    Input("data_select", "value"),
    Input("hist_checklist", "value"),
    Input("hist_slider", "value")
)
def update_data(data_select, hist_checklist, hist_slider):
    # print(hist_slider)
    if hist_slider is not None:
        if hist_slider[0] != hist_slider[1]:
            fig = v.hist(df=data[data_select],
                         date=[date_slider_dict[i]["label"] for i in list(range(hist_slider[0], hist_slider[1] + 1))],
                         borough=hist_checklist)
        else:
            fig = v.hist(df=data[data_select],
                         date=date_slider_dict[hist_slider[0]]["label"],
                         borough=hist_checklist)
    else:
        fig = v.hist(df=data[data_select],
                     date=v.date_list,
                     borough=hist_checklist)
    return fig


@app.callback(
    # Update map (select areas and highlight - useful for statistics later, select data, select crime)
    Output("map", "figure"),
    [Input("map", "clickData")],
    Input("crime_select", "value"),
    Input("data_select", "value"),
    Input("map_slider", "value")
)
def update_figure(clickData, crime_select, data_select, map_slider):
    if clickData is not None:
        location = clickData['points'][0]['location']

        if location not in selections:
            selections.add(location)
        else:
            selections.remove(location)
        # print(selections)
    print(map_slider)
    if map_slider is not None:
        fig = v.map_2_layer(df=v.reformat(
            data[data_select])[v.reformat(data[data_select])["Date"]==date_slider_dict[map_slider]["label"]],
                            selections=selections,
                            crime=crime_select)
    else:
        fig = v.map_2_layer(df=v.reformat(
            data[data_select])[v.reformat(data[data_select])["Date"]==date_slider_dict[0]["label"]],
                            selections=selections,
                            crime=crime_select)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
