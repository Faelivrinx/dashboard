import re
import string, random, time
import pandas as pd
from collections import Counter, defaultdict
from math import log

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import utility as util

app = dash.Dash()


# input = "Sie treffen sich gerne im Park. Meistens gehen sie dann zusammen Eis essen. Danach gehen sie manchmal noch einkaufen. Ricarda kauft am liebsten neue Schuhe. Maike kauft sich lieber neuen Schmuck. Am Abend gehen sie gern ins Kino. Maike übernachtet dann oft bei Ricarda."
input = "These functions cannot be used with complex numbers; use the functions."

english_text = open('hunger_game.txt', 'r').read()
german_text = open('gutenber.txt', 'r').read()



# Tworzenie ngramów
x = [util.zip_ngrams(w) for w in util.clear_text(english_text).split() if len(w) >= 3]
y = [util.zip_ngrams(w) for w in util.clear_text(input).split() if len(w) >= 3]
z = [util.zip_ngrams(w) for w in util.clear_text(german_text).split() if len(w) >= 3]


english_list = util.flatten_array([util.zip_ngrams(w) for w in util.clear_text(english_text).split() if len(w) >= 3])
german_list = util.flatten_array(z)

array = [{"data": english_list, "language": "English"},{"data": german_list, "language": "German"}]


input_list = [item for sublist in y for item in sublist]
keys = set(input_list)



util.find_in_lng("THE", array)
# Policzenie n najczęściej występujących ngramów z listy
# counts_english = Counter(english_list)
# counts_german = Counter(german_list)
# print(counts_english['THE'])
# print(counts_german['THE'])
# print([key for key in counts_english if key[0] == 'THE'])
# print([key for key in german_list if key[0] == 'THE'])
# Procent identyfikujący podobieństwo z językiem
sum_english = 0
sum_german = 0

#Szukamy po ngramach z tekstu podanego przez użytkownika tych, które występują z naszego zbioru danych. Następnie sprawdzamy ile ich jest i wyliczamy procent z wszystkich ngramów.
# Na koniec wyliczamy z wzoru log(%ngramów) w wartości bezwględnej i dodajemy do sumy.
# WZÓR Z INTERNETU (ma jakiś sens), MOZE UDA SIE LEPSZY ZNALEZC? Występuje problem gdy mała ilość tekstu podanego przez użytkownika
# for search in keys:
#     for key in counts_english:
#         if search == key[0]:
#             print("English:" + key[0] + " with freq: " + str(key[1]))
#             perc = key[1]/english_length
#             sum_english += abs(log(perc))
#
# for search in keys:
#     for key in counts_german:
#         if search == key[0]:
#             print("German:" + key[0] + " with freq: " + str(key[1]))
#             perc = key[1]/german_length
#             sum_german += abs(log(perc))


app.layout = html.Div(children=[
dcc.Dropdown(
    id='dd-language',
    options=[
        {'label': 'English', 'value': 'EN'},
        {'label': 'German', 'value': 'DE'}
    ],
    value='Language'
),
    dcc.Graph(id='example',
                figure={'data': [
                go.Bar(x=[ngram[0] for ngram in counts_english], y=[ngram[1] for ngram in counts_english])
                ],
                'layout': go.Layout(title='Language')
                })
])

@app.callback(
    Output(component_id='example', component_property='figure'),
    [Input(component_id='dd-language', component_property='value')]
)
def update_plot(input_value):
    if input_value == "EN":
            fig = {'data': [            go.Bar(x=[ngram[0] for ngram in counts_english], y=[ngram[1] for ngram in counts_english])            ],
            'layout': go.Layout(title='English')
            }
            return fig
    else:
        fig = {'data': [
        go.Bar(x=[ngram[0] for ngram in counts_german], y=[ngram[1] for ngram in counts_german])
        ],
        'layout': go.Layout(title='German')
        }
        return fig

# def update_output_div(input_value):
#     if input_value == 'EN':


if __name__ == '__main__':
    app.run_server()

# print(sum_english)
# print(sum_german)
#
# # Testowe, nie sugerować się za bardzo!
# if sum_english != 0 and sum_english > sum_german:
#     print("It's probably English!")
# else:
#     print("It's probably German!")
