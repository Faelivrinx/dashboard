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
                    html.Button(className="btn blue darken-2 waves-effect waves-light", children=['Analizuj tekst'], id='analyse-text-btn'),
                    html.Div(id='analyse-text-upload-container', children=[
                        html.Div(className="row mb-3",children=[
                            html.Div(className="col s2", children=[
                                ui.crateSelectLanguageDropdown(data.createLanguageKeysSet(languageMap), "analysis-language-dropdown-text")
                            ]),
                            html.Div(className="col s2", children=[
                                ui.createSelectNGramDropdown("analysis-ngram-dropdown-text"),
                            ])
                        ]),
                        html.Div(className="row",children=[
                            html.Div(className="col s8", children=[
                                ui.createAnalysisBarGraphMonograms("analysis-bar-graph-text")
                            ]),
                            html.Div(className="col s4", children=[
                                ui.createPieAnalysisGraph('analysis-pie-graph-text')
                            ])
                        ])
                    ])
                    ]),
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
                        html.Button(className="btn blue darken-2 waves-effect waves-light mb-4", children=['Analizuj plik'], id='analyse-file-btn'),
                        ui.createShowPredictionLanguageCard("hu"),
                        html.Div(id='analyse-file-upload-container', children=[
                            html.Div(className="row mb-3",children=[
                                html.Div(className="col s2", children=[
                                    ui.crateSelectLanguageDropdown(data.createLanguageKeysSet(languageMap), "analysis-language-dropdown-file")
                                ]),
                                html.Div(className="col s2", children=[
                                    ui.createSelectNGramDropdown("analysis-ngram-dropdown-file"),
                                ])
                            ]),
                            html.Div(className="row",children=[
                                html.Div(className="col s8", children=[
                                    ui.createAnalysisBarGraphMonograms("analysis-bar-graph-file")
                                ]),
                                html.Div(className="col s4", children=[
                                    ui.createPieAnalysisGraph('analysis-pie-graph-file')
                                ])
                            ])
                        ])
                    ])
                ])
            ])
        ], id='data-analysis-section', className="hide"),
    ],id="main-content", className="container")
], id="main-container")


@app.callback(Output('analyse-file-upload-input', 'children'),
                [Input('analyse-file-upload-input', 'filename')])
def update_upload(filename):
    if filename != None:
        return html.Div([
            filename
        ])
    return html.Div([
        'Przeciągnij plik lub ',
        html.A('wybierz')
    ])


@app.callback(Output('analysis-bar-graph-file', 'figure'),
            [Input('analyse-file-btn', 'n_clicks')],
            [State('analysis-language-dropdown-file', 'value'),
             State('analysis-ngram-dropdown-file', 'value'),
             State('analyse-file-upload-input', 'contents')])
def try_to_analyse_text(clicks, language, nGramType, fileContent):
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
    # elif textContent != None:
    #     selected = data.findLanguageDataByKeyAndNgram(language, nGramType, languageMap)
    #     flat_map = data.getNgramFlatMap(nGramType, textContent)
    #     monogram_counter = Counter(flat_map)
    #     mono_data = [[count, monogram_counter[count]]for count in monogram_counter]
    #     result = {
    #             "language": "Input",
    #             "ngramType": nGramType,
    #             "data": mono_data,
    #             "totalDataCount": data.sumNgrams(mono_data)
    #     }
    #     sorted_result = data.sortData(result)
    #     sorted_selected = data.sortData(selected)
    #     input_arr.append(sorted_selected)
    #     input_arr.append(sorted_result)
    #
    #     figure = go.Figure(
    #             data = ui.createGoBar(input_arr),
    #             layout = go.Layout(title="Analiza tekstu", barmode="stack")
    #         )
    #     return figure
    return []

@app.callback(Output('analysis-bar-graph-text', 'figure'),
            [Input('analyse-text-btn', 'n_clicks')],
            [State('analysis-language-dropdown-text', 'value'),
             State('analysis-ngram-dropdown-text', 'value'),
             State('analyse-text-input', 'value')])
def try_to_analyse_text(clicks, language, nGramType, textContent):
    input_arr = []
    if textContent != None:
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


@app.callback(Output('analysis-pie-graph-file', 'figure'),
            [Input('analysis-bar-graph-file', 'clickData')],
            [State('analysis-ngram-dropdown-file', 'value')])
def on_data_clicked(dataClicked, nGramType):
    results = []
    total_count = 0
    nGram = dataClicked['points'][0]['x']
    for lang in languageMap:
        if lang['ngramType'] == nGramType:
            for ngrams in lang['data']:
                if ngrams[0] == nGram:
                    #get percent
                    percent_value = float(ngrams[1])/float(lang['totalDataCount'])*100
                    total_count += percent_value
                    result = {'language': lang['language'], 'nGram': nGram, 'value': percent_value}
                    results.append(result)
    final_result = []
    for result in results:
        result['value'] = result['value'] / total_count * 100
        final_result.append(result)
    figure = ui.createPieBar(final_result)
    return figure

@app.callback(Output('analysis-pie-graph-text', 'figure'),
            [Input('analysis-bar-graph-text', 'clickData')],
            [State('analysis-ngram-dropdown-text', 'value')])
def on_data_clicked(dataClicked, nGramType):
    results = []
    total_count = 0
    nGram = dataClicked['points'][0]['x']
    for lang in languageMap:
        if lang['ngramType'] == nGramType:
            for ngrams in lang['data']:
                if ngrams[0] == nGram:
                    #get percent
                    percent_value = float(ngrams[1])/float(lang['totalDataCount'])*100
                    total_count += percent_value
                    result = {'language': lang['language'], 'nGram': nGram, 'value': percent_value}
                    results.append(result)
    final_result = []
    for result in results:
        result['value'] = result['value'] / total_count * 100
        final_result.append(result)
    figure = ui.createPieBar(final_result)
    return figure

# start application
if __name__ == '__main__':
    app.run_server()
