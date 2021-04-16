import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
import plotly.express as px

import numpy as np
import pandas as pd

import geopandas as gpd

import json
import os
import zipfile

from tensorflow.keras.utils import get_file

list_dia_semana = ['dom', 'seg', 'ter', 'qua', 'qui', 'sex', 'sab']

# Load file
def load_dataset(fZipName):
    zf = zipfile.ZipFile('./data/' + fZipName  + '.zip') 
    df = pd.read_csv(zf.open( fZipName + '.csv'), sep=';')
   
    # Prepoc datetime
    cat_dia_semana = pd.CategoricalDtype(categories= list_dia_semana , ordered=True)
    df['data'] = pd.to_datetime(df['data'],format="%Y-%m-%d")
    df['dia_semana'] = df['data'].dt.dayofweek
    df['dia_semana_nm'] = df['dia_semana'].replace({0:'seg', 1: 'ter', 2:'qua', 3:'qui', 4:'sex', 5:'sab', 6:'dom'}).astype(cat_dia_semana)
    return df

###

df = load_dataset('HIST_PAINEL_COVIDBR_15abr2021')


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


#### Para mapas
def preproc_comp_cidades(df1,estados, cidades):
    df1.sort_values('data', inplace = True)
    listDFs = []
    for i in range(len(estados)):
        # filtrando por estado
        fltr = df1['estado'].str.lower() == estados[i].lower()
        df_UF = df1.loc[fltr, :]
        # filtrando pro cidade
        fltr = df_UF['municipio'].str.lower() == cidades[i].lower()
        df_muni = df_UF.loc[fltr, :]

        ###
        #estado
        df_UF.dropna(subset=['municipio'])
        # esrado por município
        df_UF_muni = df_UF.groupby('municipio')
         # população do estado somatório dos municípios
        agg_estado = df_UF_muni.agg({'populacaoTCU2019': 'max', 'casosAcumulado': 'max'}).reset_index()
        popu_estado = agg_estado['populacaoTCU2019'].sum()
        casos_estado = agg_estado['casosAcumulado'].sum()
        
        df_UF_muni = df_UF_muni.agg({'populacaoTCU2019': 'max', 'casosAcumulado': 'max', 'obitosAcumulado': 'max',  }).reset_index()
        # estado por município, valores por 100 mil habitantes
        df_UF_muni['CA_por_cemMil_Hab'] = df_UF_muni['casosAcumulado'] * 10**5 / df_UF_muni['populacaoTCU2019']
        df_UF_muni['OA_por_cemMil_Hab'] = df_UF_muni['obitosAcumulado'] * 10**5 / df_UF_muni['populacaoTCU2019']
        df_UF_muni['CA_cemMil_log'] = df_UF_muni['CA_por_cemMil_Hab'].apply(lambda x: np.log10(x))
        df_UF_muni['OA_cemMil_log'] = df_UF_muni['OA_por_cemMil_Hab'].apply(lambda x: np.log10(x))

       
        print('População: somatório dos municípios do estado {} : {} '.format(estados[i], popu_estado))
        print('Casos: somatório dos municípios do estado {} : {} '.format(estados[i], casos_estado))
        print('Casos por cem mil habintnates do estado {} : {} '.format(estados[i], casos_estado*10**5/popu_estado))

        # totalização dos casos do estado
        df_UF = df_UF.groupby('data')
        df_UF = df_UF.agg({'casosNovos': sum, 'obitosNovos': sum, 'casosAcumulado': sum, 'obitosAcumulado': sum,'populacaoTCU2019': 'max'}).reset_index()
        df_UF['CN_por_cemMil_Hab'] = df_UF['casosNovos'] * 10**5 / popu_estado
        df_UF['ON_por_cemMil_Hab'] = df_UF['obitosNovos'] * 10**5 / popu_estado
        df_UF['CA_por_cemMil_Hab'] = df_UF['casosAcumulado'] * 10**5 / popu_estado
        df_UF['OA_por_cemMil_Hab'] = df_UF['obitosAcumulado'] * 10**5 / popu_estado

        ## dias a partir da primeira notificação
        dia_0 = df_UF['data'].min()
        df_UF['dia_num'] = (df_UF['data'] - dia_0).apply(lambda x: x.days)
        
        ###
        #cidades

        print('população da cidade de {}: {}'.format(cidades[i], df_muni['populacaoTCU2019'].max() ))
        df_muni['CN_por_cemMil_Hab'] = df_muni['casosNovos'] * 10**5 / df_muni['populacaoTCU2019']
        df_muni['ON_por_cemMil_Hab'] = df_muni['obitosNovos'] * 10**5 / df_muni['populacaoTCU2019']
        df_muni['CA_por_cemMil_Hab'] = df_muni['casosAcumulado'] * 10**5 / df_muni['populacaoTCU2019']
        df_muni['OA_por_cemMil_Hab'] = df_muni['obitosAcumulado'] * 10**5 / df_muni['populacaoTCU2019']

        # escala logarítimica
        df_muni['CN_cemMil_log'] = df_muni['CN_por_cemMil_Hab'].apply(lambda x: np.log10(x))
        df_muni['ON_cemMil_log'] = df_muni['ON_por_cemMil_Hab'].apply(lambda x: np.log10(x))
        df_muni['CA_cemMil_log'] = df_muni['CA_por_cemMil_Hab'].apply(lambda x: np.log10(x))
        df_muni['OA_cemMil_log'] = df_muni['OA_por_cemMil_Hab'].apply(lambda x: np.log10(x))
        ## dias a partir da primeira notificação
        dia_0 = df_muni['data'].min()
        df_muni['dia_num'] = (df_muni['data'] - dia_0).apply(lambda x: x.days)

        #lista de saida
        listDFs.append(df_UF)
        listDFs.append(df_UF_muni)
        listDFs.append(df_muni)
           
    return listDFs

app = dash.Dash()



app.layout = html.Div(

    [
        html.H1('Gráficos COVID'),
        html.Div([
        html.H2('Selecione estado e cidade: ', style={'text-align': 'left'}),

        dcc.Dropdown(id='uf_picker' ,
            options= [{'label': estado , 'value':  estado } for estado in list(dictUfMuni.keys()) ],
            value='BA', style={'width': '50%', 'align': 'left'}),
        dcc.Dropdown(id='muni_picker',
            value = "Salvador", style={'width': '50%',  'align': 'left'})],
            style = {'align': 'left'}
            ), 
        html.Div([dcc.Graph(id='casos_mm_fig'),
        dcc.Graph(id='obitos_mm_fig'),  dcc.Graph(id='mapa_casos')]
       )
    
            ], style={'text-align': 'left'})


@app.callback(
    Output('muni_picker', 'options'),
    [Input('uf_picker', 'value')]
)
def update_date_dropdown(uf):
    return [{'label': i, 'value': i} for i in dictUfMuni[uf]]



@app.callback(
    Output('casos_mm_fig', 'figure'),
    [Input('uf_picker', 'value'), dash.dependencies.Input('muni_picker', 'value') ]
)
def update_casos_mm_fig(uf, cidade):
    df2,  df1 = preproc_filter_df(uf, cidade)
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
    df2,  df1 = preproc_filter_df(uf, cidade)
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


@app.callback(
    Output('mapa_casos', 'figure'),
    [Input('uf_picker', 'value'), Input('muni_picker', 'value')]
)
def mapacasos(uf, cidade):
    df2,  df1 = preproc_filter_df(uf, cidade)
    url = "https://raw.githubusercontent.com/luizpedone/municipal-brazilian-geodata/master/data/"
    fname = uf.upper() + '.json'
    path = os.path.abspath(os.getcwd())
    path = path + '\geojsonDL'
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    filepath = path + '\\' + fname
    get_file(filepath, url+fname )
    gp_mapa= gpd.read_file( filepath, driver='GeoJSON')
    gp_mapa = gp_mapa.to_crs({'init': 'epsg:4326'})
    LatLon_path = path + '\\' + 'LatLon' + fname
    gp_mapa.to_file(LatLon_path, driver = "GeoJSON",  encoding='utf8')
    with open(LatLon_path, encoding='utf8') as geofile:
        geojson_layer = json.load(geofile)
    lon_map = gp_mapa.unary_union.centroid.x
    lat_map = gp_mapa.unary_union.centroid.y
    df_est1, df_est1_muni, df_cidade1 = preproc_comp_cidades(df, uf, cidade)
    fig = px.choropleth_mapbox(df_est1_muni, geojson=geojson_layer, locations='municipio', featureidkey = 'properties.NOME',
                        color='CA_por_cemMil_Hab',
                           color_continuous_scale="ylorbr",
                           range_color=(0, df_est1_muni['CA_por_cemMil_Hab'].max()),
                           mapbox_style="carto-positron",
                           zoom=4,
                           center = {'lat': lat_map, 'lon': lon_map},
                           opacity=0.5,
                           labels={'CA_por_cemMil_Hab':'Casos Acumulados/100Mil hab.'}
                          )
    return fig

    


if __name__ == '__main__':
    app.run_server()