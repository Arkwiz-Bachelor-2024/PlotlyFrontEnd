from dash import html, dcc, Dash, Input, Output, callback
import plotly.graph_objects as go
import dash
import base64
from datetime import datetime

app = Dash(__name__, assets_folder='Resources')

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body style="margin:0; padding:0;">
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

labels = ['TREE', 'WATER', 'BUILDING', 'GRASS']
values = [250, 300, 150, 200]

fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=['#24AECB', '#187588', '#0F4A56', '#061F24']),
                             textinfo='label+percent',
                             insidetextfont=dict(color='white', size=10),
                             outsidetextfont=dict(color='white', size=10),)])
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')


start_time = datetime.now()

app.layout = html.Div(style={'width': '100%', 'height': '100vh', 'overflow': 'hidden'},
                      children=[
                          # Left Container
                          html.Div(style={
                              'width': '70%',
                              'height': '100vh',
                              'float': 'left',
                              'display': 'flex',
                              'flexDirection': 'column',
                              'backgroundColor': 'rgba(43, 53, 59, 1)',
                          },
                              children=[

                                  # Container for the original and classified images
                                  html.Div(style={
                                      'flexGrow': '1',
                                      'display': 'flex',
                                      'flexDirection': 'row',
                                      'alignItems': 'center',
                                      'justifyContent': 'space-evenly',
                                      'marginTop': '20px',
                                  },

                                           children=[
                                               html.Div(id='original-image',
                                                        style={
                                                            'maxWidth': '100%',
                                                            'maxHeight': '30vh',
                                                            'marginLeft': '5px',
                                                            'float': 'left'}),

                                               html.Div(id='classified-image',
                                                        style={'maxWidth': '100%', 'maxHeight': '30vh',
                                                               'marginLeft': '5px', 'float': 'left'}),
                                           ]),
                                  # Container for Size, Accuracy, Time
                                  html.Div(style={
                                      'display': 'flex',
                                      'justifyContent': 'space-evenly',
                                      'color': 'white',
                                      'padding': '10px',
                                      'fontFamily': 'Arial',
                                      'fontWeight': 'bold',
                                      'fontSize': '24px',
                                      'margin': '20px'
                                  },

                                           children=[
                                               html.Div(id='image-size', children='Size: '),
                                               html.Div(id='accuracy', children='Accuracy: '),
                                               html.Div(id='timer', children='Time: 0'),
                                           ]),
                                  dcc.Interval(id='update-time', interval=1000, n_intervals=0),  # Timer


                              ]),

                          # Right Container
                          html.Div([
                              html.Img(src=app.get_asset_url('Arkwiz_Logo.png'),
                                       style={
                                           'width': '60%',
                                           'height': 'auto',
                                           'display': 'block',
                                           'marginLeft': 'auto',
                                           'marginRight': 'auto',
                                           'marginTop': '20px'}),

                              html.Div(id='file-path', children='No file selected',
                                       style={
                                           'color': 'white',
                                           'textAlign': 'center',
                                           'margin': 'auto',
                                           'fontFamily': 'Arial',
                                           'fontWeight': 'bold',
                                           'fontSize': '20px',
                                           'marginTop': '60px'}),

                              dcc.Upload(
                                  id='upload-image',
                                  children=html.Button('Upload Image', style={
                                      'height': '80px', 'width': '200px',
                                      'backgroundColor': 'rgba(18, 88, 103, 1)',
                                      'color': 'rgba(255, 255, 255, 1)',
                                      'fontFamily': 'Arial',
                                      'fontWeight': 'bold', 'fontSize': '24px',
                                      'borderWidth': '1px',
                                      'borderStyle': 'none',
                                      'borderRadius': '10px',
                                      'textAlign': 'center',
                                      'margin': 'auto',
                                      'display': 'block'}),

                                  style={
                                      'width': '60%',
                                      'height': '60px',
                                      'lineHeight': '60px',
                                      'borderWidth': '1px',
                                      'borderStyle': 'none',
                                      'borderRadius': '0px',
                                      'textAlign': 'center',
                                      'margin': '110px auto',
                                      'marginBottom': '10px'},

                                  multiple=False,
                                  accept='.tiff , .jpg'
                              ),
                              html.Div([
                                  dcc.Graph(id='classification-graph', figure=fig),
                              ], style={'marginTop': '20px'}),
                          ], style={
                              'width': '30%',
                              'height': '100vh',
                              'float': 'right',
                              'display': 'flex',
                              'flexDirection': 'column',
                              'justifyContent': 'flex-start',
                              'backgroundColor': 'rgba(88, 98, 105, 1)'})
                      ])


@callback(
    [Output('original-image', 'children'),
     Output('classified-image', 'children')],
    [Input('upload-image', 'contents')]
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
    Output('file-path', 'children'),
    [Input('upload-image', 'filename')]
)
def update_file_path(filename):
    if filename is not None:
        return filename
    return 'No file selected'


@callback(
    Output('timer', 'children'),
    [Input('update-time', 'n_intervals')]
)
def update_timer(n):
    global start_time
    time_elapsed = datetime.now() - start_time
    return f"Time: {time_elapsed.seconds}"


if __name__ == '__main__':
    app.run_server(debug=True)
