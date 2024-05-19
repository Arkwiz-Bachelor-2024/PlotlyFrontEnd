from dash import callback, Output, Input, State, no_update, dcc
from dash.exceptions import PreventUpdate
from datetime import datetime
import subprocess
import os
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from PIL import Image
import json

from dashboard.app import app
from utils.image_preparator import prepare_distribution, dictionary_to_array
from utils.image_handler import merge_images_from_array
from utils.mask_extractor import extract_masks


PARAMETERS_PATH = "ImageExtractor\parameters.json"


def load_parameters():
    """
    Load the parameters from a JSON file.
    """
    try:
        with open(PARAMETERS_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_parameters(parameters):
    """
    Save the parameters to a JSON file.
    """
    with open(PARAMETERS_PATH, "w") as f:
        json.dump(parameters, f, indent=4)

@app.callback(
    Output("classification-graph", "figure"),
    Output("classification-graph", "style"),
    [Input("update-trigger", "children")],
)
def update_pie_chart(class_distribution):
    """
    This function is called when the image is downloaded and is done classifying.
    It will display the classification distribution on the dashboard as a pie chart.
    """

    if not class_distribution:
        raise PreventUpdate

    try:
        # Read the class distribution from the file
        with open('dashboard/class_distribution.txt', 'r') as f:
            distribution_line = f.readline()
            class_distribution = list(map(float, distribution_line.strip('[]').split()))
    except FileNotFoundError as e:
        # If the file is not found, raise an error
        print(f"Error reading from class_distribution.txt: {e}")
        raise PreventUpdate
    
    labels = ["Background", "Building", "Trees", "Water", "Road"]
    colors=["#24AECB", "#187588", "#0F4A56", "#061F24", "#020B0D"]
    text_colors = ['white']

    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=class_distribution,
            hole=0.3,
            textposition="inside",
            insidetextorientation="horizontal",
            marker=dict(colors=colors, line=dict(color='white', width=2)),
            textinfo="label + percent",
            outsidetextfont=dict(color='black', size=12),
            insidetextfont=dict(color=text_colors, size=12),
        )
    )
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=300,
        width=300,
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False)
    )

    return fig, {'display': 'block'}


@app.callback(
    [Output("original-image", "children"), 
     Output("classified-image", "children")],
    [Input("update-trigger", "children")]
)
def update_image(trigger_value):
    """
    This function is called when the image is downloaded and is done classifying.
    It will display the original and classified images on the dashboard.
    """
    if not trigger_value:
        raise PreventUpdate
    
    # Load the images
    img_path_original = "ImageExtractor\\Images\\output_image.tif"
    img_path_classified = "ImageExtractor\\Images\\ClassifiedImage.png"

    if not os.path.exists(img_path_original) or not os.path.exists(img_path_classified):
        raise PreventUpdate

    img_original = np.array(Image.open(img_path_original))
    img_classified = np.array(Image.open(img_path_classified))
    
    fig_original = px.imshow(img_original)
    fig_original.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
    )
    fig_original.update_layout(coloraxis_showscale=False)
    fig_original.update_xaxes(showticklabels=False)
    fig_original.update_yaxes(showticklabels=False)

    fig_classified = px.imshow(img_classified)
    fig_classified.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
    )
    fig_classified.update_layout(coloraxis_showscale=False)
    fig_classified.update_xaxes(showticklabels=False)
    fig_classified.update_yaxes(showticklabels=False)

    return dcc.Graph(figure=fig_original), dcc.Graph(figure=fig_classified)


@callback(Output("timer", "children"), 
          [Input("update-time", "n_intervals")])
def update_timer(n):
    global start_time
    time_elapsed = datetime.now() - start_time
    return f"Time: {time_elapsed.seconds}"


@app.callback(
    Output("update-trigger", "children"),    
    Output("checker", "children"),
    [Input("submit-button", "n_clicks")],
    State("latitude-longitude-input", "value"),
)
def on_submit(n_clicks, input_value):
    """
    This function is called when the submit button is clicked.
    It will classify the image and return the classification results.
    """
    parameters = load_parameters()

    if n_clicks == 0:
        raise PreventUpdate

    try:
        lat, lon = map(float, input_value.split(","))
        # Check if the coordinates are valid
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            # If the coordinates are invalid, return an error message
            return no_update, "Invalid coordinates."
        

        else:
            # If the coordinates are valid, classify the image
            message = "Classified for coordinates: {}, {}".format(lat, lon)

            parameters["center_lat"] = lat
            parameters["center_lon"] = lon
            save_parameters(parameters)
            subprocess.run(["python", "ImageExtractor/GG_Main.py"], check=True)
            mask_details = extract_masks()

            # Example usage of the distributions
            # Prints out and array of 4 elements consisting of the class distribution over the whole image in percentages
            # 1st is background, 2nd is building, 3rd is trees, 4th is water and 5th is road
            class_distribution = prepare_distribution(dictionary_to_array(mask_details, "class_distribution"))

            with open('dashboard/class_distribution.txt', 'w') as f:
                f.write(str(class_distribution))

            print(class_distribution)


            merge_images_from_array(
                dictionary_to_array(mask_details,"mask_image"),
                "./ImageExtractor/Images/ClassifiedImage.png",
            )
            return str(datetime.now()), message
    except ValueError:
        return no_update, f"Invalid coordinates format."
    
    
    

@app.callback(
    Output("download-start-dialog", "displayed"),
    [Input("submit-button", "n_clicks")],
    State("latitude-longitude-input", "value"),
)
def handle_submit(n_clicks, input_value):
    if n_clicks == 0:
        raise PreventUpdate
    
    try:
        lat, lon = map(float, input_value.split(","))
        # Check if the coordinates are valid
        if (-90 <= lat <= 90 and -180 <= lon <= 180):
            # If the coordinates are invalid, return an error message
            return True
    except ValueError:
        pass
    return False    