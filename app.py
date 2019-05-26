import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
from dash.dependencies import Input, Output, Event, State
from collections import Counter, defaultdict

import data as data
import ui as ui
import base64

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
            html.Div(id='output-container-button', children='Enter a value and press submit'),
            html.Div(id='output-container-second', children='Enter a value and press'),
            html.Div(id='result-container', children=[
                ui.createAnalysisLangDropdown(data.createLanguageKeysSet(languageMap)),
                ui.createAnalysisNGramDropdown(),
                ui.createAnalysisBarGraphMonograms(),
            ]),
            html.Button(id='analyse-button', children='Analyse'),
            html.Div(id='test_output', children=[])
        ], id='data-analysis-section', className="hide"),
    ],id="main-content", className="container")
], id="main-container")

#callbacks
@app.callback(
    Output('output-container-button', 'children'),
    [Input('analyse-text-btn', 'n_clicks')],
    [State('analyse-text-input', 'value')])
def update_output(n_clicks, value):
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    )


@app.callback(Output('analysis-bar-graph-monograms', 'figure'),
            [Input('analyse-button', 'n_clicks')],
            [State('analysis_lang_dropdown', 'value'),
             State('analysis_ngram_dropdown', 'value'),
             State('analyse-file-upload-input', 'contents'),
             State('analyse-text-input', 'value')])
def try_to_analyse_text(clicks, language, nGramType, fileContent, textContent):
    #If empty and empty: do nothing
    input_arr = []
    # default get from file
    if fileContent != None:
        bytes = base64.b64decode(fileContent)
        decoded_text = bytes.decode("utf-8", 'ignore')
        #prepare data
        selected = data.findLanguageDataByKeyAndNgram(language, nGramType, languageMap)
        flat_map = data.getNgramFlatMap(nGramType, decoded_text)
        monogram_counter = Counter(flat_map)
        mono_data = [[count, monogram_counter[count]]for count in monogram_counter]
        result = {
                "language": "Input",
                "ngramType": nGramType,
                "data": mono_data,
                "totalDataCount": data.sumNgrams(mono_data)
        }
        sorted_result = data.sortData(result)
        sorted_selected = data.sortData(selected)
        input_arr.append(sorted_selected)
        input_arr.append(sorted_result)

        figure = go.Figure(
                data = ui.createGoBar(input_arr),
                layout = go.Layout(title="Analiza tekstu", barmode="stack")
            )
        return figure
    # Get from text area
    elif textContent != None:
        selected = data.findLanguageDataByKeyAndNgram(language, nGramType, languageMap)
        flat_map = data.getNgramFlatMap(nGramType, textContent)
        monogram_counter = Counter(flat_map)
        mono_data = [[count, monogram_counter[count]]for count in monogram_counter]
        result = {
                "language": "Input",
                "ngramType": nGramType,
                "data": mono_data,
                "totalDataCount": data.sumNgrams(mono_data)
        }
        sorted_result = data.sortData(result)
        sorted_selected = data.sortData(selected)
        input_arr.append(sorted_selected)
        input_arr.append(sorted_result)

        figure = go.Figure(
                data = ui.createGoBar(input_arr),
                layout = go.Layout(title="Analiza tekstu", barmode="stack")
            )
        return figure
    return []

@app.callback(Output('test_output', 'children'),
            [Input('analysis-bar-graph-monograms', 'clickData')])
def on_data_clicked(dataClicked):
    print(dataClicked['points'][0]['x'])
    return ''

@app.callback(Output('result-container', 'style'),
            [Input('analyse-button', 'n_clicks')])
def show_container(clicks):
    print(clicks)
    style = {'visibility': 'hidden'}
    if clicks > 0:
        style['visibility'] = 'visible'
    return style

# start application
if __name__ == '__main__':
    app.run_server()
