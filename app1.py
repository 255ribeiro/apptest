import os
import zipfile

#import patoolib
#import json
#import requests

import numpy as np
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

from read_newest import Read_newest

list_dia_semana = ['dom', 'seg', 'ter', 'qua', 'qui', 'sex', 'sab']


df = Read_newest('./data/')


def preproc_filter_df(estado, cidade):
    fltr = df['estado'].str.lower() == estado.lower()
    df_UF = df.loc[fltr, :]
    fltr = df_UF['municipio'].str.lower() == cidade.lower()
    df_muni = df_UF.loc[fltr, :]
    return df_UF,  df_muni

dictUfMuni = {}
df.sort_values(by= ['estado'], inplace=True)
for i in df['estado'].unique():
    fltr = df['estado'] == i
    df_UF_aux = df.loc[fltr, :]
    df_UF_aux.sort_values(by= ['municipio'], inplace=True)
    aux_list = []
    for j in df_UF_aux['municipio'].unique():
        aux_list.append(j)
    dictUfMuni[i] = aux_list

app = dash.Dash()
app.title = 'Gráficos Covid BR por município'

app.layout = html.Div(

    [  
        html.H1('GRÁFICOS COVID BR', style={'text-align': 'center', 'backgroundColor':'#F2F3F4'}),
        html.Div([
        html.H2('Selecione estado e cidade: ', style={'text-align': 'left'}),

        dcc.Dropdown(id='uf_picker' ,
            options= [{'label': estado , 'value':  estado } for estado in list(dictUfMuni.keys()) ],
            value='BA', style={'width': '50%', 'align': 'left'}),
        dcc.Dropdown(id='muni_picker',
            value = "Salvador", style={'width': '50%',  'align': 'left'})],
            style = {'align': 'left'}
            ),
        html.Br(),

        html.Div([dcc.Graph(id='casos_mm_fig', style={'text-align': 'center'}),
        html.Br(),
        dcc.Graph(id='obitos_mm_fig', style={'text-align': 'center'})], style={'text-align': 'center'}
       )
    
            ], style={'text-align': 'left', })


# dropdown
@app.callback(
    Output('muni_picker', 'options'),
    [Input('uf_picker', 'value')]
)
def update_date_dropdown(uf):
    return [{'label': i, 'value': i} for i in dictUfMuni[uf]]


## Cases graphics
@app.callback(
    Output('casos_mm_fig', 'figure'),
    [Input('uf_picker', 'value'), dash.dependencies.Input('muni_picker', 'value') ]
)
def update_casos_mm_fig(uf, cidade):
    df1 = preproc_filter_df(uf, cidade)[1]
    df1.sort_values('data', inplace = True)
    df1['casosNovos'] = np.absolute(df1['casosNovos'])

    df1['media_movel_casos'] =df1.rolling(7, center=False)['casosNovos'].mean()


#### plotly
    Bar_dia =[]
    cores = ['indianred',   'greenyellow', 'yellowgreen', 'lightseagreen',  'mediumseagreen', 'seagreen',  'tomato']
    for i in range(len(list_dia_semana)):
        fltr = df1['dia_semana_nm'] == list_dia_semana[i]
        df_dia = df1.loc[fltr, :]
        Bar_dia += [go.Bar(x=df_dia['data'] , y=df_dia['casosNovos'] , name = list_dia_semana[i] ,  marker = dict( color = cores[i]) )]



    Line_med_movel = go.Scatter(x = df1['data'], y = df1['media_movel_casos'] , mode='lines+markers', name = 'Media móvel', line=dict( color='darkviolet', width=5),
    marker = dict(size=2 ,   color = 'darkviolet'  ) )

    layout = go.Layout(
        width=1200, height=600,
        title='Covid casos: ' + cidade  + ' ' + str(df1['data'].max()).split(' ', 1 )[0],
        yaxis=dict(
            title_text="Número de casos"
        ),
        xaxis=dict(
            title_text="Data do registro"
        ),
        hovermode = "x"
    )

    data = Bar_dia + [Line_med_movel]
    return {'data': data, 'layout': layout}


@app.callback(
    Output('obitos_mm_fig', 'figure'),
    [Input('uf_picker', 'value'), Input('muni_picker', 'value') ]
)
def update_obitos_mm_fig(uf, cidade):
    df1 = preproc_filter_df(uf, cidade)[1]
    df1.sort_values('data', inplace = True)
    df1['obitosNovos'] = np.absolute(df1['obitosNovos'])
    df1['media_movel_obitos'] =df1.rolling(7, center= False )['obitosNovos'].mean()
    
    #### plotly
    Bar_dia =[]
    cores = ['indianred',   'greenyellow', 'yellowgreen', 'lightseagreen',  'mediumseagreen', 'seagreen',  'tomato']
    for i in range(len(list_dia_semana)):
        fltr = df1['dia_semana_nm'] == list_dia_semana[i]
        df_dia = df1.loc[fltr, :]
        Bar_dia += [go.Bar(x=df_dia['data'] , y=df_dia['obitosNovos'] , name = list_dia_semana[i] ,  marker = dict( color = cores[i]) )]


   
    Line_med_movel = go.Scatter(x = df1['data'], y = df1['media_movel_obitos'] , mode='lines+markers', name = 'Media móvel', line=dict( color='crimson', width=5),
    marker = dict( size=3 , color = 'crimson' )
    
    )

    layout = go.Layout(
        width=1200, height=600,
        title='Covid óbitos: ' + cidade + ' ' + str(df1['data'].max()).split(' ', 1 )[0],
        yaxis=dict( 
            title_text="Número de óbitos"
        ),
        xaxis=dict(
            title_text="Data do registro"
        ),
        hovermode = "x"
    )

    data = Bar_dia + [Line_med_movel]
    return {'data': data, 'layout': layout}

if __name__ == '__main__':
    app.run_server()