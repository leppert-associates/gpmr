from app import app
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import utils.api as api


# load dataframe from csv
df = api.load_data(r'data/deertrail_lab.csv')


# Data page
user_input = [
    html.H2('Input'),
    html.Label('Monitoring Well'),
    dcc.Dropdown(id='location',
                 options=[
                     {'label': loc, 'value': loc} for loc in api.get_locations(df)
                 ],
                 multi=False,
                 placeholder='Select a well'
                 ),
    html.Label('Analyte'),
    dcc.Dropdown(id='parameter',
                 options=[
                     {'label': param, 'value': param} for param in api.get_parameters(df)
                 ],
                 multi=False,
                 placeholder='Select a parameter'
                 ),
    html.Label('Y-Axis Type'),
    dcc.RadioItems(
        id='yaxis-type',
        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
        value='Linear',
        labelStyle={'display': 'inline-block'}
    ),
    html.Div([html.H2('Output'),
              dcc.Loading(type='circle', color='#4c72b0', children=[
                  html.Div(id='output_container',
                           className='output container', children=[])
              ], className='wrapper')])]


display = [html.H2('Display'),
           dcc.Graph(id='linechart', responsive=True, figure=px.line(
               None, template='seaborn'))]


# Connect the Plotly graphs with Dash Components
@ app.callback(
    Output('output_container', 'children'),
    Output('linechart', 'figure'),
    Input('location', 'value'),
    Input('parameter', 'value'),
    Input('yaxis-type', 'value'),
)
def update_graph(location, parameter, yaxis_type):
    if location and parameter:
        try:
            dfmic = api.get_data(df, location, parameter)
            if dfmic.empty:
                print('DataFrame is empty!')
                return 'No data to display', px.line(None, template='seaborn')
            desc_list = api.get_description(dfmic)
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
            fig.update_yaxes(type='linear' if yaxis_type ==
                             'Linear' else 'log')
            fig.update_layout(transition_duration=250)
            return summary, fig

        except KeyError:
            return 'No data for selection', px.line(None, template='seaborn')

    else:
        return '', px.line(None, template='seaborn')
