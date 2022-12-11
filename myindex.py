from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from app import *
from components import sidebar, dashboardsPrimario, dashboardsSecundario, dashboardsTerciario




# =========  Layout  =========== #
content = html.Div(id="page-content")


app.layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
            dcc.Location(id='url'),
            sidebar.layout
        ], sm=2),
        dbc.Col([
            content
        ], md=10)
    ])    
], fluid=True,)

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def render_page(pathname):
    if pathname == '/' or pathname == '/dashboardsPrimario':
        return dashboardsPrimario.layout
    if pathname == '/dashboardsSecundario':
        return dashboardsSecundario.layout
    if pathname == '/dashboardsTerciario':
        return dashboardsTerciario.layout

if __name__ == '__main__':
    app.run_server(debug=True,port=8080)
    #app.run_server(debug=False,port=8080,host='0.0.0.0')
