from dash import html, dcc, Dash, Input, Output, callback
import plotly.graph_objects as go
import dash
import base64

app = dash.Dash(__name__, assets_folder='Resources')

# Keep to remove the default padding and margin.
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
values = [450, 300, 150, 100]

fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

app.layout = html.Div(style={'width': '100%', 'height': '100vh', 'overflow': 'hidden'},
                      children=[
                          # Left Container
                          html.Div(id='image-container', style={'width': '70%', 'height': '100vh', 'float': 'left', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'justifyContent': 'center', 'backgroundColor': 'rgba(43, 53, 59, 1)'}),

                          # Right Container
                          html.Div([
                              html.Img(src=app.get_asset_url('Arkwiz_Logo.png'), style={'width': '60%', 'height': 'auto', 'display': 'block', 'marginLeft': 'auto', 'marginRight': 'auto', 'marginTop': '20px'}),

                              dcc.Upload(
                                    id='upload-image',
                                    children=html.Button('Upload Image', id='open-file-dialog-btn', style={'height': '80px', 'width': '200px', 'backgroundColor': 'rgba(18, 88, 103, 1)', 'color': 'rgba(255, 255, 255, 1)', 'fontFamily': 'Arial', 'fontWeight': 'bold', 'fontSize': '24px', 'borderWidth': '1px', 'borderStyle': 'none', 'borderRadius': '10px', 'textAlign': 'center', 'margin': 'auto', 'display': 'block'}),
                                    style={
                                        'width': '60%', 'height': '60px', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'none', 'borderRadius': '0px', 'textAlign': 'center', 'margin': '110px auto', 'marginBottom': '10px'
                                    },
                                  multiple=False,
                                  accept='.jpg'
                              ),

                              html.Div([
                                  dcc.Graph(id='classification-graph', figure=fig),
                              ], style={'marginTop': '20px'}),
                          ], style={'width': '30%', 'height': '100vh', 'float': 'right', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'flex-start', 'backgroundColor': 'rgba(88, 98, 105, 1)'})
                      ])
@callback(Output('image-container', 'children'),
          Input('upload-image', 'contents'))

def update_image(contents):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        img_src = f'data:image/jpg;base64,{content_string}'
        return html.Img(src=img_src, style={'maxWidth': '100%', 'maxHeight': '55vh', 'marginLeft': '5px', 'float': 'left'})
    return html.H1('Please upload the image you wish to classify!', style={'color': 'white', 'fontFamily': 'Arial'})

if __name__ == '__main__':
    app.run_server(debug=True)
