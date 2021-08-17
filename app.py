import pandas as pd
import plotly.express as px

import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
#import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'Leppert': 'Broncos303'
}

external_stylesheets = ['assets/style.css']  # [dbc.themes.CYBORG]
app = dash.Dash(__name__, title='ECIMS',
                external_stylesheets=external_stylesheets)

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

# Import and clean data, should be postgres
df = pd.read_csv(r'data/deertrail.csv', parse_dates=['datetime'])
dfmi = df.set_index(['location', 'parameter', 'datetime']).sort_index()

# App layout
app.layout = html.Div(
    children=[
        html.Nav([html.H1("ECIMS"), html.A("Login", href="/login")]),
        html.Aside([
            html.Label('Parameter'),
            dcc.Dropdown(id="parameter",
                         options=[
                             {'label': param, 'value': param} for param in df['parameter'].unique()
                         ],
                         multi=False,
                         placeholder="Select a parameter",
                         style={'width': "100%"}
                         ),
            html.Label('Location'),
            dcc.Dropdown(id="location",
                         options=[
                             {'label': loc, 'value': loc} for loc in df['location'].unique()
                         ],
                         multi=False,
                         placeholder="Select a well",
                         style={'width': "100%"}
                         ),
            html.Label('Reporting Period'),
            dcc.DatePickerRange(
                id='reporting-period',
                min_date_allowed=df['datetime'].min(),
                max_date_allowed=df['datetime'].max(),
            ),
        ], id='input_container', className="container"),
        html.Main([
            dcc.Graph(id='linechart', figure={}, responsive=True),
            html.Div(id='output_container',
                     className="container", children=[]),
        ])
    ], id="root")


# Connect the Plotly graphs with Dash Components
@app.callback(
    Output(component_id='output_container', component_property='children'),
    Output(component_id='linechart', component_property='figure'),
    Input(component_id='parameter', component_property='value'),
    Input(component_id='location', component_property='value'),
)
def update_graph(parameter_value, location_value):
    dfmic = dfmi.loc[(location_value, parameter_value)].reset_index()
    dfmic['value'].fillna(
        value=dfmic['detection_limit']/2, inplace=True)
    summary = [html.H2("Summary Statistics"), f"{dfmic['value'].describe()}"]
    # Plotly Express
    fig = px.line(
        dfmic,
        x='datetime',
        y='value',
        title='Time vs Concentration',
        labels={
            "datetime": "Date",
            "value": f"Concentration ({dfmic.unit[0]})"
        },
        template='seaborn'
    )

    return summary, fig


if __name__ == '__main__':
    app.run_server(debug=True)
