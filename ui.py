import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.plotly as py
import plotly.graph_objs as go


def createLanguagesDropdown(languages):
    return dcc.Dropdown(id='dd-language',
                        options=[{
                            'label': language,
                            'value': language
                        } for language in languages],
                        value='wybierz język')

def createNavbar():
    return html.Nav(children=[
        html.Div(children=[
            html.A("dash-board", className="brand-logo"),
            html.Ul(children=[
                html.Li(children=[html.A(children=[html.I("dashboard",className="material-icons left"),"Prezentacja danych"], className="waves-effect waves-light")], id="data-presentation"),
                html.Li(children=[html.A(children=[html.I("equalizer",className="material-icons left"), "Analiza danych"], className="waves-effect waves-light")], id="data-analysis")
            ],className="right hide-on-med-and-down", id="nav-menu")
        ], className="container")
    ], className="nav-wrapper blue darken-3")

def createSectionHeader(title):
    return html.H3(title, className="bold blue-text text-darken-2")

def createDataPresentationTabMenu():
    return html.Div(className="col s12", children=[
                html.Ul(className="tabs card", children=[
                    html.Li(className="tab col s4", children=[
                        html.A("Monogramy", href="#tab-monograms", className="waves-effect waves-dark")
                    ]),
                    html.Li(className="tab col s4", children=[
                        html.A("Digramy", href="#tab-digrams", className="waves-effect waves-dark")
                    ]),
                    html.Li(className="tab col s4", children=[
                        html.A("Trigramy", href="#tab-trigrams", className="waves-effect waves-dark")
                    ])
                ])
            ])

def createMonogramBarGraph(languageMap):
    return dcc.Graph(id = "monogram-bar-graph", figure=go.Figure(
        data = createGoBar(languageMap),
        layout = go.Layout(title="Monogramy w różnych językach", barmode="stack"),

    ))

def createBigramBarGraph(languageMap):
    return dcc.Graph(id = "bigram-bar-graph", figure=go.Figure(
        data = createGoBar(languageMap),
        layout = go.Layout(title="Bigramy w różnych językach", barmode="stack")
    ))

def createTrigramBarGraph(languageMap):
    return dcc.Graph(
        id = "trigram-bar-graph",
        figure=go.Figure(
            data = createGoBar(languageMap),
            layout = go.Layout(title="Trigramy w różnych językach", barmode="stack")
        )
    )

def createGoBar(languageMap):
    bars = []

    for language in languageMap:
        title = language['language']
        data = language['data']
        data = data[:25]
        x = [item[0] for item in data]
        y = [int(item[1])/language['totalDataCount']*100 for item in data]  
        bars.append(go.Bar(x=x, y=y, name=title))
    return bars 