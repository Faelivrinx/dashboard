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
            html.A("dash-board", className="brand-logo", id="project-intro"),
            html.Ul(children=[
                html.Li(children=[html.A(children=[html.I("dashboard",className="material-icons left"),"Prezentacja danych"], className="waves-effect waves-light")], id="data-presentation"),
                html.Li(children=[html.A(children=[html.I("equalizer",className="material-icons left"), "Analiza danych"], className="waves-effect waves-light")], id="data-analysis")
            ],className="right hide-on-med-and-down", id="nav-menu")
        ], className="container")
    ], className="nav-wrapper blue darken-3")

def createSectionHeader(title):
    return html.H3(title, className="bold blue-text text-darken-2")

def createApostrophTitle(title):
    return html.H5(title, className="bold blue-text text-darken-2")

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

# def createMonogramBarGraph(languageMap):
#     return dcc.Graph(id = "monogram-bar-graph", figure=go.Figure(
#         data = createGoBar(languageMap),
#         layout = go.Layout(title="Monogramy w różnych językach", barmode="stack"),

#     ))

# def createBigramBarGraph(languageMap):
#     return dcc.Graph(id = "bigram-bar-graph", figure=go.Figure(
#         data = createGoBar(languageMap),
#         layout = go.Layout(title="Bigramy w różnych językach", barmode="stack")
#     ))

# def createTrigramBarGraph(languageMap):
#     return dcc.Graph(
#         id = "trigram-bar-graph",
#         figure=go.Figure(
#             data = createGoBar(languageMap),
#             layout = go.Layout(title="Trigramy w różnych językach", barmode="stack")
#         )
#     )

def createAnalysisBarGraphNgrams(id):
    return dcc.Graph(
        id = id,
        figure=go.Figure(
            data = [],
            layout = go.Layout(title="Analiza tekstu", barmode="stack")
        )
    )


def crateSelectLanguageDropdown(languages, id):
    return dcc.Dropdown(
        id=id,
        options=[{'label': lang, 'value': lang }for lang in languages],
        value='english',
        clearable=False
    )
def createSelectNGramDropdown(id):
    return dcc.Dropdown(
        id=id,
        options=[
            {'label': 'monograms', 'value': 'monograms'},
            {'label': 'bigrams', 'value': 'bigrams'},
            {'label': 'trigrams', 'value': 'trigrams'}
        ],
        value='monograms',
        clearable=False
    )
def createPieAnalysisGraph(id):
    return dcc.Graph(
        id = id,
        figure=go.Figure(
            data=[
                go.Pie(labels=[],
                        values=[]
                    )],
                layout=go.Layout(title='Wybierz ngram'))
    )

def createPieBar(resultMap):
    languages = [result['language'] for result in resultMap]
    values = [result['value'] for result in resultMap]
    
    figure = go.Figure(
        data=[go.Pie(labels=languages,
                    values=values
                )],
            layout=go.Layout(title="Ngram: " + " '" + resultMap[0]['nGram']+"'"))
    return figure

def createGoBar(languageMap, range = 20):
    bars = []

    for language in languageMap:
        title = language['language']
        data = language['data']
        data = data[:range]
        x = [item[0] for item in data]
        y = [float(item[1])/language['totalDataCount']*100 for item in data]
        bars.append(go.Bar(x=x, y=y, name=title))
    return bars

def createShowPredictionLanguageCard(languageName):
    imgPath = "./assets/img/flags/"+languageName+".png"
    return html.H5(className="blue darken-3 p-2 bold white-text valign-wrapper center-align", children=[
                ("Wyniki analizy, wprowadzony tekst sugeruje język: "), 
                html.Img(className="ml-3", src=imgPath, height="42px")
            ])
