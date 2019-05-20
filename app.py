import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
from dash.dependencies import Input, Output

import dataController as data
import uiController as ui

# load app data
languageMap = data.loadInitialData()

# create app
app = dash.Dash()

languagesList = set([language["language"] for language in languageMap])

# ui.init(app)
app.layout = html.Div(children=[
    ui.createTabs(),
    ui.createLanguagesDropdown(languagesList),
    dcc.Graph(id='example', figure={'data': []})
])

# start application
if __name__ == '__main__':
    app.run_server()
