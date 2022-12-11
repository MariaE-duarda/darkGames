from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_templates as dbt
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import calendar
from globals import *
from plotly.subplots import make_subplots
from app import app
from dash_bootstrap_templates import ThemeSwitchAIO

template_theme1 = "bootstrap"
template_theme2 = "darkly"
url_theme1 = dbc.themes.BOOTSTRAP
url_theme2 = dbc.themes.DARKLY

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

# === Tratamento dos dados === #
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

df_plaforma = df.groupby('Platform').sum().reset_index().head(5)
publicados_fig_pizza = px.pie(
    df_plaforma, values='Global_Sales', 
    names='Platform', hole=.3
)

# =========  Layout  =========== #
layout = dbc.Col([
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
                ], style={'margin-bottom':'10px', 'margin-top':'10px'}, className='card')
            ])
        ]),
        dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H5('Filtro por Gênero'),
                dbc.RadioItems(
                    id="radio-genre",
                    options=[{"label": x, "value": x} for x in global_genres],
                    value='Global',
                    inline=True,
                    labelCheckedClassName="text-success",
                    inputCheckedClassName="border border-success bg-success",
                ),
            ], style={'padding':'10px'}, className='card')
        ], width=4),
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='graph0', className='dbc', config={"displayModeBar": False, "showTips": False}),
                dbc.Button("Abrir modal", id="open", n_clicks=0, style={'border':'none', 'border-radius':'5px', 'margin-top':'5px'}),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Gráficos de pizza:")),
                        dbc.ModalBody(dcc.Graph(id='graph01', className='dbc', config={"displayModeBar": False, "showTips": False})),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Fechar", id="close", className="ms-auto", n_clicks=0, style={'border-radius':'5px'}
                            )
                        ),
                    ],
                    id="modal",
                    size="xl",
                    is_open=False,
                ),
            ], style={'padding':'10px', 'padding-left':'20px'}),
        ], width=8, style={'margin-bottom':'10px'}),
       ]),
        dbc.Row([
        dbc.Col([
            dbc.Card([
                dcc.Tabs([
            dcc.Tab(label='Geral', children=[
                dcc.Graph(id='graph2', className='dbc', config={"displayModeBar": False, "showTips": False}),
                dbc.Button("Abrir modal", id="open2", n_clicks=0, style={'border':'none', 'border-radius':'5px', 'width':'95%', 'margin-left':'10px', 'margin-top':'5px', 'margin-bottom':'10px'}),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle("Gráfico geral:")),
                            dbc.ModalBody(dcc.Graph(id='graph02', className='dbc', config={"displayModeBar": False, "showTips": False})),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Fechar", id="close2", className="ms-auto", n_clicks=0, style={'border-radius':'5px'}
                                )
                            ),
                        ],
                        id="modal2",
                        size="xl",
                        is_open=False,
                    ),
            ], style={'color':'white', 'background-color':'#181D3135'}),
        dcc.Tab(label='Plataforma', children=[
            dcc.Graph(id='graph5', className='dbc', config={"displayModeBar": False, "showTips": False}, animate=True),
            dbc.Button("Abrir modal", id="open3", n_clicks=0, style={'border':'none', 'border-radius':'5px', 'width':'95%', 'margin-left':'10px', 'margin-top':'5px', 'margin-bottom':'10px'}),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle("Gráfico de barras vertical:")),
                            dbc.ModalBody(dcc.Graph(id='graph05', className='dbc', config={"displayModeBar": False, "showTips": False})),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Fechar", id="close3", className="ms-auto", n_clicks=0, style={'border-radius':'5px'}
                                )
                            ),
                        ],
                        id="modal3",
                        size="xl",
                        is_open=False,
                    ),

        ], style={'color':'white', 'background-color':'#181D3135'}),
    ], style={'font-size':'16px', 'font-weight':'bold'}),          
            ], style={'margin-top':'-100px'}, className='card')
        ], width=4),
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='graph3', className='dbc',  config={"displayModeBar": False, "showTips": False})
            ], style={'height':'220px'})
        ], width=4, style={'height':'200px'}),
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='graph4', className='dbc',  config={"displayModeBar": False, "showTips": False})
            ], style={'height':'220px'})
        ], width=4, style={'height':'200px'}),
       ]),
    ])

# =========  Callbacks  =========== #
@app.callback(
    Output('graph0', 'figure'),
    Input('rangeslider', 'value'),
    Input('radio-genre', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")

)
def graph0(date, radio, toggle):
    template = template_theme1 if toggle else template_theme2

    if radio == 'Global':
        mask = (df['Year'] >= date[0]) & (df['Year'] <= date[1])
    else:
        mask = (df['Year'] >= date[0]) & (df['Year'] <= date[1]) & (df['Genre'].isin([radio]))
    
    df_subplot = df.loc[mask]

    df_NA = df_subplot.sort_values(by='NA_Sales', ascending=False).head(5).rename(columns = {'NA_Sales': 'Sales'})
    df_EU = df_subplot.sort_values(by='EU_Sales', ascending=False).head(5).rename(columns = {'EU_Sales': 'Sales'})
    df_JP = df_subplot.sort_values(by='JP_Sales', ascending=False).head(5).rename(columns = {'JP_Sales': 'Sales'})
    df_Other = df_subplot.sort_values(by='Other_Sales', ascending=False).head(5).rename(columns = {'Other_Sales': 'Sales'})

    subplot_topgames = make_subplots(rows=1, cols=4, specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}, {"type": "pie"}]],  subplot_titles=("América do Norte", "Europa", "Japão", "Outras Regiões"))

    night_colors = ['rgb(56, 75, 126)', 'rgb(18, 36, 37)', 'rgb(34, 53, 101)',
            'rgb(36, 55, 57)', 'rgb(6, 4, 4)', 'rgb(50, 80, 100)', 'rgb(40, 50, 70)', 'rgb(10, 45, 70)', 'rgb(20, 80, 126)']

    subplot_topgames.add_trace(go.Pie(
        labels=df_NA['Name'], values=df_NA['Sales'], hole=.2, marker_colors=night_colors), row=1, col=1)
    subplot_topgames.add_trace(go.Pie(
        labels=df_EU['Name'], values=df_EU['Sales'], hole=.2, marker_colors=night_colors), row=1, col=2)
    subplot_topgames.add_trace(go.Pie(
        labels=df_JP['Name'], values=df_JP['Sales'], hole=.2, marker_colors=night_colors), row=1, col=3)
    subplot_topgames.add_trace(go.Pie(
        labels=df_Other['Name'], values=df_Other['Sales'], hole=.2, marker_colors=night_colors), row=1, col=4)

    subplot_topgames.update_layout(margin={"l":0, "r":0, "t":20, "b":0}, height=200, template=template)

    return subplot_topgames

@app.callback(
    Output('graph01', 'figure'),
    Input('rangeslider', 'value'),
    Input('radio-genre', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")

)
def graph01(date, radio, toggle):
    template = template_theme1 if toggle else template_theme2

    if radio == 'Global':
        mask = (df['Year'] >= date[0]) & (df['Year'] <= date[1])
    else:
        mask = (df['Year'] >= date[0]) & (df['Year'] <= date[1]) & (df['Genre'].isin([radio]))
    
    df_subplot = df.loc[mask]

    df_NA = df_subplot.sort_values(by='NA_Sales', ascending=False).head(5).rename(columns = {'NA_Sales': 'Sales'})
    df_EU = df_subplot.sort_values(by='EU_Sales', ascending=False).head(5).rename(columns = {'EU_Sales': 'Sales'})
    df_JP = df_subplot.sort_values(by='JP_Sales', ascending=False).head(5).rename(columns = {'JP_Sales': 'Sales'})
    df_Other = df_subplot.sort_values(by='Other_Sales', ascending=False).head(5).rename(columns = {'Other_Sales': 'Sales'})

    subplot_topgames = make_subplots(rows=1, cols=4, specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}, {"type": "pie"}]],  subplot_titles=("América do Norte", "Europa", "Japão", "Outras Regiões"))
    
    night_colors = ['rgb(56, 75, 126)', 'rgb(18, 36, 37)', 'rgb(34, 53, 101)',
            'rgb(36, 55, 57)', 'rgb(6, 4, 4)', 'rgb(50, 80, 100)', 'rgb(40, 50, 70)', 'rgb(10, 45, 70)', 'rgb(20, 80, 126)']

    subplot_topgames.add_trace(go.Pie(
        labels=df_NA['Name'], values=df_NA['Sales'], hole=.2, marker_colors=night_colors), row=1, col=1)
    subplot_topgames.add_trace(go.Pie(
        labels=df_EU['Name'], values=df_EU['Sales'], hole=.2, marker_colors=night_colors), row=1, col=2)
    subplot_topgames.add_trace(go.Pie(
        labels=df_JP['Name'], values=df_JP['Sales'], hole=.2, marker_colors=night_colors), row=1, col=3)
    subplot_topgames.add_trace(go.Pie(
        labels=df_Other['Name'], values=df_Other['Sales'], hole=.2, marker_colors=night_colors), row=1, col=4)

    subplot_topgames.update_layout(margin={"l":0, "r":0, "t":20, "b":0}, height=200, template=template)

    return subplot_topgames

@app.callback(
    Output('graph3', 'figure'),
    Output('graph4', 'figure'),
    Input('rangeslider', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")

)
def ind1(date, toggle):    
    template = template_theme1 if toggle else template_theme2
    mask = (df['Year'] >= date[0]) & (df['Year'] <= date[1])

    df_graph3 = df_graph4 = df.loc[mask]

    df_graph3 = df_graph3.groupby(['Publisher'])['Global_Sales'].sum().reset_index()
    df_graph4 = df_graph4.groupby(['Genre'])['Global_Sales'].sum().reset_index()
    
    value1 = df_graph3['Global_Sales'].max()
    name1 = df_graph3.loc[df_graph3['Global_Sales'].idxmax()]['Publisher']

    value2 = df_graph4['Global_Sales'].max()
    name2 = df_graph4.loc[df_graph4['Global_Sales'].idxmax()]['Genre']

    fig1 = go.Figure()
    fig2 = go.Figure()
    
    fig1.add_trace(go.Indicator(
        mode = "number",
        title = {"text": f"<span style='font-size:150%'> Editor top 1 - {name1}</span><br><span style='font-size:70%'>Em milhões de dólares ($)</span><br><span style='font-size:0.7em'>{date[0]} - {date[1]}</span>"},
        value = value1,
        number = {'valueformat': '.2f'}
    ))

    fig2.add_trace(go.Indicator(
        mode = "number",
        title = {"text": f"<span style='font-size:150%'>Gênero top 1 - {name2}</span><br><span style='font-size:70%'>Em milhões de dólares ($)</span><br><span style='font-size:0.7em'>{date[0]} - {date[1]}</span>"},
        value = value2,
        number = {'valueformat': '.2f'}
    ))

    fig1.update_layout(main_config, height=273, template=template)
    fig2.update_layout(main_config, height=273, template=template)

    return fig1, fig2

@app.callback(
    Output('graph2', 'figure'),
    Input('rangeslider', 'value'),
    Input('radio-genre', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")

)
def long(date, radio, toggle):
    template = template_theme1 if toggle else template_theme2

    if radio == 'Global':
        mask = (df['Year'] >= date[0]) & (df['Year'] <= date[1])
    else:
        mask = (df['Year'] >= date[0]) & (df['Year'] <= date[1]) & (df['Genre'].isin([radio]))

    df_anos = df.loc[mask]

    trace = df_anos.groupby('Year')['Global_Sales'].sum().reset_index()

    fig_anos = go.Figure(go.Scatter(x=trace['Year'], y=trace['Global_Sales'], mode='lines+markers', fill='tonexty', name='Global Sales'))
    fig_anos.update_layout(main_config, height=200, xaxis={'title': None}, yaxis={'title': None}, template=template)

    fig_anos.add_annotation(text=f'Vendas em milhões de {date[0]} a {date[1]}',
        xref="paper", yref="paper",
        font=dict(
            size=20,
            color='gray'
            ),
        align="center", opacity=0.8,
        x=0.05, y=0.85, showarrow=False)

    return fig_anos

@app.callback(
    Output('graph02', 'figure'),
    Input('rangeslider', 'value'),
    Input('radio-genre', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")

)
def long(date, radio, toggle):
    template = template_theme1 if toggle else template_theme2

    if radio == 'Global':
        mask = (df['Year'] >= date[0]) & (df['Year'] <= date[1])
    else:
        mask = (df['Year'] >= date[0]) & (df['Year'] <= date[1]) & (df['Genre'].isin([radio]))

    df_anos = df.loc[mask]

    trace = df_anos.groupby('Year')['Global_Sales'].sum().reset_index()

    fig_anos = go.Figure(go.Scatter(x=trace['Year'], y=trace['Global_Sales'], mode='lines+markers', fill='tonexty', name='Global Sales'))
    fig_anos.update_layout(main_config, height=200, xaxis={'title': None}, yaxis={'title': None}, template=template)

    fig_anos.add_annotation(text=f'Vendas em milhões de {date[0]} a {date[1]}',
        xref="paper", yref="paper",
        font=dict(
            size=20,
            color='gray'
            ),
        align="center", opacity=0.8,
        x=0.05, y=0.85, showarrow=False)

    return fig_anos


@app.callback(
    Output('graph5', 'figure'),
    Input('rangeslider', 'value'),
    Input('radio-genre', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")

)
def fig1(date, radio, toggle):
    template = template_theme1 if toggle else template_theme2
    if radio == 'Global':
        mask = (df['Year'] >= date[0]) & (df['Year'] <= date[1])
    else:
        mask = (df['Year'] >= date[0]) & (df['Year'] <= date[1]) & (df['Genre'].isin([radio]))
    
    
    #radio = 'Action'
    #date = [1980, 2017]
    
    
    df_topglobal = df.loc[mask]
    df_topglobal = df_topglobal.head(7).sort_values(by='Global_Sales', ascending=True)
    text = [f'{x} - U${y} milhões' for x,y in zip(df_topglobal['Name'].unique(), df_topglobal['Global_Sales'].unique())]

    fig = go.Figure(go.Bar(x=df_topglobal['Global_Sales'], y=df_topglobal['Name'], orientation='h', marker_color='rgb(55, 83, 109)', text=text))
    fig.update_layout(main_config, height=250, xaxis={'title': None, 'showticklabels':False}, yaxis={'title': None, 'showticklabels':False}, template=template)
    return fig

@app.callback(
    Output('graph05', 'figure'),
    Input('rangeslider', 'value'),
    Input('radio-genre', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")

)
def fig1(date, radio, toggle):
    template = template_theme1 if toggle else template_theme2

    if radio == 'Global':
        mask = (df['Year'] >= date[0]) & (df['Year'] <= date[1])
    else:
        mask = (df['Year'] >= date[0]) & (df['Year'] <= date[1]) & (df['Genre'].isin([radio]))
    
    
    #radio = 'Action'
    #date = [1980, 2017]
    
    
    df_topglobal = df.loc[mask]
    df_topglobal = df_topglobal.head(7).sort_values(by='Global_Sales', ascending=True)
    text = [f'{x} - U${y} milhões' for x,y in zip(df_topglobal['Name'].unique(), df_topglobal['Global_Sales'].unique())]

    fig = go.Figure(go.Bar(x=df_topglobal['Global_Sales'], y=df_topglobal['Name'], orientation='h', marker_color='rgb(55, 83, 109)', text=text))
    fig.update_layout(main_config, height=410, xaxis={'title': None, 'showticklabels':False}, yaxis={'title': None, 'showticklabels':False}, template=template)
    return fig

@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("modal2", "is_open"),
    [Input("open2", "n_clicks"), Input("close2", "n_clicks")],
    [State("modal2", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("modal3", "is_open"),
    [Input("open3", "n_clicks"), Input("close3", "n_clicks")],
    [State("modal3", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open