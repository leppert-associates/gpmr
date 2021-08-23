from app import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from utils.api import get_data

# grab data from csv, will be sqlite3...
df = get_data()
dfmi = df.set_index(['location', 'parameter', 'datetime']).sort_index()

# Data page
user_input = [
    html.H2('Inputs'),
    html.Label('Monitoring Well'),
    dcc.Dropdown(id='location',
                 options=[
                     {'label': loc, 'value': loc} for loc in df['location'].unique()
                 ],
                 multi=False,
                 placeholder='Select a well'
                 ),
    html.Label('Analyte'),
    dcc.Dropdown(id='parameter',
                 options=[
                     {'label': param, 'value': param} for param in df['parameter'].unique()
                 ],
                 multi=False,
                 placeholder='Select a parameter'
                 ),
    html.H2('Output'),
    html.Div(id='output_container',
             className='output container', children=[])]


display = [html.H2('Display'),
           dcc.Graph(id='linechart', responsive=True, figure=px.line(
               None, template='seaborn'))]


# Connect the Plotly graphs with Dash Components
@ app.callback(
    Output('output_container', 'children'),
    Output('linechart', 'figure'),
    Input('location', 'value'),
    Input('parameter', 'value'),
)
def update_graph(location, parameter):
    if location and parameter:
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
    # keep it empty if no inputs
    else:
        return '', px.line(None, template='seaborn')
