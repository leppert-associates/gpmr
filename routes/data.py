import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_html_components import Summary
import pandas as pd
import plotly.express as px

from app import app

# Import and clean data, should be postgres
df = pd.read_csv(r'data/deertrail.csv', parse_dates=['datetime'])
dfmi = df.set_index(['location', 'parameter', 'datetime']).sort_index()

# Data page
layout = html.Div([
    html.Aside([
        html.H2('Inputs'),
        html.Label('Location'),
        dcc.Dropdown(id='location',
                     options=[
                         {'label': loc, 'value': loc} for loc in df['location'].unique()
                     ],
                     multi=False,
                     placeholder='Select a well'
                     ),
        html.Label('Parameter'),
        dcc.Dropdown(id='parameter',
                     options=[
                         {'label': param, 'value': param} for param in df['parameter'].unique()
                     ],
                     multi=False,
                     placeholder='Select a parameter'
                     ),
        # html.Label('Reporting Period'),
        # dcc.DatePickerRange(
        #     id='reporting-period',
        #     min_date_allowed=df['datetime'].min(),
        #     max_date_allowed=df['datetime'].max(),
        # ),
    ], id='input_container', className='container'),
    # outputs
    html.Main([
        html.H2('Summary Statistics'),
        html.Div(id='output_container',
                 className='output container', children=[]),
        html.H2('Graph'),
        dcc.Graph(id='linechart', responsive=True, figure=px.line(
            None, template='seaborn')),
    ]),
], id='root')


# Connect the Plotly graphs with Dash Components
@app.callback(
    Output('output_container', 'children'),
    Output('linechart', 'figure'),
    Input('location', 'value'),
    Input('parameter', 'value'),
    # Input('reporting-period', 'children'),
)
def update_graph(location, parameter):
    dfmic = dfmi.loc[(location, parameter)].reset_index()
    dfmic['value'].fillna(
        value=dfmic['detection_limit']/2, inplace=True)
    dfmic.sort_values(by='datetime', inplace=True)
    # get sum stats
    description = dfmic['value'].describe().reset_index()
    desc_list = list(description.itertuples(index=False, name=None))
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
