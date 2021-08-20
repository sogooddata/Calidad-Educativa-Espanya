import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_table
from dash.dependencies import Input, Output
#import pyreadstat
import json
from app import app
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


VCCA = pd.read_csv("data/compe.csv", na_values = ["NaN", "NaN"], sep = ";")
VCCA['CCAA'] = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19']

gson = json.loads(open('data/georef-spain-comunidad-autonoma.geojson').read())



comunidades = {"Andalucía":1,"Aragón":2,"Asturias":3,"Baleares":4,"Canarias":5,"Cantabría":6,"Castilla y León":7,"Castilla y La Mancha":8,"Cataluña":9,"Extremadura":10,"Galicia":11,"La Rioja":12,"Madrid":13,"Murcia":14,"Navarra":15,"País Vasco":16,"Comunidad Valenciana":17,"Ceuta":18,"Melilla":19}
comunidadest = {'01':"Andalucía",'02':"Aragón",'03':"Asturias",'04':"Baleares",'05':"Canarias",'06':"Cantabría",'07':"Castilla y León",'08':"Castilla y La Mancha",'09':"Cataluña",'10':"Extremadura",'11':"Galicia",'12':"La Rioja",'13':"Madrid",'14':"Murcia",'15':"Navarra",'16':"País Vasco",'17':"Comunidad Valenciana",'18':"Ceuta",'19':"Melilla"}

VCCA = VCCA.replace({"CCAA": comunidadest})

controls = dbc.CardBody(
   html.H5("Gráfico interactivo donde se pueden cruzar a nivel de CC.AA. los datos de las distintas competencias que mide PISA (Global, Ciencias, Lectura y Matemáticas), con diferentes datos socioeconómicos de DATOS.GOB.ES"),
    className = 'texto_cab'
    )
vari = {'Competencia en Matemáticas (PISA)':'Competencia en Matemáticas (PISA)',
        'Competencia en Ciencias  (PISA)' :'Competencia en Ciencias  (PISA)',
        'Competencia Lengua  (PISA)': 'Competencia Lengua  (PISA)',
        'Competencia Global  (PISA)':'Competencia Global  (PISA)',
        'Vandalismo (DATOS.GOB.ES)':'Vandalismo (DATOS.GOB.ES)',
        'Tasa de Empleo(DATOS.GOB.ES)':'Tasa de Empleo(DATOS.GOB.ES)',
        'Tasa de Paro(DATOS.GOB.ES)':'Tasa de Paro(DATOS.GOB.ES)',
        'PIB per Capita':'PIB per Capita',
        'Nº medio de alumnos por profesor (Todos los centros)':'Nº medio de alumnos por profesor (Todos los centros)',
        'Nº medio de alumnos por profesor (Centros públicos)':'Nº medio de alumnos por profesor (Centros públicos)',
        'Nº medio de alumnos por profesor (Centros privados)':'Nº medio de alumnos por profesor (Centros privados)',
        'Abandono temprano de la educación-formación en la población de 18 a 24 años (%)':'Abandono temprano de la educación-formación en la población de 18 a 24 años (%)',
        'Sentimiento de felicidad en las cuatro últimas semanas (%) Muy a menudo':'Sentimiento de felicidad en las cuatro últimas semanas (%) Muy a menudo',
        'Sentimiento de felicidad en las cuatro últimas semanas (%) Algunas veces':'Sentimiento de felicidad en las cuatro últimas semanas (%) Algunas veces',
        'Sentimiento de felicidad en las cuatro últimas semanas (%) Nunca':'Sentimiento de felicidad en las cuatro últimas semanas (%) Nunca',
        'Porcentaje de alumnado que supera 4 de la ESO':'Porcentaje de alumnado que supera 4 de la ESO',
        'Porcentaje de alumnado que supera 4 de la ESO (Todas materias superadas)':'Porcentaje de alumnado que supera 4 de la ESO (Todas materias superadas)',
        'Porcentaje de alumnado que supera 4 de la ESO(Con materias no superadas)':'Porcentaje de alumnado que supera 4 de la ESO(Con materias no superadas)',
        'Porcentaje de alumnado que supera Bachillerato':'Porcentaje de alumnado que supera Bachillerato',
        'Porcentaje de alumnado que supera Bachillerato (Todas materias superadas)':'Porcentaje de alumnado que supera Bachillerato (Todas materias superadas)',
        'Porcentaje de alumnado que supera Bachillerato (Con materias no superadas)':'Porcentaje de alumnado que supera Bachillerato (Con materias no superadas)'
        }


Ejex = dbc.Card(className='twelve columns pretty_container', children=
[
    dbc.CardHeader("Variables Eje X"),
    dbc.CardBody(className="w-100 mb-3",
                 children=[html.Br(),
                           dcc.Dropdown(id="EjexS",options=list({"label": param, "value": param} for param in vari.keys()))
                          ]
                 ),
    dbc.CardHeader("Variables Eje Y"),
    dbc.CardBody(className="w-100 mb-3",
                 children=[html.Br(),
                           dcc.Dropdown(id="EjeyS",
                                        options=list({"label": param, "value": param} for param in vari.keys()))
                           ]
                 )
]
                    )


fig = px.scatter(VCCA, y="Competencia en Matemáticas (PISA)", x="Vandalismo (DATOS.GOB.ES)", color="CCAA")

fig.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))


layout = dbc.Container(
    fluid=True,
    style={"height": "100vh","width": "100%",},
    children=[
                dbc.Row(children=
                    [
                        dbc.Row(className='twelve columns pretty_container',
                            children=dbc.Card(
                                        [dbc.CardHeader(children=[html.H4("Gráficas PISA y DATOS.GOB.ES")],className='texto_cab'), controls]
                       )),
                       dbc.Row(className='twelve columns pretty_container',
                            children=Ejex),
                       dbc.Row( className='twelve columns pretty_container',
                            children=dbc.Card(className='twelve columns pretty_container',children=
                                [
                                    dbc.CardHeader("Competencias por comunidades"),
                                        dbc.CardBody(className="w-100 mb-3",
                                        children=[
                                                          dcc.Graph(id='GINE',figure=fig)
                                                          ]
                                                 )
                                ]
                                              )
                                ),

                    ]
                        )

             ]
             )

@app.callback(
    Output("GINE", "figure"),
    [
     Input( 'EjexS', 'value'),Input( 'EjeyS', 'value'),
    ],prevent_initial_call=True
)

def update_charts(V1, V2):
    fig = px.scatter(VCCA, y=V1, x=V2, color="CCAA")
    print(VCCA[V2])

    fig.update_traces(marker=dict(size=12,
                                  line=dict(width=2,
                                            color='DarkSlateGrey')),
                      selector=dict(mode='markers'))
    return fig