import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from app import app

import base64


test_base64N = base64.b64encode(open('Nono.png', 'rb').read()).decode('ascii')
test_base64B = base64.b64encode(open('Bea.png', 'rb').read()).decode('ascii')
test_base64I = base64.b64encode(open('Ivan.png', 'rb').read()).decode('ascii')

Contacto = html.Div(
            children=html.H2("Para cualquier sugerencia o comentario nos podeís escribir a: contacto@dxe.es",style={"font-family": "Bodoni MT Black"})
                )

Contacto2 = html.Div(
            children=html.H2("DXE somos:",style={"font-family": "Bodoni MT Black"})
                )

Nono = html.Div(
            children=html.Img(src='data:image/png;base64,{}'.format(test_base64N)),
                )
Bea = html.Div(
            children=html.Img(src='data:image/png;base64,{}'.format(test_base64B)),
                )
Ivan = html.Div(
            children=html.Img(src='data:image/png;base64,{}'.format(test_base64I)),
                )

layout = html.Div([Contacto, Contacto2, Nono,Bea,Ivan])



