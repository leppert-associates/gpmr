import dash

app = dash.Dash(__name__, title='GPMR',
                suppress_callback_exceptions=True,
                external_stylesheets=['assets/style.css'])
server = app.server
