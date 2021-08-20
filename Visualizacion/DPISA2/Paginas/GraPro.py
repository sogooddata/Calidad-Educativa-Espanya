import dash_html_components as html
import plotly.express as px
import pandas as pd
import pickle
import json
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, ALL, State
from app import app
import dash_core_components as dcc

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


##Recupera el nombre de los grupos en un Label
def RecuperaGrupos(grupos, preguntas, grupo2):
    Nombres=[]
    ##Seleccionamos solo las del grupo del tab
    grupos = grupos[grupos.CodigoGrupo2 == grupo2]
    ##Generamos el Label y las preguntas del Dropdown

    for NomGrupo in grupos['CodigoGrupo'].values:
        desgru = grupos[grupos.CodigoGrupo == NomGrupo ]['DescripcionGrupo'].values[0]
        Nombres.append(html.Label(id=desgru, children=desgru))

        Preguntas = dcc.Dropdown(
            id={'index': desgru+'Pro_', 'type':'Pro_din_pregu'},
            options=[
            {"label": Variable2, "value": Variable}
            for Variable, Variable2 in preguntas[preguntas.CodigoGrupo==NomGrupo][['Codigo','Descripcion']].values

        ],
        clearable=False,
        className="dropdown",
        )
        Nombres.append(Preguntas)

    return Nombres

Cabecera = dbc.Card(children=[dbc.CardHeader(html.H3("Gráficas cuestionario del profesorado")),
                    dbc.CardBody(children=[
                        html.H5("En esta sección, se podrá visualizar la mayoría de las preguntas que se han realizado a las y los 3000 docentes de las escuelas españolas seleccionadas en el Informe PISA."),html.P(style={"line-height":"1px"}),
                        html.H5("Se puede seleccionar dentro de las diferentes categorías, una pregunta concreta; una vez seleccionada, se muestran los siguientes gráficos:"),html.P(style={"line-height":"1px"}),
                        html.H5("    - Gráfico de tarta resumen, de todo el profesorado"),html.P(style={"line-height":"1px"}),
                        html.H5("    - Gráfico de mapa de color de las comunidades con las diferentes respuestas de la pregunta"),html.P(style={"line-height":"1px"}),
                        html.H5("    - Gráfico de barras de las distintas comunidades para su comparación"),html.P(style={"line-height":"1px"}),
                        html.H5("    - Pestaña con gráficos de barras desglosado por CCAA"),html.P(style={"line-height":"1px"}),
                        html.H5("    - Pestaña con gráficos de barras desglosado por tipo de población"),html.P(style={"line-height":"1px"}),
                        html.H5("    - Pestaña con gráfico de barras desglosado por tipo de escuela")]
                    )])

comunidades = {"Andalucía":1,"Aragón":2,"Asturias":3,"Baleares":4,"Canarias":5,"Cantabría":6,"Castilla y León":7,"Castilla y La Mancha":8,"Cataluña":9,"Extremadura":10,"Galicia":11,"La Rioja":12,"Madrid":13,"Murcia":14,"Navarra":15,"País Vasco":16,"Comunidad Valenciana":17,"Ceuta":18,"Melilla":19}
comunidadest = {'01':"Andalucía",'02':"Aragón",'03':"Asturias",'04':"Baleares",'05':"Canarias",'06':"Cantabría",'07':"Castilla y León",'08':"Castilla y La Mancha",'09':"Cataluña",'10':"Extremadura",'11':"Galicia",'12':"La Rioja",'13':"Madrid",'14':"Murcia",'15':"Navarra",'16':"País Vasco",'17':"Comunidad Valenciana",'18':"Ceuta",'19':"Melilla"}

tip_localidad = {1:'A village, hamlet or rural area (fewer than 3 000 people)', 2:'A small town (3 000 to about 15 000 people)',3:'A town (15 000 to about 100 000 people)',4: 'A city (100 000 to about 1 000 000 people)',5: 'A large city (with over 1 000 000 people)'}
tip_escuela= {1:'Pública', 2:'Privada'}

preguntas = pd.read_csv("data/GruPreguntasPRO.csv", na_values = ["NaN", "NaN"], sep = ";")

grupos = pd.read_csv("data/GruposPRO.csv", na_values = ["NaN", "NaN"], sep = ";")
gson = json.loads(open('data/georef-spain-comunidad-autonoma.geojson').read())

VCCA = pd.read_csv("data/GRUPCA.csv", na_values = ["NaN", "NaN"], sep = ",")
VCCA['CCAA'] = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19']

##Diccionario con los datos calculados por CCAA
with open("data/ProCal.dat", "rb") as f:
    DatCal= pickle.load(f)

##Diccionario con los datos calculados por población
with open("data/ProCal2.dat", "rb") as f:
    DatCal2= pickle.load(f)

##Diccionario con los datos calculados por tipo de escuela
with open("data/ProCal3.dat", "rb") as f:
    DatCal3= pickle.load(f)


a_file = open("data/valuesPro.pkl", "rb")
var_values = pickle.load(a_file)
a_file.close()

a_file = open("data/labelPro.pkl", "rb")
var_labels = pickle.load(a_file)
a_file.close()

variablesG1 = dbc.Card(
        [dbc.CardHeader("Variables1", className='texto_cab'),
        html.Div(children=RecuperaGrupos(grupos,preguntas,'G1'))]
        )

variablesG2 = dbc.Card(
        [dbc.CardHeader("Variables", className='texto_cab'),
        html.Div(children=RecuperaGrupos(grupos,preguntas, 'G2'))]
        )

variablesG3 = dbc.Card(
        [dbc.CardHeader("Variables", className='texto_cab'),
        html.Div(children=RecuperaGrupos(grupos,preguntas, 'G3'))]
        )


tabs_1 = dbc.Col(className='pretty_container',width=4,children=[dcc.Tabs(value='tab1',
                children=[
                    dcc.Tab(
                        label="Categorias 1",style=tab_style, selected_style=tab_selected_style,
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        children=[variablesG1]),
                    dcc.Tab(
                        label="Categorias 2",style=tab_style, selected_style=tab_selected_style,
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        children=[variablesG2]),
                    dcc.Tab(label="Categorias 3",style=tab_style, selected_style=tab_selected_style,
                        value="tab3",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        children=[variablesG3]
                    ),
                ],

)])

##Graficos
grafi1 = dbc.Col(width=12,children=[dcc.Graph(id="Pro_pie-chart")])

grafi2 = dbc.Col(width=12,children=[html.H3(children='Porcentaje alumnado por CCAA',
                    style={'color': 'white', 'fontSize': 24, 'background-color': 'black', ' text-align': 'center'}),
                    dcc.RadioItems(id='countries-radiop', value=1),
                    dcc.Graph(id="map-chartp")])

grafi3x = html.Div(children=[dcc.Graph(id="bar-chartxp")])

grafi1P = dbc.Col(width=12,children=[dcc.Graph(id="P1Pro_pie-chart")])
grafi2P = dbc.Col(width=12,children=[dcc.Graph(id="P2Pro_pie-chart")])

grafi3 = html.Div(children=[dcc.Graph(id="Pro_bar-chart")])
grafi3C1 = html.Div(children=[dcc.Graph(id="Pro_bar-chart1")])
grafi3C2 = html.Div(children=[dcc.Graph(id="Pro_bar-chart2")])
grafi3C3 = html.Div(children=[dcc.Graph(id="Pro_bar-chart3")])
grafi3C4 = html.Div(children=[dcc.Graph(id="Pro_bar-chart4")])

grafi1E = dbc.Col(width=12,children=[dcc.Graph(id="E1Pro_pie-chart")])






graficas = dbc.Col(className='pretty_container', width=7,
    children=dbc.Card(
        [dbc.CardHeader(className='texto_cab', children=['(',html.Label(id='Pro_vari'),')  ',html.H4(id='Pro_vari2')]),
         grafi1,grafi2, grafi3x]))

graficasCCAA = dbc.Col(className='pretty_container', width=12,
    children=dbc.Card(
        [dbc.CardHeader(className='texto_cab', children=['Graficas por Comunidad autónoma']),
         grafi3,
         grafi3C1,
         grafi3C2,
         grafi3C3,
         grafi3C4]))

graficasPob = dbc.Col(className='pretty_container', width=12,
    children=dbc.Card(
        [dbc.CardHeader(className='texto_cab', children=['Graficas por tipo de población']),
         grafi1P,
         grafi2P]))

graficasEsc = dbc.Col(className='pretty_container', width=12,
    children=dbc.Card(
        [dbc.CardHeader(className='texto_cab', children=['Graficas por tipo de escuela']),
         grafi1E]))

TB = dcc.Tabs(children=[
                   dcc.Tab(id="PGraficas1",style=tab_style, selected_style=tab_selected_style,
                           label="Gráficas por CCCAA", children=dbc.Row([graficasCCAA])),
                   dcc.Tab(id="PGraficas2",style=tab_style, selected_style=tab_selected_style,
                           label="Gráficas por tipo de población", children=dbc.Row([graficasPob])),
                   dcc.Tab(id="PGraficas3",style=tab_style, selected_style=tab_selected_style,
                           label="Gráficas por tipo de escuelas", children=dbc.Row([graficasEsc])),
                   ])

layout = dbc.Container(
    fluid=True,
    style={"height": "100vh"},
    children=(Cabecera, dbc.Row([tabs_1,graficas]),TB)

     )

##Callback que resetea la elección de la pregunta para que solo quede una y le pasa la variable a las graficas
@app.callback(
    Output({'type': 'Pro_din_pregu', 'index': ALL}, 'value'),
    Output('Pro_vari', 'children'),Output('Pro_vari2', 'children'),
    Input( {'type': 'Pro_din_pregu', 'index': ALL}, 'value'),
    State('Pro_vari', 'children'),prevent_initial_call=True
    )

def resetea(value,value2):
    for pre in range(0,len(value)):
        if value[pre] != None and value2 == value[pre]:
           value[pre] = None
        if value[pre] != None:
           value21 =  value[pre]
    value2 = value21
    titulo = preguntas[preguntas['Codigo'] == value2]['Descripcion'].values[0]
    return value, value2, titulo

@app.callback(
    Output("Pro_pie-chart", "figure"),Output("P1Pro_pie-chart", "figure"),Output("P2Pro_pie-chart", "figure"),
    Output("E1Pro_pie-chart", "figure"),
    Output('countries-radiop', 'options'), Output('countries-radiop', 'value'),
    [
     Input( 'Pro_vari', 'children'),
    ],prevent_initial_call=True
)

def update_charts(variable):

    df3 = DatCal.get(variable).sort_values(variable)
    #df3 = df3.replace({"CCAA": comunidadest}).sort_values(variable)
    fig = px.pie(df3, values=0, names=variable, color=variable)
    fig.update_traces(hoverinfo='label+percent', textinfo='label+percent', textfont_size=20,
                      marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    options = [{'label': var_values[variable][k], 'value': var_values[variable][k]} for k in
               var_values[variable].keys()]
    df3 = DatCal2.get(variable)

    df4 = df3[(df3['SC001Q01TA'].isin([1, 2, 3]))]
    df4 = df4.replace({"SC001Q01TA": tip_localidad}).sort_values(variable)
    figp1 = px.bar(df4, x=variable, y=0, color=variable, barmode="group",facet_col='SC001Q01TA')

    df4 = df3[(df3['SC001Q01TA'].isin([4, 5]))]
    df4 = df4.replace({"SC001Q01TA": tip_localidad}).sort_values(variable)
    figp2 = px.bar(df4, x=variable, y=0, color=variable, barmode="group",facet_col='SC001Q01TA')

    df3 = DatCal3.get(variable)
    df3 = df3.replace({"SC013Q01TA": tip_escuela}).sort_values(variable)
    figp3 = px.bar(df3, x=variable, y=0, color=variable, barmode="group",facet_col='SC013Q01TA')

    return fig, figp1, figp2, figp3, options, df3.iloc[0][variable]

@app.callback(
    Output("map-chartp", "figure"),
    [
        Input( 'Pro_vari', 'children'),
        Input('countries-radiop', 'value')
    ],prevent_initial_call=True
)
def update_charts2(variable, valor):

    df = DatCal.get(variable)
#    df = DatCal.get(variable)
#    df = df.replace({"CCAA": comunidades})
    df = df.loc[df[variable] == valor]

    fig = px.choropleth_mapbox(df, geojson=gson, locations='CCAA', color=0,
                               featureidkey="properties.id",
                               color_continuous_scale="Viridis",
#                               range_color=(cal[variable].min(), cal[variable].max()),
                               mapbox_style="carto-positron",
                               zoom=4, center={"lat": 40.4167, "lon": -3.70325},
                               opacity=0.5,
                               labels={0: 'unemployment rate'}
                               )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    return fig

@app.callback(
    Output("Pro_bar-chart", "figure"), Output("Pro_bar-chart1", "figure"), Output("Pro_bar-chart2", "figure"), Output("Pro_bar-chart3", "figure"),
    Output("Pro_bar-chart4", "figure"),Output("bar-chartxp", "figure"),
    [
        Input( 'Pro_vari', 'children')
    ],prevent_initial_call=True
    )

def update_charts3(variable):

    df = DatCal.get(variable)
    df1 = df[(df['CCAA'].isin(['01','02','03','04']))]
    df1 = df1.replace({"CCAA": comunidadest}).sort_values(variable)
    fig = px.bar(df1, x=variable, y=0, color=variable, barmode="group", facet_col="CCAA")

    df1 = df[(df['CCAA'].isin(['05','06','07','08']))]
    df1 = df1.replace({"CCAA": comunidadest}).sort_values(variable)
    fig1 = px.bar(df1, x=variable, y=0, color=variable, barmode="group", facet_col="CCAA")

    df1 = df[(df['CCAA'].isin(['09','10','11','12']))]
    df1 = df1.replace({"CCAA": comunidadest}).sort_values(variable)
    fig2 = px.bar(df1, x=variable, y=0, color=variable, barmode="group", facet_col="CCAA")

    df1 = df[(df['CCAA'].isin(['13','14','15','16']))]
    df1 = df1.replace({"CCAA": comunidadest}).sort_values(variable)
    fig3 = px.bar(df1, x=variable, y=0, color=variable, barmode="group", facet_col="CCAA")

    df1 = df[(df['CCAA'].isin(['17','18','19']))]
    df1 = df1.replace({"CCAA": comunidadest}).sort_values(variable)
    fig4 = px.bar(df1, x=variable, y=0, color=variable, barmode="group", facet_col="CCAA")

    df = df.replace({"CCAA": comunidadest})
    fig5 = px.bar(df, x="CCAA", y=0, color=variable, title="Long-Form Input")

    fig5.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig5.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    return fig, fig1, fig2, fig3, fig4, fig5