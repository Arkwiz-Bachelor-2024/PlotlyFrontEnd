import dash
from dash import html, dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import base64
import io

# Initialize the Dash app
app = dash.Dash(__name__)

# Sample data for the Plotly graph
x_data = [0, 1, 2, 3, 4]
y_data = [0, 1, 4, 9, 16]

# Create the Plotly figure
fig = go.Figure(data=go.Scatter(x=x_data, y=y_data))

# Define the layout of the app
app.layout = html.Div([
    html.H1('Hello Dash'),
    html.Div('''Dash: A web application framework for your data.'''),
    dcc.Graph(id='example-graph', figure=fig),
    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload File'),
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
])

@app.callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'filename'),
    State('upload-data', 'contents')
)
def update_output(uploaded_filenames, uploaded_file_contents):
    # Check if there are files
    if uploaded_filenames is not None and uploaded_file_contents is not None:
        # Process each file
        children = [
            html.Div([
                html.H6(filename),
                # You can add more file processing here
            ]) for filename in uploaded_filenames
        ]
        return children

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
