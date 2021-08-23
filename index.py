import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from routes import notfound, home, data


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Nav([
        html.Div([
            html.Img(src=app.get_asset_url('favicon.ico')),
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
    html.Main(children=[], id='display', className='container')
], id='root')


def get_layouts(page):
    return page.user_input, page.display


@app.callback(Output('user_input', 'children'),
              Output('display', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return get_layouts(home)
    elif pathname == '/routes/data':
        return get_layouts(data)
    else:
        return get_layouts(notfound)


if __name__ == '__main__':
    app.run_server(debug=True)
