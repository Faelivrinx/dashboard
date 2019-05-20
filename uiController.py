import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


def createLanguagesDropdown(languages):
    return dcc.Dropdown(id='dd-language',
                        options=[{
                            'label': language,
                            'value': language
                        } for language in languages],
                        value='wybierz język')


def createTabs():
    return html.Div([
        dcc.Tabs(id="tabs",
                 value='tab-1',
                 children=[
                     dcc.Tab(label='Tab one', value='tab-1'),
                     dcc.Tab(label='Tab two', value='tab-2'),
                 ]),
        html.Div(id='tabs-content')
    ])


@app.callback(Output('tabs-content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([html.H3('Tab content 1')])
    elif tab == 'tab-2':
        return html.Div([html.H3('Tab content 2')])
