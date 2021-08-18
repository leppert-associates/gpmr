import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from routes import data


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Nav([
        html.Div([
            html.Img(src=app.get_asset_url('favicon.ico')),
            dcc.Link(
                html.H1('Leppert Associates'), href='/', className='title')
        ], className='flex'),
        html.H1('ECIMS'), dcc.Link('Login', href='/login')
    ]),
    html.Div(id='page-content'),
])


index_layout = html.Div([
    html.Label('Facility'),
    dcc.Dropdown(id='facility',
                 options=[
                     {'label': 'Deer Trail', 'value': 'Deer Trail'}
                 ],
                 multi=False,
                 placeholder='Select a facility',
                 style={'width': '40%'}
                 ),
    html.Div([
        dcc.Link('Data Page', href='/routes/data', className='button'),
        dcc.Link('New Report', href='/routes/data', className='button'),
        dcc.Link('Edit Report', href='/routes/data', className='button'),
    ], className='buttons container')
], className='container')


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/routes/data':
        return data.layout
    else:
        return index_layout


if __name__ == '__main__':
    app.run_server(debug=True)
