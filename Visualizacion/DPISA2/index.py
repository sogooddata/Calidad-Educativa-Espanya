import dash_core_components as dcc
import dash_html_components as html
from app import app
from Paginas import home, GraEstu, Simu, GraPro, GraEscu, INE, contacto
import base64

test_png = 'LOGO.png'
test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')

## Cabecera
header = html.Div(
            children=html.Img(src='data:image/png;base64,{}'.format(test_base64)),
                )
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
server = app.server

app.layout = html.Div([
    header,
#    navbar,
    dcc.Tabs(children=[dcc.Tab(id="Inicio",style=tab_style, selected_style=tab_selected_style,
                     label="Inicio",children=html.Div(children=[home.layout])),
             dcc.Tab(id="Graficas1",style=tab_style, selected_style=tab_selected_style,
                     label="Gráficas Alumnado",children=GraEstu.layout),
             dcc.Tab(id="Graficas2",style=tab_style, selected_style=tab_selected_style,
                     label="Gráficas Profesorado",children=GraPro.layout),
             dcc.Tab(id="Graficas3",style=tab_style, selected_style=tab_selected_style,
                     label="Gráficas Centros Educativos", children=GraEscu.layout),
             dcc.Tab(id="Graficas4",style=tab_style, selected_style=tab_selected_style,
                     label="Gráficas PISA y DATOS.GOB.ES", children=INE.layout),
             dcc.Tab(id="Simulación",style=tab_style, selected_style=tab_selected_style,
                     label="Simulacion", children=Simu.layout),
             dcc.Tab(id="Contacto", style=tab_style, selected_style=tab_selected_style,
                     label="Contacto", children=contacto.layout),
                       ])
])


#@app.callback(Output('page-content', 'children'),
#              Input('url', 'pathname'))
#def display_page(pathname):
#    if pathname == '/Paginas/Home':
#        return home.layout
#    if pathname == '/Paginas/GraEstu':
#        return GraEstu.layout
#    if pathname == '/Paginas/Simu':
#        return Simu.layout
#    else:
#        return home.layout


if __name__ == '__main__':
    app.run_server(debug=True)

