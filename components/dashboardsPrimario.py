from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
from globals import *
from app import app

main_config = {
    "hovermode": "x unified",
    "legend": {"yanchor":"top", 
                "y":0.9, 
                "xanchor":"left",
                "x":0.1,
                "title": {"text": None},
                "font" :{"color":"white"},
                "bgcolor": "rgba(0,0,0,0.5)"},
    "margin": {"l":0, "r":0, "t":20, "b":0}
}

df = pd.read_csv("vgsales.csv")

df.dropna(inplace=True)
df.drop('Rank', axis=1, inplace=True)

df = df[df['Year'] != 2020]
df['Year'] = df['Year'].astype('int')

global_genres = df.groupby(['Genre'])['Global_Sales'].sum().sort_values(ascending=False).reset_index()['Genre'].unique().tolist()
global_genres.insert(0, 'Global')

top_publishers = df.groupby(['Publisher'])['Global_Sales'].sum()
top_publishers = top_publishers.sort_values(ascending=False).head(10).reset_index()

df_store = df.to_dict()

fig = px.bar(df, x=df['Genre'], y=df['Global_Sales'])

# =========  Layout  =========== #
layout = dbc.Col([
        dbc.Row([
        dbc.Col([
            dbc.Card([
                html.Legend('DataSet usado', style={'text-align':'center'}),
                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{'id': c, 'name': c} for c in df.columns],
                    style_header={ 'border': '1px solid #EAEAEA' },
                    filter_action='native',
                    style_cell={ 'border': '1px solid #EAEAEA', 'textAlign': 'left'},
                    page_size=4,     
                    style_data={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                    },)
            ], style={'margin-top':'10px', 'padding-left':'10px', 'padding-right':'15px'})
        ], width=12),
       ]),
       dbc.Row([
        dbc.Col([
            dbc.Card([
                dcc.RangeSlider(
                            id='rangeslider',
                            marks= {int(x): f'{x}' for x in df['Year'].unique()},
                            step=3,                
                            min=1980,
                            max=2017,
                            value=[1980,2017],   
                            dots=True,             
                            pushable=3,
                            tooltip={'always_visible':False, 'placement':'bottom'},
                        ),
                        dcc.Interval(id='interval', interval=5000),
            ], style={'margin-top':'10px'})
        ], width=12)
       ]),
        dbc.Row([
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='graphSec0', className='dbc', config={"displayModeBar": False, "showTips": False}),
                dbc.Button("Abrir modal", id="open10", n_clicks=0, style={'border':'none', 'border-radius':'5px', 'margin-top':'5px', 'width':'80%', 'margin-left':'10%', 'margin-bottom':'10px'}),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Gráfico de barra (gênero x venda global):")),
                        dbc.ModalBody(dcc.Graph(id='graphSec10', className='dbc', config={"displayModeBar": False, "showTips": False})),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Fechar", id="close10", className="ms-auto", n_clicks=0, style={'border-radius':'5px'}
                            )
                        ),
                    ],id="modal10",
                    size="xl",
                    is_open=False,)

            ], style={'margin-top':'10px'})
        ], width=4),
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='graphSec1', className='dbc', config={"displayModeBar": False, "showTips": False}, animate=True),
                dbc.Button("Abrir modal", id="open11", n_clicks=0, style={'border':'none', 'border-radius':'5px', 'margin-top':'5px', 'width':'80%', 'margin-left':'10%', 'margin-bottom':'10px'}),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Gráfico de linha (Venda da Europa x Ano):")),
                        dbc.ModalBody(dcc.Graph(id='graphSec11', className='dbc', config={"displayModeBar": False, "showTips": False})),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Fechar", id="close11", className="ms-auto", n_clicks=0, style={'border-radius':'5px'}
                            )
                        ),
                    ],id="modal11",
                    size="xl",
                    is_open=False,)
            ], style={'margin-top':'10px'})
        ], width=5),
        dbc.Col([
            dbc.Card([
                dbc.Carousel(
                    items=[
                        {"key": "1", "src": "https://www.techvisibility.com/wp-content/uploads/2022/01/istockphoto-1183889081-612x612-1.jpg"},
                        {"key": "2", "src": "https://images.medicaldaily.com/sites/medicaldaily.com/files/styles/headline/public/2015/11/19/video-games.jpg"},
                        {"key": "3", "src": "https://cdn.pixabay.com/photo/2021/09/07/07/11/game-console-6603120__340.jpg"},
                        {"key": "4", "src":"https://media.istockphoto.com/id/687958304/photo/sony-play-station-4-and-dualshock-video-game-console.jpg?s=612x612&w=0&k=20&c=TjYQMjUchhSuoWd9P3z4XE-E_QddhruFMKVq644RmIE="},
                        {"key": "5", "src": "https://media.istockphoto.com/id/1287493837/photo/sony-playstation-5-console-and-games.jpg?s=612x612&w=0&k=20&c=WY9UmmXx7Oqr-7byiFh6JP3XL0hOCb_koGLmIK8lsk0="},
                        {"key": "6", "src": "https://s2.glbimg.com/CSKVAF2Ge6KlRYIlbh-1cY8wUsg=/0x0:750x500/984x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_08fbf48bc0524877943fe86e43087e7a/internal_photos/bs/2020/D/5/OQSN6dTA6z3AdoS3koqw/nintendo-unsplash-alvaro-reyes.jpeg"},
                    ],
                    controls=False,
                    className="carousel-fade",
                    indicators=True,
                    interval=1500,
                    ride="carousel"
                ) 
            ], style={'margin-top':'10px', 'padding':'5px'})
        ], width=3, style={'height':'370px'}),
       ]),
    ])



# =========  Callbacks  =========== #
@app.callback(
    Output('graphSec0', 'figure'),
    Input('rangeslider', 'value'),
)
def long(date):
    mask = (df['Year'] >= date[0]) & (df['Year'] <= date[1])

    df_generos = df.loc[mask]
    trace = df_generos.groupby('Genre')['Global_Sales'].sum().reset_index()
    fig = px.bar(df, x=trace['Genre'], y=trace['Global_Sales'])

    fig.update_layout(main_config, height=200, xaxis={'title': None}, yaxis={'title': None})

    return fig

@app.callback(
    Output('graphSec10', 'figure'),
    Input('rangeslider', 'value'),
)
def long(date):
    mask = (df['Year'] >= date[0]) & (df['Year'] <= date[1])

    df_generos = df.loc[mask]
    trace = df_generos.groupby('Genre')['Global_Sales'].sum().reset_index()
    fig = px.bar(df, x=trace['Genre'], y=trace['Global_Sales'])

    fig.update_layout(main_config, height=200, xaxis={'title': None}, yaxis={'title': None})

    return fig


@app.callback(
    Output("modal10", "is_open"),
    [Input("open10", "n_clicks"), Input("close10", "n_clicks")],
    [State("modal10", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('graphSec1', 'figure'),
    Input('rangeslider', 'value'),
)
def long(date):
    mask = (df['Year'] >= date[0]) & (df['Year'] <= date[1])

    df_EU = df.loc[mask]
    trace = df_EU.groupby('Year')['EU_Sales'].sum().reset_index()
    fig_line = px.line(df, x=trace['Year'], y=trace['EU_Sales'], markers=True)

    fig_line.update_layout(main_config, height=200, xaxis={'title': None}, yaxis={'title': None})

    return fig_line

@app.callback(
    Output("modal11", "is_open"),
    [Input("open11", "n_clicks"), Input("close11", "n_clicks")],
    [State("modal11", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('graphSec11', 'figure'),
    Input('rangeslider', 'value'),
)
def long(date):
    mask = (df['Year'] >= date[0]) & (df['Year'] <= date[1])

    df_EU = df.loc[mask]
    trace = df_EU.groupby('Year')['EU_Sales'].sum().reset_index()
    fig_line = px.line(df, x=trace['Year'], y=trace['EU_Sales'], markers=True)

    fig_line.update_layout(main_config, height=200, xaxis={'title': None}, yaxis={'title': None})

    return fig_line