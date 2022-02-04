# Copied from the Dash tutorial documentation at https://dash.plotly.com/layout on 24/05/2021
# Import section modified 10/10/2021 to comply with changes in the Dash library.

# Run this app with `python dash_app.py` and visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import visualization as v

# Define a list of one or more stylesheets here
v = v.all()
data = v.pop2020_df_r

external_stylesheets = [dbc.themes.BOOTSTRAP]

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
            html.H2("Map Chart"),
            dcc.Graph(id="map",
                      figure=v.map(crime=v.crime_list[1], df=v.pop2020_df_r)),
        ]),
        dbc.Col([
            dbc.Row([
                html.H2("Histogram"),
                dcc.Graph(id="hist",
                          figure=v.hist(date="202109",
                                        df=v.pop2020_df, borough="Camden"))
            ]),
            dbc.Row([
                html.H2("Line Chart"),
                dcc.Graph(id="line",
                          figure=v.line(crime="Drugs",
                                        df=v.pop2020_df_r, borough="Camden"))
            ])
        ])
    ])
])
if __name__ == '__main__':
    app.run_server(debug=True)
