from dash import html, dcc, Input, Output, callback, State, MATCH, ALL, no_update, Dash
import dash
import sys
import os

# Imports the root directory to the path in order to import project modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

import plotly.graph_objects as go
import base64
import re
from dash.exceptions import PreventUpdate
from datetime import datetime
import json
import subprocess
from math import cos, pi
import pyproj
from PIL import Image
from PIL.ExifTags import TAGS
import pathlib
import csv

from model.metrics import get_class_distribution

import glob
from PIL import Image
import pandas as pd
from utils.image_preparation import dictionary_to_array, prepare_distribution
from utils.image_divider import split_image, merge_images_from_array
from mask_extractor import extract_masks
import plotly.express as px
import numpy as np
import time

PARAMETERS_PATH = "ImageExtractor\\parameters.json"
mask_details = None


def load_parameters():
    try:
        with open(PARAMETERS_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_parameters(parameters):
    with open(PARAMETERS_PATH, "w") as f:
        json.dump(parameters, f, indent=4)


app = Dash(__name__, suppress_callback_exceptions=True, assets_folder="assets")

start_time = datetime.now()

app.layout = html.Div(
    className="main-container",
    children=[
        # Left Container
        html.Div(
            className="left-container",
            children=[
                html.Div(
                    className="images-container",
                    children=[
                        html.Div(id="original-image", className="image"),
                        html.Div(id="classified-image", className="image"),
                    ],
                ),
                html.Div(
                    className="info-container",
                    children=[
                        #html.Div(id="timer", children="Time: 0"),
                    ],
                ),
                dcc.Interval(id="update-time", interval=1000, n_intervals=0),
            ],
        ),
        # Right Container
        html.Div(
            className="right-container",
            children=[
                html.Img(
                    src=app.get_asset_url("images\Arkwiz_Logo.png"), className="logo"
                ),
                dcc.Input(
                    id="latitude-longitude-input",
                    type="text",
                    placeholder="Latitude, Longitude",
                    className="lat-long-input",
                ),
                html.Div(id="checker", className="checker"),
                html.Button(
                    "Classify",
                    id="submit-button",
                    className="classify-button",
                    n_clicks=0,
                ),
                html.Div(
                    [
                        dcc.Graph(id="classification-graph", style={'display': 'none'}),
                    ],
                    className="graph-container",
                ),
                html.Div(id='update-trigger', style={'display': 'none'}),
            ],
        ),
    ],
)


@app.callback(
    Output("classification-graph", "figure"),
    Output("classification-graph", "style"),
    [Input("update-trigger", "children")],
)
def update_pie_chart(class_distribution):
    if not class_distribution:
        raise PreventUpdate

    try:
        with open('class_distribution.txt', 'r') as f:
            distribution_line = f.readline()
            class_distribution = list(map(float, distribution_line.strip('[]').split()))
    except FileNotFoundError as e:
        print(f"Error reading from class_distribution.txt: {e}")
        raise PreventUpdate
    
    labels = ["Background", "Building", "Trees", "Water", "Road"]
    colors=["#24AECB", "#187588", "#0F4A56", "#061F24", "#020B0D"]
    text_colors = ['white' if value < 5 else 'black' for value in class_distribution]

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
    if not trigger_value:
        raise PreventUpdate

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
    parameters = load_parameters()
    script_configs = parameters.get("scripts", {})

    if n_clicks == 0:
        raise PreventUpdate

    try:
        lat, lon = map(float, input_value.split(","))
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            return "Latitude or longitude is out of range.", PreventUpdate

        else:
            parameters["center_lat"] = lat
            parameters["center_lon"] = lon
            save_parameters(parameters)
            subprocess.run(["python", "ImageExtractor/GG_Main.py"], check=True)
            mask_details = extract_masks()

            # Example usage of the distributions
            # Prints out and array of 4 elements consisting of the class distribution over the whole image in percentages
            # 1st is background, 2nd is building, 3rd is trees, 4th is water and 5th is road
            class_distribution = prepare_distribution(dictionary_to_array(mask_details, "class_distribution"))

            with open('class_distribution.txt', 'w') as f:
                f.write(str(class_distribution))

            print(class_distribution)


            merge_images_from_array(
                dictionary_to_array(mask_details,"mask_image"),
                "./ImageExtractor/Images/ClassifiedImage.png",
            )
            return f"Coordinates: {lat}, {lon} with distribution {class_distribution}", str(datetime.now())
    except ValueError:
        return f"Invalid coordinates format.{ValueError}"


if __name__ == "__main__":
    app.run_server(debug=True)
