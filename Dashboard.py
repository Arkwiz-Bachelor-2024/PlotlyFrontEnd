from dash import html, dcc, Dash, Input, Output, callback, State, MATCH, ALL, no_update

import plotly.graph_objects as go
import dash
import base64
import re
from dash.exceptions import PreventUpdate
from datetime import datetime
import json
import subprocess
from math import cos, pi
import pyproj

PARAMETERS_PATH = 'ImageExtractor\\parameters.json'

def load_parameters():
    try:
        with open(PARAMETERS_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    

def save_parameters(parameters):
    with open(PARAMETERS_PATH, 'w') as f:
        json.dump(parameters, f, indent=4)

app = Dash(__name__, suppress_callback_exceptions=True, assets_folder='assets')

labels = ['TREE', 'WATER', 'BUILDING', 'GRASS']
values = [250, 300, 150, 200]

fig = go.Figure(data=[go.Pie(labels=labels, values=values,
                             marker=dict(colors=['#24AECB', '#187588', '#0F4A56', '#061F24']),
                             textinfo='label+percent',
                             insidetextfont=dict(color='white', size=10),
                             outsidetextfont=dict(color='white', size=10),)])
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')


start_time = datetime.now()

app.layout = html.Div(className='main-container', children=[
    #Left Container
    html.Div(className='left-container', children=[
        html.Div(className='images-container', children=[
            html.Div(id='original-image', className='image'),
            html.Div(id='classified-image', className='image'),
        ]),
        html.Div(className='info-container', children=[
            html.Div(id='image-size', children='Size: '),
            html.Div(id='accuracy', children='Accuracy: '),
            html.Div(id='timer', children='Time: 0'),
        ]),
        dcc.Interval(id='update-time', interval=1000, n_intervals=0),
    ]),

    #Right Container
    html.Div(className='right-container', children=[
        html.Img(src=app.get_asset_url('images\Arkwiz_Logo.png'), className='logo'),
        dcc.Input(id='latitude-longitude-input', type='text',
                  placeholder='Latitude, Longitude', className='lat-long-input'),
        html.Div(id='checker', className='checker'),
        html.Button('Classify', id='submit-button', className='classify-button', n_clicks=0),
        html.Div([
            dcc.Graph(id='classification-graph', figure=fig),
        ], className='graph-container'),
    ]),
])


@callback(
    [Output('original-image', 'children'),
     Output('classified-image', 'children')],
    [Input('upload-image-button', 'contents')]
)
def update_image(contents):
    if contents is None:
        no_image_message = "Please upload the image you wish to classify!"
        return html.Div(no_image_message,
                        style={
                            'color': 'white',
                            'textAlign': 'center',
                            'margin': 'auto',
                            'fontFamily': 'Arial',
                            'fontWeight': 'bold',
                            'fontSize': '20px',
                            'marginTop': '60px'}), html.Div(
            no_image_message, style={
                'color': 'white',
                'textAlign': 'center',
                'margin': 'auto',
                'fontFamily': 'Arial',
                'fontWeight': 'bold',
                'fontSize': '20px',
                'marginTop': '60px'})

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    img_src = f'data:image/jpg;base64,{content_string}'
    image_element = html.Img(src=img_src, style={'maxWidth': '100%', 'maxHeight': '40vh', 'marginLeft': '5px'})
    return image_element, image_element


@callback(
    Output('timer', 'children'),
    [Input('update-time', 'n_intervals')]
)
def update_timer(n):
    global start_time
    time_elapsed = datetime.now() - start_time
    return f"Time: {time_elapsed.seconds}"

@callback(
    Output('checker', 'children'),
    [Input('submit-button', 'n_clicks')],
    State('latitude-longitude-input', 'value'),
) 
def on_submit(n_clicks, input_value):
    parameters = load_parameters()
    script_configs = parameters.get('scripts', {})
    
    if n_clicks == 0:
        raise PreventUpdate
    
    try:
        lat, lon = map(float, input_value.split(','))
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            return "Latitude or longitude is out of range."
        
        else:
            parameters["center_lat"] = lat
            parameters["center_lon"] = lon
            save_parameters(parameters)
            subprocess.run(["python", "ImageExtractor/GG_Main.py"], check=True)
            return f"Coordinates: {lat}, {lon}"
    except ValueError:
        return "Invalid coordinates format."


if __name__ == '__main__':
    app.run_server(debug=True)
