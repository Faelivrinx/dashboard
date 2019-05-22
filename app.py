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
            # Data presentation
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
                    html.Div(className="row",children=[
                        html.Div(className="col s12", children=[html.Div(className="card-panel", children=[
                            ui.createTrigramBarGraph(data.getTrigramData(languageMap))
                            ])])
                    ])
                )])
            ])
        ], id='data-presentation-section', className="hide"),
        html.Div(children=[
            # Data analysis
            ui.createSectionHeader("Analiza danych"),
            html.Ul(className="collapsible",children=[
                html.Li(className="active", children=[
                    html.Div(className="collapsible-header", children=[
                        html.I(className="material-icons", children=["short_text"]), 
                        "Wczytaj z pola tekstowego"
                    ]),
                    html.Div(className="collapsible-body grey lighten-5", children=[
                        html.Div(className="input-field mb-4", children=[
                        dcc.Textarea(
                            maxLength="2000",
                            className="materialize-textarea",
                            id='analyse-text-input'
                        ),
                        html.Label(htmlFor="input-text",children=["Wklej tekst do analizy"]),
                    ]),
                    html.Button(className="btn blue darken-2 waves-effect waves-light", children=['Analizuj tekst'], id='analyse-text-btn')
                    ])
                ]),
                html.Li(children=[
                    html.Div(className="collapsible-header", children=[
                        html.I(className="material-icons", children=["insert_drive_file"]), 
                        "Wczytaj z pliku"
                    ]),
                    html.Div(className="collapsible-body grey lighten-5", children=[
                        dcc.Upload(
                            className="mb-4",
                            id='analyse-file-upload-input',
                            children=html.Div([
                                'Przeciągnij plik lub ',
                                html.A('wybierz')
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px'
                            },
                            multiple=False
                        ),
                        html.Button(className="btn blue darken-2 waves-effect waves-light", children=['Analizuj plik'], id='analyse-file-btn')
                    ])
                ])
            ]),
            html.Div(id='output-container-button', children='Enter a value and press submit')
        ], id='data-analysis-section', className="hide"),
    ],id="main-content", className="container")
], id="main-container")

#callbacks
@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('analyse-text-btn', 'n_clicks')],
    [dash.dependencies.State('analyse-text-input', 'value')])
def update_output(n_clicks, value):
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    )

# start application
if __name__ == '__main__':
    app.run_server()
