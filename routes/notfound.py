import dash_core_components as dcc
import dash_html_components as html

user_input = html.Div([
    html.H1('Page not found'),
    dcc.Link('Go back', href='/', className='button'),
], className='subcontainer')

display = "Page not found"
