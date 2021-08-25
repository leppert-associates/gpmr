from dash import dcc
from dash import html

user_input = [
    html.H2('Input'),
    html.Label('Data Type'),
    dcc.Dropdown(id='dtype',
                 options=[
                     {'label': 'Field', 'value': 'Field'},
                     {'label': 'Laboratory', 'value': 'Laboratory'}
                 ],
                 multi=False,
                 placeholder='Select a data type',
                 style={'width': '100%'}
                 ),
    dcc.Link('View Data', href='/routes/data', className='button'),
]


display = [
    html.H2('Display'),
    html.P('This is an example dashboard for groundwater protection monitoring data.'),
    html.P('Please select a data type to view.'),
]
