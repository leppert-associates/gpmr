import dash

external_stylesheets = ['assets/style.css']
app = dash.Dash(__name__, title='GPMR',
                suppress_callback_exceptions=True,
                external_stylesheets=external_stylesheets)
server = app.server
