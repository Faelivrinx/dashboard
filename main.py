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

app = dash.Dash()

# funkcja tworząca z tekstu ngramy
def zip_ngrams(text, n=3, exact=True):
    return ["".join(j).upper() for j in zip(*[text[i:] for i in range(n)])]

# input = "Sie treffen sich gerne im Park. Meistens gehen sie dann zusammen Eis essen. Danach gehen sie manchmal noch einkaufen. Ricarda kauft am liebsten neue Schuhe. Maike kauft sich lieber neuen Schmuck. Am Abend gehen sie gern ins Kino. Maike übernachtet dann oft bei Ricarda."
input = "These functions cannot be used with complex numbers; use the functions."

english_text = open('hunger_game.txt', 'r').read()
german_text = open('gutenber.txt', 'r').read()


# Usuwanie nieznaczących danych dla poszczególnych języków
# TODO: Usprawnić, jakaś funkcja przyjmująca listę języków i zwracając przerobioną listę?
english_text = re.sub(r'\d+', '', english_text)
english_text = english_text.translate(str.maketrans('','',string.punctuation))
english_text = english_text.strip()

german_text = re.sub(r'\d+', '', german_text)
german_text = german_text.translate(str.maketrans('','',string.punctuation))
german_text = german_text.strip()

input = re.sub(r'\d+', '', input)
input = input.translate(str.maketrans('','',string.punctuation))
input = input.strip()

# Tworzenie ngramów
x = [zip_ngrams(w) for w in english_text.split() if len(w) >= 3]
y = [zip_ngrams(w) for w in input.split() if len(w) >= 3]
z = [zip_ngrams(w) for w in german_text.split() if len(w) >= 3]

# Scalanie ngramów do jednej listy w celu łatwiejszego operowania na nich
english_list = [item for sublist in x for item in sublist]
english_length = len(english_list)

german_list = [item for sublist in z for item in sublist]
german_length = len(german_list)

input_list = [item for sublist in y for item in sublist]
keys = set(input_list)

# Policzenie n najczęściej występujących ngramów z listy
counts_english = Counter(english_list).most_common(n=50)
counts_german = Counter(german_list).most_common(n=50)


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
            fig = {'data': [
            go.Bar(x=[ngram[0] for ngram in counts_english], y=[ngram[1] for ngram in counts_english])
            ],
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
