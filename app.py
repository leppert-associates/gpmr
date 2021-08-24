import dash
import dash_bootstrap_components as dbc

external_stylesheets = ['assets/style.css']
app = dash.Dash(__name__, title='GPMR',
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
