from dash import dcc
from dash import html

user_input = html.Div([
    html.H1('Page not found'),
    dcc.Link('Go back', href='/', className='button'),
], className='subcontainer')

display = "Page not found"
