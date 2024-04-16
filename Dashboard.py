from celery import Celery
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

import glob
from PIL import Image
import pandas as pd
from utils.image_preparation import dictionary_to_array
from utils.image_divider import split_image, merge_images_from_array
from mask_extractor import extract_masks


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

labels = ["TREE", "WATER", "BUILDING", "GRASS"]
values = [250, 300, 150, 200]

fig = go.Figure(
    data=[
        go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=["#24AECB", "#187588", "#0F4A56", "#061F24"]),
            textinfo="label+percent",
            insidetextfont=dict(color="white", size=10),
            outsidetextfont=dict(color="white", size=10),
        )
    ]
)
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")


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
                        html.Div(id="image-size", children="Size: "),
                        html.Div(id="accuracy", children="Accuracy: "),
                        html.Div(id="timer", children="Time: 0"),
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
                        dcc.Graph(id="classification-graph", figure=fig),
                    ],
                    className="graph-container",
                ),
            ],
        ),
    ],
)


@callback(
    [Output("original-image", "children"), Output("classified-image", "children")],
    [Input("upload-image-button", "contents")],
)
def update_image(contents):
    if contents is None:
        raise PreventUpdate

    img = Image.open("ImageExtractor\\Images\\output_image.tif")

    original_image = html.Img(src=contents, className="image")
    classified_image = html.Img(src=contents, className="image")
    return original_image, classified_image


@callback(Output("timer", "children"), [Input("update-time", "n_intervals")])
def update_timer(n):
    global start_time
    time_elapsed = datetime.now() - start_time
    return f"Time: {time_elapsed.seconds}"


@app.callback(
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
            return "Latitude or longitude is out of range."

        else:
            parameters["center_lat"] = lat
            parameters["center_lon"] = lon
            save_parameters(parameters)
            subprocess.run(["python", "ImageExtractor/GG_Main.py"], check=True)
            merge_images_from_array(dictionary_to_array(extract_masks()),"./ImageExtractor/Images/ClassifiedImage.tif")
            return f"Coordinates: {lat}, {lon}"
    except ValueError:
        return "Invalid coordinates format."


if __name__ == "__main__":
    app.run_server(debug=True)
