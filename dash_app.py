# dash_app.py

import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import requests
import base64
from flask import Flask

# Create Flask server
server = Flask(__name__)

# Create Dash app
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

API_URL = 'http://localhost:8000'  # Adjust this if your backend is hosted elsewhere

app.layout = dbc.Container([
    html.H1("Data Analysis App"),

    # File Upload Section
    html.H2("Upload CSV File"),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
        style={
            'width': '100%', 'height': '60px', 'lineHeight': '60px',
            'borderWidth': '1px', 'borderStyle': 'dashed',
            'borderRadius': '5px', 'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    html.Div(id='output-upload'),

    # Ask Question Section
    html.H2("Ask a Question about Your Data"),
    dcc.Input(id='question-input', type='text', placeholder='Enter your question', style={'width': '100%'}),
    html.Button('Get Answer', id='submit-question', n_clicks=0),
    html.Div(id='output-answer'),

    # Visualization Section
    html.H2("Data Visualization"),
    dcc.Input(id='viz-question-input', type='text', placeholder='Enter your visualization request', style={'width': '100%'}),
    html.Button('Generate Visualization', id='submit-viz', n_clicks=0),
    html.Div(id='output-viz'),
])

# Callback for file upload
@app.callback(
    Output('output-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def upload_file(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        files = {'file': (filename, decoded)}
        response = requests.post(f"{API_URL}/upload_csv/", files=files)
        if response.status_code == 200:
            return html.Div(['File uploaded successfully.'])
        else:
            return html.Div(['Failed to upload file.'])
    return ''

# Callback for asking question
@app.callback(
    Output('output-answer', 'children'),
    Input('submit-question', 'n_clicks'),
    State('question-input', 'value'),
    State('upload-data', 'filename')
)
def ask_question(n_clicks, question, filename):
    if n_clicks > 0 and question and filename:
        data = {'question': question, 'filename': filename}
        response = requests.post(f"{API_URL}/ask_question/", data=data)
        if response.status_code == 200:
            answer = response.json().get('response', '')
            return html.Div(['Answer: ', html.B(answer)])
        else:
            return html.Div(['Error: ', response.json().get('error', 'Unknown error')])
    return ''

# Callback for visualization
@app.callback(
    Output('output-viz', 'children'),
    Input('submit-viz', 'n_clicks'),
    State('viz-question-input', 'value'),
    State('upload-data', 'filename')
)
def generate_viz(n_clicks, viz_question, filename):
    if n_clicks > 0 and viz_question and filename:
        data = {'question': viz_question, 'filename': filename}
        response = requests.post(f"{API_URL}/visualize/", data=data)
        if response.status_code == 200:
            # Encode image to display in Dash
            encoded_image = base64.b64encode(response.content).decode()
            return html.Img(src='data:image/png;base64,{}'.format(encoded_image))
        else:
            return html.Div(['Error: ', response.json().get('error', 'Unknown error')])
    return ''

if __name__ == '__main__':
    app.run_server(debug=True)
