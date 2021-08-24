from app import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import utils.api as api


# Data page
user_input = [
    html.H2('Input'),
    html.Label('Monitoring Well'),
    dcc.Dropdown(id='location',
                 options=[
                     {'label': loc, 'value': loc} for loc in api.get_locations()
                 ],
                 multi=False,
                 placeholder='Select a well'
                 ),
    html.Label('Analyte'),
    dcc.Dropdown(id='parameter',
                 options=[
                     {'label': param, 'value': param} for param in api.get_parameters()
                 ],
                 multi=False,
                 placeholder='Select a parameter'
                 ),
    html.Div([html.H2('Output'),
              html.Div(id='output_container',
             className='output container', children=[])], className='wrapper'),
]


display = [html.H2('Display'),
           dcc.Loading(type='circle', color='#4c72b0', children=[
               dcc.Graph(id='linechart', responsive=True, figure=px.line(
                   None, template='seaborn'))])
           ]


# Connect the Plotly graphs with Dash Components
@ app.callback(
    Output('output_container', 'children'),
    Output('linechart', 'figure'),
    Input('location', 'value'),
    Input('parameter', 'value'),
)
def update_graph(location, parameter):
    if location and parameter:
        dfmic, desc_list = api.get_data(location, parameter)
        summary = html.Ul(
            id='sum-list', children=[html.Li(f"{i[0]}: {i[1]}") for i in desc_list])

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
            template='seaborn',
            markers=True,
        )

        return summary, fig
    # keep it empty if no inputs
    else:
        return '', px.line(None, template='seaborn')
