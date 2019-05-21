import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
from dash.dependencies import Input, Output, Event, State

import data as data
import ui as ui

# load app data
languageMap = data.loadInitialData()

# create app
app = dash.Dash()

# Main layout
app.layout = html.Div(children=[
    ui.createNavbar(),
    html.Section(children=[
        html.Div(children=[
            ui.createSectionHeader("Prezentacja danych"),
            html.Div(className="row", children=[
                ui.createDataPresentationTabMenu(),
                html.Div(id="tab-monograms", className="col s12", children=[
                    # monograms layout
                    html.Div(className="row",children=[
                        html.Div(className="col s7", children=[html.Div(className="card-panel", children=["Ilość wczytanych monogramów"])]),
                        html.Div(className="col s5", children=[html.Div(className="card-panel", children=[
                            dcc.Input(placeholder="Podaj monogram...", type="number",value='',id="monogram-input")])])
                    ]),
                    html.Div(className="row",children=[
                        html.Div(className="col s7", children=[html.Div(className="card-panel", children=[
                            ui.createMonogramBarGraph(data.getMonogramData(languageMap))
                            ])]),
                        html.Div(className="col s5", children=[html.Div(className="card-panel", children=[])])
                    ])
                ]),
                html.Div(id="tab-digrams", className="col s12", children=[html.Div(
                    # digrams layout
                    html.Div(className="row",children=[
                        html.Div(className="col s12", children=[html.Div(className="card-panel", children=[
                            ui.createBigramBarGraph(data.getBigramData(languageMap))
                            ])])
                    ])
                )]),
                html.Div(id="tab-trigrams", className="col s12", children=[html.Div(
                    # trigrams layout
                )])
            ])
        ], id='data-presentation-section', className="hide"),
        html.Div(children=["sekcja analizy"], id='data-analysis-section', className="hide"),
    ],id="main-content", className="container")
], className="yellow lighten-5", id="main-container")

# start application
if __name__ == '__main__':
    app.run_server()
