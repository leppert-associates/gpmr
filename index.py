from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from routes import notfound, home, data


app.layout = html.Div([
    dcc.Store(id='store'),
    dcc.Location(id='url', refresh=False),
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
    html.Aside(children=[], id='user_input', className='container'),
    html.Main(children=[], id='display', className='container'),
    html.P(id='store-value')
], id='root')


def get_layouts(page):
    return page.user_input, page.display


@ app.callback(Output('user_input', 'children'),
               Output('display', 'children'),
               Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return get_layouts(home)
    elif pathname == '/routes/data':
        return get_layouts(data)
    else:
        return get_layouts(notfound)


# add a click to the appropriate store
@ app.callback(Output('store', 'data'),
               Input('dtype', 'value'),
               State('store', 'data'))
def on_click(value, data):
    if value is None:
        raise PreventUpdate
    data = data or {'dtype': ''}
    data['dtype'] = value
    return data


# output the stored data
@ app.callback(Output('store-value', 'children'),
               Input('store', 'modified_timestamp'),
               State('store', 'data'))
def on_data(ts, data):
    if ts is None:
        raise PreventUpdate
    data = data or {}
    return data.get('dtype', 0)


if __name__ == '__main__':
    app.run_server(debug=True)
