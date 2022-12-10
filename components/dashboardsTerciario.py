from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
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

layout = dbc.Col([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.Legend('Vendas na América do norte', style={'text-align':'center', 'font-size':'35px', 'margin-top':'20px'}),
                dcc.Graph(id='graphNNA', style={'margin-top':'-15px'})
            ], style={'margin-top':'10px'}),
        ], width=4),
        dbc.Col([
            dbc.Card([
                html.Legend('Vendas na Europa', style={'text-align':'center', 'font-size':'35px', 'margin-top':'20px'}),
                dcc.Graph(id='graphNEU', style={'margin-top':'-15px'})
            ], style={'margin-top':'10px'})
        ], width=4),
        dbc.Col([
            dbc.Card([
                html.Legend('Vendas no Japão', style={'text-align':'center', 'font-size':'35px', 'margin-top':'20px'}),
                dcc.Graph(id='graphNJP', style={'margin-top':'-15px'})
            ], style={'margin-top':'10px'})
        ], width=4),
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
                        dcc.Interval(id='interval', interval=10000),
            ], style={'margin-top':'10px'})
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.Carousel(
                    items=[
                        {"key": "2", "src": "https://upload.wikimedia.org/wikipedia/pt/b/b5/Wii_Sports_capa.png"},
                        {"key": "3", "src": "https://m.media-amazon.com/images/I/81U3yDkYrgL.jpg"},
                        {"key": "4", "src": "https://images.tcdn.com.br/img/img_prod/647213/jogo_wii_play_motion_seminovo_1585_1_862a2757ad4622c053fe97aa5e6dda17.jpg"},
                        {'key': '6', 'src': 'https://smartcdkeys.com/image/data/products/grand-theft-auto-5-gta-v-steam/cover/grand-theft-auto-5-gta-v-steam-smartcdkeys-cheap-cd-key-cover.jpg'},
                        {'key': '7', 'src': 'https://m.media-amazon.com/images/M/MV5BY2ZjYjY2ZGMtZGMwNi00NjRlLWJlNmQtMGRlYTE4YjE4MGFjXkEyXkFqcGdeQXVyMzIwMjMyMzc@._V1_FMjpg_UX1000_.jpg'},
                        {'key': '8', 'src': 'https://upload.wikimedia.org/wikipedia/pt/b/b1/Super_Mario_Galaxy_capa.png'},
                        {'key': '9', 'src': 'https://a-static.mlcdn.com.br/800x560/revista-superposter-dicas-truques-xbox-edition-halo-reach-editora-europa/europa/02c37cfe6c6a11eb9bd74201ac1850d6/3ff53bae0aba7dbc4c13960c2302e9ac.jpg'},
                    ],
                    controls=False,
                    className="carousel-fade",
                    indicators=True,
                    interval=1500,
                    ride="carousel"
                ) 
            ], style={'margin-top':'10px'})
        ], width=3),
        dbc.Col([
            dbc.Card([
                html.Legend('Vendas em outros países', style={'text-align':'center', 'font-size':'35px', 'margin-top':'20px'}),
                dcc.Graph(id='GraphNOther', style={'margin-top':'-14px'})
            ], style={'margin-top':'10px'})
        ], width=4),
        dbc.Col([
            dbc.Card([
                html.Legend('Vendas global', style={'text-align':'center', 'margin-top':'20px', 'font-size':'35px'}),
                dcc.Graph(id='graphNGS', style={'margin-top':'-15px'})
            ], style={'margin-top':'10px'})
        ], width=5)
    ])
])

# ==== CALLBACK ==== #

@app.callback(
    Output('graphNEU', 'figure'),
    Output('graphNNA', 'figure'),
    Output('graphNJP', 'figure'),
    Output('GraphNOther', 'figure'),
    Output('graphNGS', 'figure'),
    Input('rangeslider', 'value'),
)
def ind1(date):    
    mask = (df['Year'] >= date[0]) & (df['Year'] <= date[1])

    graphNEU = graphNNA = graphNJP = GraphNOther = graphNGS = df.loc[mask]

    graphNEU = graphNEU.groupby(['EU_Sales'])['Global_Sales'].sum().reset_index()
    graphNNA = graphNNA.groupby(['NA_Sales'])['Global_Sales'].sum().reset_index()
    graphNJP = graphNJP.groupby(['JP_Sales'])['Global_Sales'].sum().reset_index()
    GraphNOther = GraphNOther.groupby(['Other_Sales'])['Global_Sales'].sum().reset_index()
    graphNGS = graphNGS.groupby(['Global_Sales']).sum().reset_index()
    
    value1 = graphNEU['Global_Sales'].max()
    name1 = graphNEU.loc[graphNEU['Global_Sales'].idxmax()]['EU_Sales']

    value2 = graphNNA['Global_Sales'].max()
    name2 = graphNNA.loc[graphNNA['Global_Sales'].idxmax()]['NA_Sales']

    value3 = graphNJP['Global_Sales'].max()
    name3 = graphNJP.loc[graphNJP['Global_Sales'].idxmax()]['JP_Sales']

    value4 = GraphNOther['Global_Sales'].max()
    name4 = GraphNOther.loc[GraphNOther['Global_Sales'].idxmax()]['Other_Sales']

    value5 = graphNGS['Global_Sales'].max()
    name5 = graphNGS.loc[graphNGS['Global_Sales'].idxmax()]


    fig1 = go.Figure()
    fig2 = go.Figure()
    fig3 = go.Figure()
    fig4 = go.Figure()
    fig5 = go.Figure()

    fig1.add_trace(go.Indicator(
        mode = "number",
        value = value1,
        number = {'valueformat': '.2f'}
    ))

    fig2.add_trace(go.Indicator(
        mode = "number",
        value = value2,
        number = {'valueformat': '.2f'}
    ))

    fig3.add_trace(go.Indicator(
        mode = "number",
        value = value3,
        number = {'valueformat': '.2f'}
    ))

    fig4.add_trace(go.Indicator(
        mode = "number",
        value = value4,
        number = {'valueformat': '.2f'}
    ))

    fig5.add_trace(go.Indicator(
        mode = "number",
        value = value1 + value2 + value3 + value4,
        number = {'valueformat': '.2f'}
    ))

    fig1.update_layout(main_config, height=150)
    fig2.update_layout(main_config, height=150)
    fig3.update_layout(main_config, height=150)
    fig4.update_layout(main_config, height=150)
    fig5.update_layout(main_config, height=150)


    return fig1, fig2, fig3, fig4, fig5