import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from api import SqlachemyEngine, Facility
from dotenv import load_dotenv

load_dotenv()

app = dash.Dash(__name__, title='GPMR')
server = app.server

uri = os.getenv('DATABASE_URL')
if uri.startswith('postgres://'):
    uri = uri.replace('postgres://', 'postgresql://', 1)
engine = SqlachemyEngine(uri).create_engine()
facility = Facility(engine, 'deertrail')

app.layout = html.Div([
    html.Nav([
        html.Div([
            html.Img(src=app.get_asset_url('logo.png'),
                     style={'height': '2rem'}),
            dcc.Link(
                html.H1('GPMR'), href='/', className='title')
        ], className='flex'),
        html.Div([
            html.Img(src=app.get_asset_url(
                'github-brands.svg'), className='icon'),
            html.A('Source', href='https://github.com/ItaiAxelrad/gpmr')
        ], className='flex')
    ]),
    html.Aside(children=[
        html.Div([html.H2('Input'),
                  html.Label('Monitoring Well', className='label'),
                  dcc.Dropdown(id='location',
                               options=[
                                   {'label': loc, 'value': loc} for loc in [l[0] for l in facility.get_locations()]
                               ],
                               placeholder='Select a well',
                               ),
                  html.Label('Analyte', className='label'),
                  dcc.Dropdown(id='parameter',
                               options=[],
                               placeholder='Select a parameter',
                               ),
                  html.Label('Y-Axis Type', className='label'),
                  dcc.RadioItems(
            id='yaxis-type',
            options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
            value='Linear',
            labelStyle={'display': 'inline-block'}
        )], className='wrapper'),
        html.Div([html.H2('Output'),
                  dcc.Loading(type='circle', color='#4c72b0', children=[
                      html.Div(id='output_container',
                               className='output container', children=[])
                  ])], className='wrapper')], id='user_input', className='container'),
    html.Main(children=[html.H2('Display'),
                        dcc.Graph(id='linechart', responsive=True, figure={})], id='display', className='container')
], id='root')


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
            results = facility.get_values_by_location(
                location, parameter)
            columns = facility.get_fields()
            df = pd.DataFrame(results, columns=columns)
            df.sort_values(by='datetime')
            df['value'].fillna(
                value=df['detection_limit']/2, inplace=True)
            # if df.empty:
            #     return 'No data to display 1', px.line(None)
            desc_list = list(df['value'].describe(
            ).reset_index().itertuples(index=False, name=None))
            summary = html.Ul(
                id='sum-list', children=[html.Li(f"{i[0]}: {i[1]}") for i in desc_list])

            # Plotly Express
            fig = px.line(
                df,
                x='datetime',
                y='value',
                title='Time vs Concentration',
                labels={
                    "datetime": "Date",
                    "value": f"Concentration ({df.unit[0]})"
                },
                markers=True,
            )
            fig.update_yaxes(type='linear' if yaxis_type ==
                             'Linear' else 'log')
            fig.update_layout(transition_duration=250)
            return summary, fig

        except KeyError:
            return 'No data for selection 2', px.line(None)

    else:
        return '', px.line(None)


@app.callback(
    Output('parameter', 'options'),
    Input('location', 'value'),
)
def update_params(location):
    print(location)
    params = facility.get_parameters_by_location(location)
    if location:
        return [{'label': param, 'value': param} for param in [p[0] for p in params]]
    return []


if __name__ == '__main__':
    app.run_server(debug=True)
