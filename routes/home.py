import dash_core_components as dcc
import dash_html_components as html

user_input = [
    html.H2('Inputs'),
    html.Label('Data Type'),
    dcc.Dropdown(id='data',
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
    html.P('Welcome to the groundwater protection monitoring report application.'),
    html.P('Please select a data type to view.')
]
