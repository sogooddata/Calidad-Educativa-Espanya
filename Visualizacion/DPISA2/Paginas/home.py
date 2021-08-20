import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
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

comunidadest = {"Andalucía":1,"Aragón":2,"Asturias":3,"Baleares":4,"Canarias":5,"Cantabría":6,"Castilla y León":7,"Castilla y La Mancha":8,"Cataluña":9,"Extremadura":10,"Galicia":11,"La Rioja":12,"Madrid":13,"Murcia":14,"Navarra":15,"País Vasco":16,"Comunidad Valenciana":17,"Ceuta":18,"Melilla":19}
comunidades = {'01':"Andalucía",'02':"Aragón",'03':"Asturias",'04':"Baleares",'05':"Canarias",'06':"Cantabría",'07':"Castilla y León",'08':"Castilla y La Mancha",'09':"Cataluña",'10':"Extremadura",'11':"Galicia",'12':"La Rioja",'13':"Madrid",'14':"Murcia",'15':"Navarra",'16':"País Vasco",'17':"Comunidad Valenciana",'18':"Ceuta",'19':"Melilla"}
#VCCA = VCCA.replace({"CCAA": comunidades})

controls = dbc.CardBody(children=[
   html.H5("Datos por la Educación (DxE) es un cuadro de mando que permite ver la información del informe PISA, realizado por la OCDE, u otras evaluaciones educativas junto con datos proporcionados por datos.gob.es de ámbito socioeconómico, demográfico, educativo o científico. El objetivo es detectar qué aspectos favorecen el incremento del rendimiento académico utilizando un modelo de machine learning, de tal forma que se pueda llevar a cabo una toma de decisiones eficaz. La idea es que los propios centros educativos e instituciones públicas puedan adaptar sus recursos, prácticas y currículos educativos hacia las necesidades de aprendizaje del alumnado para garantizar un mayor éxito. Esta aplicación utiliza diversos datos abiertos del INE, del Ministerio de Educación y Formación Profesional o de PISA España."),html.P(style={"line-height":"1px"}),
   html.H5("La herramienta se divide en las siguientes secciones:"),html.P(style={"line-height":"1px"}),
   html.H5("-  Tres secciones de gráficos de los cuestionarios PISA para el alumnado, los centros educativos y el profesorado"),html.P(style={"line-height":"1px"}),
   html.H5("-  Una sección para comparar distintas variables socioeconómicas con las competencias medidas es el Informe PISA"),html.P(style={"line-height":"1px"}),
   html.H5("-  Una herramienta de simulación mediante un modelo ML, para predecir como podría cambiar la competencía global de las escuelas modificando ciertas categorías basadas en preguntas de los cuestionarios PISA"),html.Br(style={"line-height":"22px"}),
],
   className = 'texto_cab'
    )

fmap = px.choropleth_mapbox(VCCA, geojson=gson, locations='CCAA', color='Competencia Global  (PISA)',
                               featureidkey="properties.id",
                               color_continuous_scale="Viridis",
#                               range_color=(cal[variable].min(), cal[variable].max()),
                               hover_name = 'Literal',
                               mapbox_style="carto-positron",
                               zoom=4, center={"lat": 40.4167, "lon": -3.70325},
                               opacity=0.5,
                               labels={'GLOBAL1': 'Competencía Global'}
                               )
fmap.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fmap.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

variim = ['Competencia en Matemáticas (PISA)', 'Competencia en Ciencias  (PISA)', 'Competencia Lengua  (PISA)', 'Competencia Global  (PISA)']

fig = px.bar(VCCA[variim].T, x=VCCA[variim].T.index, y=0, color=VCCA[variim].T.index, title='Andalucía',         range_y = [400, 600])


fig.add_trace(
    go.Scatter(
        x=VCCA[variim].T.index,
        y=VCCA[variim].mean(),
        name='Media de España'

    ))


layout = dbc.Container(
    fluid=True,
    style={"height": "100vh","width": "100%",},
    children=[
                dbc.Row(children=
                    [
                        dbc.Row(className='twelve columns pretty_container',
                            children=dbc.Card(
                                        [dbc.CardHeader(html.H3("Proyecto"),className='texto_cab'), controls,]
                       ),
                       ),
                        dbc.Row( className='twelve columns pretty_container',
                            children=dbc.Card(className='twelve columns pretty_container',children=
                                [
                                    dbc.CardHeader(html.H3("Competencias por comunidades")),
                                    dbc.CardBody(html.H4("Grafica resumen donde se puede visualizar las competencias que miden los cuestionarios PISA por cada comunidad (pinchar en la comunidad deseada para ver los datos)")),
                                    dbc.CardBody(className="w-100 mb-3",
                                        children=[
                                                          dcc.Graph(id='fmap',figure=fmap),
                                                          dcc.Graph(id='GEstu',figure=fig)
                                                          ]
                                                 )
                                ]
                                              )
                                ),

                    ]
                        )

             ]
             )


##Callback Resetea y carga los valores de las barras
@app.callback(
    Output('GEstu', 'figure'),
    Input( 'fmap', 'clickData'),prevent_initial_call=True
    )

def Gra_Estu(Cvalor):

    comu = Cvalor.get('points')[0].get('location')
    comuT = Cvalor.get('points')[0].get('hovertext')

    variim = ['Competencia en Matemáticas (PISA)', 'Competencia en Ciencias  (PISA)', 'Competencia Lengua  (PISA)', 'Competencia Global  (PISA)']
    #print(VCCA.columns())
    #print(VCCA[variim].T.index)
    print(Cvalor)

    #fig = px.bar(VCCA[variim].T, x=VCCA[variim], y=int(comu), color=VCCA['CCAA'], title=comuT, range_y = [400, 600])
    fig = px.bar(VCCA[variim].T, x=VCCA[variim].T.index, y=int(comu)-1, color=VCCA[variim].T.index, title=comuT,
                 range_y=[400, 600])

    fig.add_trace(
        go.Scatter(
            x=VCCA[variim].T.index,
            y=VCCA[variim].mean(),
            name='Media de España'

        ))

    return fig

