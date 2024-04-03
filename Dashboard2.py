from dash import html, dcc, Dash, Input, Output, callback, State, MATCH, ALL, no_update

import plotly.graph_objects as go
import dash
import base64
import re
from dash.exceptions import PreventUpdate
from datetime import datetime

app = Dash(__name__, suppress_callback_exceptions=True, assets_folder='assets')

labels = ['TREE', 'WATER', 'BUILDING', 'GRASS']
values = [250, 300, 150, 200]

fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=['#24AECB', '#187588', '#0F4A56', '#061F24']),
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
        dcc.Input(id='latitude-longitude-input', type='text', placeholder='Latitude, Longitude', className='lat-long-input'),
        html.Div(id='input-validation-message', className='input-validation'),
        dcc.Upload(
            id='upload-image-button',
            children=html.Button('Classify', className='classify-button'),
            className='upload-button',
            multiple=False,
            accept='.tiff , .jpg, .png'
        ),
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
    

@app.callback(
    [Output('upload-image-button', 'children'),
     Output('input-validation-message', 'children')],
    [Input('latitude-longitude-input', 'value')]
)
def check_input(input_value):
    if input_value is None:
        return [html.Button('Classify', className='classify-button', disabled=True), ""]
    try:
        lat, lon = map(str.strip, input_value.split(','))
        lat = float(lat)
        lon = float(lon)
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return [html.Button('Classify', className='classify-button', disabled=False), ""]
        else:
            raise ValueError
    except ValueError:
        return [html.Button('Classify', className='classify-button', disabled=True), "Invalid input. Please enter in the format: Latitude, Longitude"]

if __name__ == '__main__':
    app.run_server(debug=True)
