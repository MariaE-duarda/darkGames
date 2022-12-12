import os
import dash
from dash import html, dcc, no_update
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash import Input, Output, html, no_update
from app import app
from dash_bootstrap_templates import ThemeSwitchAIO

from datetime import datetime, date
import plotly.express as px
import numpy as np
import pandas as pd

template_theme1 = "bootstrap"
template_theme2 = "darkly"
url_theme1 = dbc.themes.BOOTSTRAP
url_theme2 = dbc.themes.DARKLY

# ========= Layout ========= #
layout = dbc.Col([
    dbc.Card([
        html.H1('Dashboard', style={'text-align':'center'}),
        html.Legend('GAME SALES', style={'text-align':'center'}),
        dbc.Button(id='botao_avatar',
        children=[html.Img(src='/assets/Game-Icon.jpg', id='avatar_change', alt='Avatar', className='perfil_avatar', style={'width':'100%', 'height':'110px', 'border-radius':'10px'} )], 
        style={'background-color':'transparent', 'border-color':'transparent'}),
        html.Button('Acessar código', className='button-git', style={'border':'none', 'background':'#181818', 'color':'white', 'border-radius':'10px', 'width':'80%', 'height':'40px', 'font-size':'18px', 'margin-left':'10%'}, id='simple-toast-toggle', n_clicks=1),
            dbc.Toast(
                dbc.Badge(
                    "GitHub",
                    href="https://github.com/MariaE-duarda/darkGames",
                    color="dark",
                    className="me-1 text-decoration-none badge",
                    style={'width':'200px', 'font-size':'13px', 'border-radius':'5px'}
                ),
                id="simple-toast",
                header="Acesse o link abaixo:",
                dismissable=True,
                is_open=False,
                icon="black",
                # top: 66 positions the toast below the navbar
                style={"position": "fixed", "top": '70vh', "left": 30, "width": 240},
            ),
        html.Hr(),
        html.Legend('Telas de visualização', style={'font-size':'22px', 'margin-top':'5px', 'text-align':'center'}),
        dbc.Nav([
            dbc.NavLink('Tela principal', className='button',href='/dashboardsPrimario', active='exact', style={'border':'none', 'border-radius':'5px', 'background-color':'#181818', 'color':'white', 'height':'35px', 'font-size':'17px', 'width':'80%', 'text-align':'center', 'margin-left':'10%'}),
            dbc.NavLink('Tela secundária', className='button', href='/dashboardsSecundario', active='exact', style={'border':'none', 'border-radius':'5px', 'background-color':'#181818', 'color':'white', 'margin-top':'5px', 'height':'35px', 'font-size':'17px', 'width':'80%', 'text-align':'center', 'margin-left':'10%'}),
            dbc.NavLink('Tela terciária', className='button', href='/dashboardsTerciario', active='exact', style={'border':'none', 'border-radius':'5px', 'background-color':'#181818', 'color':'white', 'margin-top':'5px', 'height':'35px', 'font-size':'17px', 'width':'80%', 'text-align':'center', 'margin-left':'10%'}),
        ]),
        dbc.Card([ 
            ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
     ], style={'padding-left':'30%', 'margin-top':'15px', 'width':'93%', 'border':'none'})
    ], style={'padding':'15px', 'margin-left':'-10px', 'height':'100%'}),
], sm=20, lg=12, style={'height':'97.5vh', 'margin-top':'10px'})

# =========  Callbacks  =========== #
# Pop-up receita
@app.callback(
    Output("simple-toast", "is_open"),
    [Input("simple-toast-toggle", "n_clicks")],
)
def open_toast(n):
    if n == 1:
        return no_update
    return True