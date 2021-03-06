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

# UWAGA niniejszy kod był pisany przez osoby które nigdy nie używały pythona, nie było czasu na refaktoryzację kodu, usuwanie zbędnych już nie używanych funkcji i komentowanie, a co dopiero testy jednostkowe :) pozdrawiamy.

# load app data
languageMap = data.loadInitialData()

# create app
app = dash.Dash()

# Main layout
app.layout = html.Div(children=[
    dcc.Interval(id='globalInterval', interval=2 * 1000, n_intervals=0),
    ui.createNavbar(),
    html.Section(children=[
        html.Div(children=[
            # project intro layout
            ui.createSectionHeader("O projekcie"),
            html.Div(className="row",children=[
                html.Div(className="col s12", children=[
                    html.Div(className="card-panel dataIntro1", children=[
                        ui.createApostrophTitle("Cel do osiągnięcia"),
                        html.P("Celem niniejszego projektu było zaprojektowanie kokpitu do interaktywnej prezentacji danych dotyczących różnic w częstotliwości występowania liter, di- oraz trigramów w różnych językach. "
                        + "Językami, które przygotowaliśmy jako dane do porównania pochodzą ze strony: http://practicalcryptography.com oraz przykładowe pliki JSON od innej grupy. "
                        + "Projekt przygotowano z myślą o dołączeniu do niego pozostałych języków, nad którymi pracowały inne grupy tak, by mieć docelowo komplet interaktywnych wizualizacji dla wszystkich 16 języków.", className="")
                    ])]),
                html.Div(className="col s12", children=[
                        html.Div(className="card-panel", children=[
                            html.Img(className="ml-3", src="./assets/img/flags/czech.png", height="42px"),
                            html.Img(className="ml-3", src="./assets/img/flags/english.png", height="42px"),
                            html.Img(className="ml-3", src="./assets/img/flags/german.png", height="42px"),
                            html.Img(className="ml-3", src="./assets/img/flags/hungary.png", height="42px"),
                            html.Img(className="ml-3", src="./assets/img/flags/spanish.png", height="42px")
                        ])
                    ]),
                html.Div(className="col s12", children=[
                    html.Div(className="card-panel", children=[
                        ui.createApostrophTitle("Działanie aplikacji "),
                        html.P("W zależności od celu użytkownika, alikacja pozwala na różne czynności ukryte pod dwiema opcjami ulokowanymi w prawej, górnej części ekranu - Prezentacja danych oraz Analiza danych. ", className=""),
                        html.P("Po wyborze pierwszej z nich, w ręce użytkownika oddane są narzędzia, dzięki którym może on wybrać spośród różnych dostępnych języków oraz wyświetlić częstotliwość występujących w nim n-gramów. "
                        + "Po zaznaczeniu konkretnego n-gramu wyświetlany jest wykres kołowy ilustrujący częstotliwość jego występowania w innych językach. ", className=""),
                        html.P("Po wyborze sekcji analizy, użytkownik dostaje do wyboru możliwość analizy wklejonego tekstu, bądź też tekstu z załadowanego pliku. "
                        + "W obydwu przypadkach analiza odbywa się w ten sam sposób - po wklejeniu tekstu/załadowaniu pliku użytkownik wybiera do którego spośród dostępnych języków chce porównać swoje dane oraz w jakim n-gramie chce dostać wyniki. "
                        + "Podobnie, jak w sekcji prezentacji danych, po wyborze konkretnego n-gramu pojawia się wykres kołowy dodatkowych informacji na jego temat.", className="")
                    ])]),
                html.Div(className="col s12", children=[
                    html.Div(className="card-panel blue white-text dataIntro1", children=[
                        html.P(className="bold white-text", children=["Autorzy: Baczyński Konrad, Bigaj Adam, Jurasz Dominik"])
                    ])]),
            ])
        ], id='project-intro-section', className="hide"),
        html.Div(children=[
            # Data presentation
            ui.createSectionHeader("Prezentacja danych"),
            html.Div(className="card-panel", children=[
                html.Div(className="row mb-3",children=[
                    html.Div(className="col s6 m4 l2", children=[
                        ui.crateSelectLanguageDropdown(data.createLanguageKeysSet(languageMap), "presentation-language-dropdown")
                    ]),
                    html.Div(className="col s6 m4 l2", children=[
                        ui.createSelectNGramDropdown("presentation-ngram-dropdown"),
                    ])
                ]),
                html.Div(className="row",children=[
                    html.Div(className="col m12 l8", children=[
                        ui.createAnalysisBarGraphNgrams("presentation-bar-graph"),
                        dcc.Slider(
                            id='presentation-items-slider',
                            min=3,
                            max=45,
                            value=15,
                            step=3
                        )
                    ]),
                    html.Div(className="col m12 l4", children=[
                        ui.createPieAnalysisGraph('presentation-pie-graph')
                    ])
                ])
            ])
        ], id='data-presentation-section', className="hide"),
        html.Div(children=[
            # Data analysis
            ui.createSectionHeader("Analiza danych"),
            html.Ul(className="collapsible", id="analysis-collapsible", children=[
                html.Li(title="text", children=[
                    html.Div(className="collapsible-header", children=[
                        html.I(className="material-icons", children=["short_text"]),
                        "Wczytaj z pola tekstowego"
                    ]),
                    html.Div(className="collapsible-body white", children=[
                        html.Div(className="input-field mb-4", children=[
                        dcc.Textarea(
                            maxLength="2000",
                            className="materialize-textarea",
                            id='analyse-text-input'
                        ),
                        html.Label(htmlFor="input-text",children=["Wklej tekst do analizy"]),
                    ]),
                    html.Div(className="row",children=[
                        html.Div(className="col s12", children=[

                        ], id='flag-container-text')
                    ]),
                    html.Div(className="row mb-3",children=[
                        html.Div(className="col s6 m4 l2", children=[
                            ui.crateSelectLanguageDropdown(data.createLanguageKeysSet(languageMap), "analysis-language-dropdown-text")
                        ]),
                        html.Div(className="col s6 m4 l2", children=[
                            ui.createSelectNGramDropdown("analysis-ngram-dropdown-text"),
                        ])
                    ]),
                    html.Div(id='analyse-text-upload-container', children=[
                        html.Div(className="row",children=[
                            html.Div(className="col m12 l8", children=[
                                ui.createAnalysisBarGraphNgrams("analysis-bar-graph-text")
                            ]),
                            html.Div(className="col m12 l4", children=[
                                ui.createPieAnalysisGraph('analysis-pie-graph-text')
                            ])
                        ])
                    ])
                    ]),
                ]),
                html.Li(title="file", children=[
                    html.Div(className="collapsible-header", children=[
                        html.I(className="material-icons", children=["insert_drive_file"]),
                        "Wczytaj z pliku"
                    ]),
                    html.Div(className="collapsible-body white", children=[
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
                        html.Div(className="row",children=[
                        html.Div(className="col s12", children=[

                        ], id='flag-container-file')
                        ]),
                        html.Div(className="row mb-3",children=[
                            html.Div(className="col s6 m3 l2", children=[
                                ui.crateSelectLanguageDropdown(data.createLanguageKeysSet(languageMap), "analysis-language-dropdown-file")
                            ]),
                            html.Div(className="col s6 m3 l2", children=[
                                ui.createSelectNGramDropdown("analysis-ngram-dropdown-file"),
                            ])
                        ]),
                        html.Div(id='analyse-file-upload-container', children=[
                            html.Div(className="row",children=[
                                html.Div(className="col m12 l8", children=[
                                    ui.createAnalysisBarGraphNgrams("analysis-bar-graph-file")
                                ]),
                                html.Div(className="col m12 l4", children=[
                                    ui.createPieAnalysisGraph('analysis-pie-graph-file')
                                ])
                            ])
                        ])
                    ])
                ])
            ])
        ], id='data-analysis-section', className="hide"),
    ],id="main-content", className="container"),
    html.A(id="helpBtn",className="btn-floating btn-large waves-effect waves-light red pulse", children=[html.I("help_outline",className="material-icons left")])
], id="main-container")

@app.callback(
    Output('presentation-bar-graph', 'figure'),
    [Input('presentation-language-dropdown', 'value'),
     Input('presentation-ngram-dropdown', 'value'),
     Input('presentation-items-slider', 'value')])
def update_graph(language, nGramType, range):
    input_arr = []
    selected = data.findLanguageDataByKeyAndNgram(language, nGramType, languageMap)
    sorted_selected = data.sortData(selected)
    input_arr.append(sorted_selected)
    figure = go.Figure(
                data = ui.createGoBar(input_arr, range),
                layout = go.Layout(title="Analiza tekstu", barmode="stack")
            )
    return figure

@app.callback(Output('presentation-pie-graph', 'figure'),
        [Input('presentation-bar-graph', 'clickData')],
        [State('presentation-ngram-dropdown', 'value')])
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


@app.callback(Output('flag-container-file', 'children'),
            [Input('analyse-file-upload-input', 'contents')])
def update_flag_file(fileContent):
    similarity = []
    if fileContent != None:
        bytes = base64.b64decode(fileContent)
        decoded_text = bytes.decode("utf-8", 'ignore')
        #bigrams
        flat_map_bigrams = data.getNgramFlatMap('bigrams', decoded_text)
        bigrams_counter = Counter(flat_map_bigrams).most_common(n=25)
        bigram_data = [[count[0], count[1]]for count in bigrams_counter]
        result_bigrams = {
                "language": "Input",
                "ngramType": 'bigrams',
                "data": bigram_data,
                "totalDataCount": data.sumNgrams(bigram_data)
        }
        #trigrams
        flat_map_trigrams = data.getNgramFlatMap('trigrams', decoded_text)
        trigrams_counter = Counter(flat_map_trigrams).most_common(n=25)
        trigram_data = [[count[0], count[1]]for count in trigrams_counter]
        result_trigrams = {
                "language": "Input",
                "ngramType": 'trigrams',
                "data": trigram_data,
                "totalDataCount": data.sumNgrams(trigram_data)
        }
        similarity.append(result_bigrams)
        similarity.append(result_trigrams)
        most_probably_language = data.sortBySimilarity(languageMap, similarity)
        return ui.createShowPredictionLanguageCard(most_probably_language['language'])

@app.callback(Output('flag-container-text', 'children'),
            [Input('globalInterval', 'n_intervals')],
            [State('analyse-text-input', 'value')])
def update_flag_file(n, textContent):
    similarity = []
    if textContent != None:
        if len(textContent) > 10:
            flat_map_bigrams = data.getNgramFlatMap('bigrams', textContent)
            bigrams_counter = Counter(flat_map_bigrams).most_common(n=25)
            bigram_data = [[count[0], count[1]]for count in bigrams_counter]
            result_bigrams = {
                    "language": "Input",
                    "ngramType": 'bigrams',
                    "data": bigram_data,
                    "totalDataCount": data.sumNgrams(bigram_data)
            }
            #trigrams
            flat_map_trigrams = data.getNgramFlatMap('trigrams', textContent)
            trigrams_counter = Counter(flat_map_trigrams).most_common(n=25)
            trigram_data = [[count[0], count[1]]for count in trigrams_counter]
            result_trigrams = {
                    "language": "Input",
                    "ngramType": 'trigrams',
                    "data": trigram_data,
                    "totalDataCount": data.sumNgrams(trigram_data)
            }
            similarity.append(result_bigrams)
            similarity.append(result_trigrams)
            most_probably_language = data.sortBySimilarity(languageMap, similarity)
            return ui.createShowPredictionLanguageCard(most_probably_language['language'])
        else:
            return ""


@app.callback(Output('analysis-bar-graph-file', 'figure'),
            [Input('analyse-file-upload-input', 'contents'),
             Input('analysis-language-dropdown-file', 'value'),
             Input('analysis-ngram-dropdown-file', 'value')],[])
def try_to_analyse_text(fileContent, language, nGramType):
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
                "language": "dane",
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

@app.callback(Output('analysis-bar-graph-text', 'figure'),
            [Input('analyse-text-input', 'value'),
             Input('analysis-language-dropdown-text', 'value'),
             Input('analysis-ngram-dropdown-text', 'value')],
            [])
def try_to_analyse_text(textContent, language, nGramType):
    input_arr = []
    if textContent != None:
        selected = data.findLanguageDataByKeyAndNgram(language, nGramType, languageMap)
        flat_map = data.getNgramFlatMap(nGramType, textContent)
        monogram_counter = Counter(flat_map)
        mono_data = [[count, monogram_counter[count]]for count in monogram_counter]
        result = {
            "language": "dane",
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
    app.run_server(host="0.0.0.0", debug=True)
