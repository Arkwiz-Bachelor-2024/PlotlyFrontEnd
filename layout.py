from dash import html, dcc
from app import app


def init_layout():
    # Layout of the dashboard
    app.layout = html.Div(
        className="main-container",
        children=[
            dcc.ConfirmDialog(
                id='download-start-dialog',
                message='Classification started. Please wait...',
                displayed=False
            ),
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




if __name__ == "__main__":
    app.run_server(debug=True)
