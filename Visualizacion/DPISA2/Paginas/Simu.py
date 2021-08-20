import dash
import dash_html_components as html
import pandas as pd
import numpy as np
import pickle
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, MATCH, ALL, State
from app import app
import dash_core_components as dcc
import dash_daq as daq
from joblib import load
import datetime
import time

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}


mode = load('data/Modesc.joblib')

preguntas = pd.read_csv("data/GruPreguntasEST.csv", na_values = ["NaN", "NaN"], sep = ";")

grupos = pd.read_csv("data/GruposEST.csv", na_values = ["NaN", "NaN"], sep = ";")
gruposP = pd.read_csv("data/GruposPRO.csv", na_values = ["NaN", "NaN"], sep = ";")
gruposEs = pd.read_csv("data/GruposESC.csv", na_values = ["NaN", "NaN"], sep = ";")

PRgrupos = pd.read_csv("data/GruPreguntasEST.csv", na_values = ["NaN", "NaN"], sep = ";")
PRgruposP = pd.read_csv("data/GruPreguntasPRO.csv", na_values = ["NaN", "NaN"], sep = ";")
PRgruposEs = pd.read_csv("data/GruPreguntasESC.csv", na_values = ["NaN", "NaN"], sep = ";")

DatosP_EST = pd.read_csv("data/PCAReguntasEST.csv", na_values = ["NaN", "NaN"], sep = ",")
DatosP_PRO = pd.read_csv("data/PCAReguntasPRO.csv", na_values = ["NaN", "NaN"], sep = ",")
DatosP_ESC = pd.read_csv("data/PCAReguntasESC.csv", na_values = ["NaN", "NaN"], sep = ",")

Datamod = pd.read_csv("data/datamod.csv", na_values = ["NaN", "NaN"], sep = ",")

valoEsc = pd.read_csv("data/valoEsc.csv", na_values = ["NaN", "NaN"], sep = ",")

valorig = '--'

a_file = open("data/valuesEst.pkl", "rb")
var_values_Est = pickle.load(a_file)
a_file.close()

a_file = open("data/labelEst.pkl", "rb")
var_labels_Est = pickle.load(a_file)
a_file.close()

a_file = open("data/valuesEsc.pkl", "rb")
var_values_Esc = pickle.load(a_file)
a_file.close()

a_file = open("data/labelEsc.pkl", "rb")
var_labels_Esc = pickle.load(a_file)
a_file.close()

a_file = open("data/valuesPro.pkl", "rb")
var_values_Pro = pickle.load(a_file)
a_file.close()

a_file = open("data/labelPro.pkl", "rb")
var_labels_Pro = pickle.load(a_file)
a_file.close()

comunidades = {"Andalucía":1,"Aragón":2,"Asturias":3,"Baleares":4,"Canarias":5,"Cantabría":6,"Castilla y León":7,"Castilla y La Mancha":8,"Cataluña":9,"Extremadura":10,"Galicia":11,"La Rioja":12,"Madrid":13,"Murcia":14,"Navarra":15,"País Vasco":16,"Comunidad Valenciana":17,"Ceuta":18,"Melilla":19}
tip_escuela = {"Publica":1, "Privada":2}
tip_localidad = {'A village, hamlet or rural area (fewer than 3 000 people)':1, 'A small town (3 000 to about 15 000 people)':2, 'A town (15 000 to about 100 000 people)':3, 'A city (100 000 to about 1 000 000 people)':4, 'A large city (with over 1 000 000 people)':5}


controls = dbc.CardBody(children=[
   html.H5("En esta sección se puede seleccionar uno de los 1036 centros educativos españoles participantes en el Informe PISA según sus características de centro para hacer una simulación sobre aquellos aspectos que influyen en la adquisición de las competencias."),html.P(style={"line-height":"1px"}),
   html.H5("De esta manera, otros centros educativos con características similares y las instituciones públicas pueden comprobar el impacto global que tienen ciertas variables y modificar tanto las políticas públicas educativas con la práctica en los centros educativos."),
   html.H5("Los valores se muestran en una escala de 0 a 1000 que al ir modificándose se actualiza en la competencia global, en base a un modelo de Regresión Lineal.")],
    className = 'texto_cab'
    )


##Grafico resultado
dd = daq.Gauge(id="progress-gauge",
                max=1000,
                min=0,
                 showCurrentValue=True,  # default size 200 pixel
                    )

predi = dbc.Row(children=[dbc.Col(width=6,children=[dbc.CardHeader("Valor Original",className='texto_cab'),
                                                    dbc.Card(html.H1(id='ValOri',children='--')),
                                                    ]),
                          dbc.Col(width=6,children=[dbc.CardHeader("Valor Calculado",className='texto_cab'),
                                                    dbc.Card(html.H1(id='ValNue',children='--'))])], style={"text-align": "center"})

predi2 = dbc.Row(children=[dbc.Col(width=6,children=[dbc.CardHeader("Media España",className='texto_cab'),
                                                    dbc.Card(html.H1(id='ValEsp',children='--'))]),
                          dbc.Col(width=6,children=[dbc.CardHeader("Media Comunidad",className='texto_cab'),
                                                    dbc.Card(html.H1(id='ValCom',children='--'))])], style={"text-align": "center"})


Variables = dbc.Row(children=[dbc.Col(width=12,children=[dbc.CardHeader("Composición Variables"),
                                                        dbc.Card(children=[html.H1(id='varicom2'),
                                                                 html.Ol(id='varicom',children='--', )])])])




## Construye selección
def build_selec():
    return [
        # Manually select metrics
        html.Div(
            id="set-specs-intro-container",
            children=html.P(
                "Elegir las características de la escuela, para seleccionar una de ejemplo"
            ),
        ),
        dbc.Row(
            id="settings-menu",
            children=[
               dbc.Col(
                    id="SelCCAA1",
                    width=3,
                    children=[
                        html.Label(children="Comunidad Autónoma"),
                        html.Br(),
                        dcc.Dropdown(
                            id="SelCCAA",
                            options=list(
                                {"label": param, "value": param} for param in comunidades.keys()
                            )
                        ),
                    ],
                ),
                dbc.Col(
                    id="SelEsc1",
                    width=3,
                    children=[
                        html.Label(children="Tipo de escuela"),
                        html.Br(),
                        dcc.Dropdown(
                            id="SelEsc",
                            options=list(
                                {"label": param, "value": param} for param in tip_escuela.keys()
                            )
                        ),
                    ],
                ),
                dbc.Col(
                    id="SelLoc1",
                    width=3,
                    children=[
                        html.Label(children="Tipo de localidad"),
                        html.Br(),
                        dcc.Dropdown(
                            id="SelLoc",
                            options=list(
                                {"label": param, "value": param} for param in tip_localidad.keys()
                            )
                        ),
                    ],
                ),
                dbc.Col(
                    id="SelId1",
                    width=3,
                    children=[
                        html.Label(children="Id Escuela"),
                        html.Br(),
                        dcc.Dropdown(
                            id="SelId"
                        ),
                    ],
                )
            ],
        ),html.Br(),
#        html.Button('Resetear Simulación', id='reset', n_clicks=0),
        html.Br(),html.Br()
    ]


tabs_1 = dbc.Col(
    width=12, children=[dcc.Tabs(value='Estudiantes',
                children=[
                    dcc.Tab(
                        id="Estudiantes2",
                        label="Estudiantes",
                        value="Estudiantes2",
                        disabled=True,
                        style=tab_style, selected_style=tab_selected_style,
                        children=[]),
                    dcc.Tab(
                        id="Escuelas2",
                        label="Escuelas",
                        disabled=True,
                        style=tab_style, selected_style=tab_selected_style,
                        children=['variablesG2']
                             ),
                    dcc.Tab(
                        id="Profesores2",
                        label="Profesores",
                        disabled=True,
                        style=tab_style, selected_style=tab_selected_style,
                        children=['variablesG2']
                    ),
                ],

)])

layout = html.Div(
    children=[
              dbc.Row(className='twelve columns pretty_container',
                children=dbc.Card(
                    [dbc.CardHeader(children=[html.H4("Gráficas PISA y DATOS.GOB.ES")],
                                    className='texto_cab'), controls]
                )),
              html.Div(className='pretty_container',children= build_selec()),
              dbc.Row(children=[dbc.Col(width=6, children=[dbc.Container(className='pretty_container',
                                                                        fluid=True,
                                                                        style={"height": "auto"},
                                                                        children=(dbc.Row([tabs_1]))),]),
                                dbc.Col(width=6, children=[dbc.Container(className='pretty_container',
                                                                        fluid=True,
                                                                        style={"height": "100vh"},
                                                                        children=(predi,predi2,Variables ))])])
              ])


##Callback que filtra los ID de escuelas
@app.callback(
    Output('SelId', 'options'),
    Output('ValCom', 'children'),
    Output('ValEsp', 'children'),
    Input( 'SelCCAA', 'value'),
    Input( 'SelEsc', 'value'),
    Input( 'SelLoc', 'value'),prevent_initial_call=True
    )

def idEscuelas(CCAA, Esc, SelLoc):

    valoEsc2 = valoEsc[(valoEsc.SC001Q01TA == tip_localidad.get(SelLoc)) & (valoEsc.CCAA == comunidades.get(CCAA)) & (valoEsc.SC013Q01TA == tip_escuela.get(Esc))]

    global valorig
    valorig = '--'

    CA = DatosP_EST[(DatosP_EST.CCAA == comunidades.get(CCAA))]  * 10
    CA2 = int(CA.GLOBAL1.mean())

    ES2 = int(DatosP_EST.GLOBAL1.mean())  * 10


    return [{'label': i, 'value': i} for i in valoEsc2['CNTSCHID']], CA2, ES2


##Callback Resetea y carga los valores de las barras
@app.callback(
    Output('Estudiantes2', 'children'),Output('Escuelas2', 'children'),Output('Profesores2', 'children'),
    Output('Estudiantes2', 'disabled'),
    Output('Escuelas2', 'disabled'),Output('Profesores2', 'disabled'),

    Input('SelId', 'value'),prevent_initial_call=True
    )

def carga_barritas1(idEsc):
    global valorig
    valorig = '--'


    datFil = DatosP_EST[(DatosP_EST.CNTSCHID == idEsc)]
    datFilE = DatosP_ESC[(DatosP_ESC.CNTSCHID == idEsc)]
    datFilP = DatosP_PRO[(DatosP_PRO.CNTSCHID == idEsc)]


    h1 = []

    he1 = []

    hp1 = []


    a = []
    for G in ['G1','G2', 'G3']:

        gruposE = grupos[grupos.CodigoGrupo2 == G]


        for col in gruposE.CodigoGrupo:
            col1 = col + '_0'
            a.append(col1)
            pdxx = pd.DataFrame(a)
            pdxx.to_csv('col.csv')
            m = datFil.columns.str.contains(col)
            gruposE2 = datFil[datFil.columns[m]]

            pd1 = pd.DataFrame(gruposE[gruposE.CodigoGrupo == col][['DescripcionGrupo','Visible']])


            if pd1['Visible'].values == 'S':
                c = 'True'
            else:
                c = 'none'

            P1 = html.P(
                children=pd1['DescripcionGrupo'].values,
                style={'display': c},
                className="header-description",
            )

            sl = dcc.Slider(
                min=1,
                max=100,
                step=0.001,
                value=datFil[col1].min(),
#                tooltip={'always_visible':c},
                id={
                    'type': 'dynamic-Slider',
                    'index': col1},
                marks={
                    0: {'label': '0'},
                    datFil[col1].min(): {'label': 'Original'},
                    100: {'label': '0'}
                }
            )
            P2 = html.H1(
                title='Nono',
                style={'display': c},
                className="header-description",
                id={
                    'type': 'dynamic-P',
                    'index': col1 + '2'})

            sl3 = html.Div(children=[P1,P2,sl], style={'display': c})

            if pd1['Visible'].values == 'S':
               h1.append(sl3)



            gruposE2 = gruposE2.drop(col1, axis=1)


            for col2 in gruposE2.columns:
                sl2 = dcc.Slider(
                    min=1,
                    max=100,
                    step=0.001,

                    value=datFil[col2].min(),
                    id={
                        'type': 'dynamic-Slider',
                        'index': col2},
                    marks={
                        0: {'label': '0'},
                        datFil[col1].min(): {'label': 'Original'},
                        100: {'label': '0'}
                    },
                )
                sl = html.Div(children=sl2, style={'display': 'none'})


#                h1.append(sl)




    H1 = html.Div(children=h1)

    for G in ['G1', 'G2', 'G3']:

        gruposE = gruposEs[gruposEs.CodigoGrupo2 == G]

        for col in gruposE.CodigoGrupo:
            col1 = col + '_0'
            pd1 = pd.DataFrame(gruposE[gruposE.CodigoGrupo == col][['DescripcionGrupo', 'Visible']])

            m = datFilE.columns.str.contains(col)
            gruposE2 = datFilE[datFilE.columns[m]]

            if pd1['Visible'].values == 'S':
                c = 'True'
            else:
                c = 'none'

            P1 = html.P(
                children=pd1['DescripcionGrupo'].values,
                className="header-description",
            )

            sl = dcc.Slider(
                #                    className='slider',
                min=1,
                max=100,
                step=0.001,
                value=datFilE[col1].min(),
                id={
                    'type': 'dynamic-Slider_ESC',
                    'index': col1},
                marks={
                    0: {'label': '0'},
                    datFilE[col1].min(): {'label': 'Original'},
                    100: {'label': '0'}
                }
            )
            P2 = html.H1(
                title='Nono',
                className="header-description",
                id={
                    'type': 'dynamic-P',
                    'index': col1 + '2'})

            sl3 = html.Div(children=[P1, P2, sl], style={'display': c})
#
#            he1.append(sl3)
            if pd1['Visible'].values == 'S':
               he1.append(sl3)

            gruposE2 = gruposE2.drop(col1, axis=1)

            for col2 in gruposE2.columns:
                sl2 = dcc.Slider(
                    #                    className='slider',
                    min=1,
                    max=100,
                    step=0.001,

                    value=datFilE[col2].min(),
                    id={
                        'type': 'dynamic-Slider_ESC',
                        'index': col2},
                    marks={
                        0: {'label': '0'},
                        datFilE[col1].min(): {'label': 'Original'},
                        100: {'label': '0'}
                    },
                )
                sl = html.Div(children=sl2, style={'display': 'none'})



#                he1.append(sl)


    H2 = html.Div(children=he1)

##TABS Profesores
    for G in ['G1', 'G2', 'G3']:

        gruposE = gruposP[gruposP.CodigoGrupo2 == G]

        for col in gruposE.CodigoGrupo:
            col1 = col + '_0'
            pd1 = pd.DataFrame(gruposE[gruposE.CodigoGrupo == col][['DescripcionGrupo', 'Visible']])
            m = datFilP.columns.str.contains(col)
            gruposE2 = datFilP[datFilP.columns[m]]

            if pd1['Visible'].values == 'S':
                c = 'True'
            else:
                c = 'none'

            P1 = html.P(
                children=pd1['DescripcionGrupo'].values,
                className="header-description",
            )

            sl = dcc.Slider(
                #                    className='slider',
                min=1,
                max=100,
                step=0.001,
                value=datFilP[col1].min(),
                id={
                    'type': 'dynamic-Slider_PRO',
                    'index': col1},
                marks={
                    0: {'label': '0'},
                    datFilP[col1].min(): {'label': 'Original'},
                    100: {'label': '0'}
                }

            )
            P2 = html.H1(
                title='Nono',
                className="header-description",
                id={
                    'type': 'dynamic-P',
                    'index': col1 + '2'})

            sl3 = html.Div(children=[P1, P2, sl], style={'display': c})

#            hp1.append(sl3)
            if pd1['Visible'].values == 'S':
               hp1.append(sl3)

            gruposE2 = gruposE2.drop(col1, axis=1)

            for col2 in gruposE2.columns:
                sl2 = dcc.Slider(
                    #                    className='slider',
                    min=1,
                    max=100,
                    step=0.001,

                    value=datFilP[col2].min(),
                    id={
                        'type': 'dynamic-Slider_PRO',
                        'index': col2},
                    marks={
                        0: {'label': '0'},
                        datFilP[col1].min(): {'label': 'Original'},
                        100: {'label': '0'}
                    },
                )
                sl = html.Div(children=sl2, style={'display': 'none'})


#                hp1.append(sl)


    H3 = html.Div(children=hp1)


    return H1,H2,H3,False,False,False

## Actualiza el valor de la barra Estudiantes
@app.callback(
    Output({'type': 'dynamic-Slider', 'index': MATCH}, 'marks'),
    Input( {'type': 'dynamic-Slider', 'index': MATCH}, 'value'),
    State( {'type': 'dynamic-Slider', 'index': MATCH}, 'id'),
    State('SelId', 'value'),prevent_initial_call=True
    )

def update_output(value,ide,idEsc):
        datFil = DatosP_EST[(DatosP_EST.CNTSCHID == idEsc)]
        ori = datFil[ide.get('index')].min()
        marks = {
        0: {'label': '0'},
        value: {'label': 'Actual '+str(int(value))},
        ori : {'label': 'Original ' +str(int(ori)) },
        100: {'label': '100'}
                }

        return marks

# Actualiza el valor de la barra Escuelas
@app.callback(
    Output({'type': 'dynamic-Slider_ESC', 'index': MATCH}, 'marks'),
    Input( {'type': 'dynamic-Slider_ESC', 'index': MATCH}, 'value'),
    State( {'type': 'dynamic-Slider_ESC', 'index': MATCH}, 'id'),
    State('SelId', 'value'),prevent_initial_call=True
    )

def update_output(value,ide,idEsc):

    datFil = DatosP_ESC[(DatosP_ESC.CNTSCHID == idEsc)]
    ori = datFil[ide.get('index')].min()
    marks = {
    0: {'label': '0'},
    value: {'label': 'Actual '+str(int(value))},
    ori : {'label': 'Original ' +str(int(ori)) },
    100: {'label': '100'}
           }

    return marks

## Actualiza el valor de la barra Profesores
@app.callback(
    Output({'type': 'dynamic-Slider_PRO', 'index': MATCH}, 'marks'),
    Input( {'type': 'dynamic-Slider_PRO', 'index': MATCH}, 'value'),
    State( {'type': 'dynamic-Slider_PRO', 'index': MATCH}, 'id'),
    State('SelId', 'value'),prevent_initial_call=True
    )

def update_output(value,ide,idEsc):

        datFil = DatosP_PRO[(DatosP_PRO.CNTSCHID == idEsc)]
        ori = datFil[ide.get('index')].min()
        marks = {
        0: {'label': '0'},
        value: {'label': 'Actual '+str(int(value))},
        ori : {'label': 'Original ' +str(int(ori)) },
        100: {'label': '100'}
                }

        return marks



## Actualiza la lista de preguntas estudiantes
@app.callback(
    Output('varicom2','children'),Output('varicom','children'),
    Input( {'type': 'dynamic-Slider', 'index': ALL}, 'value'),
    Input( {'type': 'dynamic-Slider_PRO', 'index': ALL}, 'value'),
    Input( {'type': 'dynamic-Slider_ESC', 'index': ALL}, 'value'),

    prevent_initial_call=True
    )

def update_variables(value1,value2, value3):


        ctx = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
        ctx = eval(ctx)

        a = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
        a = eval(a)


        C = []
        if ctx.get('type') == 'dynamic-Slider':
            gruposE = PRgrupos[PRgrupos.CodigoGrupo == a.get('index').split('_')[0]]
            nom = gruposE.iloc[0].DescripcionGrupo
            for des in gruposE.Descripcion:
                P2 = html.Li(
                children=des,
                className="header-description")
                C.append(P2)


        if ctx.get('type') == 'dynamic-Slider_ESC':
            gruposE = PRgruposEs[PRgruposEs.CodigoGrupo == a.get('index').split('_')[0]]
            nom = gruposE.iloc[0].DescripcionGrupo
            for des in gruposE.Descripcion:
                P2 = html.Li(
                    children=des,
                    className="header-description")
                C.append(P2)

        if ctx.get('type') == 'dynamic-Slider_PRO':
            gruposE = PRgruposP[PRgruposP.CodigoGrupo == a.get('index').split('_')[0]]
            nom = gruposE.iloc[0].DescripcionGrupo
            for des in gruposE.Descripcion:
                P2 = html.Li(
                    children=des,
                    className="header-description")
                C.append(P2)


        return nom, C
## En Datamod estan las 358  variables de las 1000 escuelas, al final estan las que se pueden tocar
## con las barras, por lo que usamos esos datos y actualizamos los de las barras
@app.callback(
    Output('ValNue', 'children'),Output('ValOri', 'children'),
    Input( {'type': 'dynamic-Slider_ESC', 'index': ALL}, 'value'),
    Input( {'type': 'dynamic-Slider', 'index': ALL}, 'value'),
    Input( {'type': 'dynamic-Slider_PRO', 'index': ALL}, 'value'),
    Input({'type': 'dynamic-Slider_ESC', 'index': ALL}, 'id'),
    Input({'type': 'dynamic-Slider', 'index': ALL}, 'id'),
    Input({'type': 'dynamic-Slider_PRO', 'index': ALL}, 'id'),
    State('ValOri', 'children'),State('SelId', 'value'),
    prevent_initial_call=True
)
def display_output(valuesESC,valuesEST, valuesPRO,indexESC,indexPRO, indexEST,valorig1,ides):


      Datamod2 = Datamod[Datamod['CNTSCHID'] == ides]

      Datamod2 = Datamod2.drop(['CNTSCHID','Unnamed: 0'], axis='columns')
      ab2 = mode.predict(Datamod2) * 10

      values = np.concatenate((valuesESC, valuesEST, valuesPRO), axis=None)

      i2 = 323
      for  i  in range(34):

         i2 = i2 + 1

         Datamod2.iloc[:, i2] = values[i]


      ab = mode.predict(Datamod2) * 10


#      global valorig
#      print(valorig)
#      if valorig == '--':
#         ab2 = ab
#         valorig = ab
#      else:
#         valorig = ab
#      ab = 2

      return round(float(ab),2), round(float(ab2),2)
#      return ab, ab2



#Datamod
#@app.callback(
#    Output('ValNue', 'children'),Output('ValOri', 'children'),
#    Input( {'type': 'dynamic-Slider_ESC', 'index': ALL}, 'value'),
#    Input( {'type': 'dynamic-Slider_PRO', 'index': ALL}, 'value'),
#    Input( {'type': 'dynamic-Slider', 'index': ALL}, 'value'),
#    Input({'type': 'dynamic-Slider_ESC', 'index': ALL}, 'id'),
#    Input({'type': 'dynamic-Slider_PRO', 'index': ALL}, 'id'),
#    Input({'type': 'dynamic-Slider', 'index': ALL}, 'id'),
#    State('ValOri', 'children'),
#    prevent_initial_call=True
#)
#def display_output(valuesESC,valuesPRO, valuesEST,indexESC,indexPRO, indexEST,valorig1):


#      valuesESC = np.array(valuesESC)

#      valuesPRO = np.array(valuesPRO)

#      valuesEST = np.array(valuesEST)

#      values = np.concatenate((valuesESC, valuesPRO, valuesEST), axis=None)

#      values = np.array(values).reshape((1, 358))

#      values = values.reshape((1, 358))


#      ab = mode.predict(values) * 10

#      ab2 = valorig1
#      global valorig

#      if valorig == '--':
#         ab2 = ab
#         valorig = ab
#      else:
#         valorig = ab
#      ab = 2
#
#     return round(float(ab),2), round(float(ab2),2)
#      return ab, ab2
