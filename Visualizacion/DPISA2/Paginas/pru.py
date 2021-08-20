app.layout = html.Div(
    children=[
        html.Div(
            [
                html.H1(
                    children=[
                        "World Cell Towers",
                        html.A(
                            html.Img(
                                src="assets/dash-logo.png",
                                style={"float": "right", "height": "50px"},
                            ),
                            href="https://dash.plot.ly/",
                        ),
                    ],
                    style={"text-align": "left"},
                ),
            ]
        ),
        html.Div(
            children=[
                build_modal_info_overlay(
                    "indicator",
                    "bottom",
                    dedent(
                        """
            The _**Selected Towers**_ panel displays the number of cell towers
            that are currently selected. A tower is considered to be selected
            if it is currently visible in the _**Locations**_ map, and satisfies
            the selections applied in the _**Radio**_, _**Signal Range**_, and
            _**Construction Date**_ panels.
            The _**Reset All**_ button may be used to clear all selections and
            recenter the _**Locations**_ map view. 
            """
                    ),
                ),
                build_modal_info_overlay(
                    "radio",
                    "bottom",
                    dedent(
                        """
            The _**Radio**_ panel displays a bar chart representing the
            number cell towers with each radio technology.

            The colored bars represent the number of towers that are currently selected
            in the _**Locations**_, _**Signal Range**_, and _**Construction Date**_
            panels. Note that cell tower counts are displayed using a log scale.

            Left-clicking on a colored bar selects the towers with the corresponding
            radio technology.  Holding the shift key while left-clicking extends the
            current selection. A left-click drag may also be used to select multiple
            bars using the box-selection tool. 

            The _**Clear Selection**_ button may be used to clear any selections
            applied in the _**Radio**_ panel, while leaving any selections applied in
            other panels unchanged. 
        """
                    ),
                ),
                build_modal_info_overlay(
                    "map",
                    "bottom",
                    dedent(
                        """
            The _**Locations**_ panel displays the position of each selected tower on
            an interactive world map. Towers are colored by their radio technology with
            colors that match the bars in the _**Radio**_ panel.

            When 5000 or fewer towers are selected, hover tooltips containing
            tower details are available at each tower location. 

            Left-click drag to pan the map view, right-click drag to rotate and pitch
            the map view, and scroll to zoom in and out.  

            The _**Reset View**_ button may be used to reset the map to the original
            centered view, while leaving any selections applied in other panels
            unchanged. 
        """
                    ),
                ),
                build_modal_info_overlay(
                    "range",
                    "top",
                    dedent(
                        """
            The _**Signal Range**_ panel displays a histogram of the signal range of
            each tower in the dataset.  The dark gray bars represent the set of towers
            in the current selection, while the light gray bars underneath represent
            all towers in the dataset.

            Left-click drag to select histogram bars using the box-selection tool.

            The _**Clear Selection**_ button may be used to clear any selections
            applied in the _**Signal Range**_ panel, while leaving any selections
            applied in other panels unchanged.
        """
                    ),
                ),
                build_modal_info_overlay(
                    "created",
                    "top",
                    dedent(
                        """
            The _**Construction Date**_ panel displays a histogram of the construction
            date of each tower in the dataset.  The dark gray bars represent the set of
            towers in the current selection, while the light gray bars underneath
            represent all towers in the dataset.

            Left-click drag to select histogram bars using the box-selection tool.

            The _**Clear Selection**_ button may be used to clear any selections
            applied in the _**Construction Date**_ panel, while leaving any selections
            applied in other panels unchanged.
        """
                    ),
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.H4(
                                    [
                                        "Selected Towers",
                                        html.Img(
                                            id="show-indicator-modal",
                                            src="assets/question-circle-solid.svg",
                                            n_clicks=0,
                                            className="info-icon",
                                        ),
                                    ],
                                    className="container_title",
                                ),
                                dcc.Loading(
                                    dcc.Graph(
                                        id="indicator-graph",
                                        figure=blank_fig(row_heights[0]),
                                        config={"displayModeBar": False},
                                    ),
                                    className="svg-container",
                                    style={"height": 150},
                                ),
                                html.Div(
                                    children=[
                                        html.Button(
                                            "Reset All",
                                            id="clear-all",
                                            className="reset-button",
                                        ),
                                    ]
                                ),
                            ],
                            className="six columns pretty_container",
                            id="indicator-div",
                        ),
                        html.Div(
                            children=[
                                html.H4(
                                    [
                                        "Radio",
                                        html.Img(
                                            id="show-radio-modal",
                                            src="assets/question-circle-solid.svg",
                                            className="info-icon",
                                        ),
                                    ],
                                    className="container_title",
                                ),
                                dcc.Graph(
                                    id="radio-histogram",
                                    figure=blank_fig(row_heights[0]),
                                    config={"displayModeBar": False},
                                ),
                                html.Button(
                                    "Clear Selection",
                                    id="clear-radio",
                                    className="reset-button",
                                ),
                            ],
                            className="six columns pretty_container",
                            id="radio-div",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.H4(
                            [
                                "Locations",
                                html.Img(
                                    id="show-map-modal",
                                    src="assets/question-circle-solid.svg",
                                    className="info-icon",
                                ),
                            ],
                            className="container_title",
                        ),
                        dcc.Graph(
                            id="map-graph",
                            figure=blank_fig(row_heights[1]),
                            config={"displayModeBar": False},
                        ),
                        html.Button(
                            "Reset View", id="reset-map", className="reset-button"
                        ),
                    ],
                    className="twelve columns pretty_container",
                    style={
                        "width": "98%",
                        "margin-right": "0",
                    },
                    id="map-div",
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.H4(
                                    [
                                        "Signal Range",
                                        html.Img(
                                            id="show-range-modal",
                                            src="assets/question-circle-solid.svg",
                                            className="info-icon",
                                        ),
                                    ],
                                    className="container_title",
                                ),
                                dcc.Graph(
                                    id="range-histogram",
                                    figure=blank_fig(row_heights[2]),
                                    config={"displayModeBar": False},
                                ),
                                html.Button(
                                    "Clear Selection",
                                    id="clear-range",
                                    className="reset-button",
                                ),
                            ],
                            className="six columns pretty_container",
                            id="range-div",
                        ),
                        html.Div(
                            children=[
                                html.H4(
                                    [
                                        "Construction Date",
                                        html.Img(
                                            id="show-created-modal",
                                            src="assets/question-circle-solid.svg",
                                            className="info-icon",
                                        ),
                                    ],
                                    className="container_title",
                                ),
                                dcc.Graph(
                                    id="created-histogram",
                                    config={"displayModeBar": False},
                                    figure=blank_fig(row_heights[2]),
                                ),
                                html.Button(
                                    "Clear Selection",
                                    id="clear-created",
                                    className="reset-button",
                                ),
                            ],
                            className="six columns pretty_container",
                            id="created-div",
                        ),
                    ]
                ),
            ]
        ),
        html.Div(
            [
                html.H4("Acknowledgements", style={"margin-top": "0"}),
                dcc.Markdown(
                    """\
 - Dashboard written in Python using the [Dash](https://dash.plot.ly/) web framework.
 - Parallel and distributed calculations implemented using the [Dask](https://dask.org/) Python library.
 - Server-side visualization of the location of all 40 million cell towers performed 
 using the [Datashader] Python library (https://datashader.org/).
 - Base map layer is the ["light" map style](https://www.mapbox.com/maps/light-dark/)
 provided by [mapbox](https://www.mapbox.com/).
 - Cell tower dataset provided by the [OpenCelliD Project](https://opencellid.org/) which is licensed under a
[_Creative Commons Attribution-ShareAlike 4.0 International License_](https://creativecommons.org/licenses/by-sa/4.0/).
 - Mapping from cell MCC/MNC to network operator scraped from https://cellidfinder.com/mcc-mnc.
 - Icons provided by [Font Awesome](https://fontawesome.com/) and used under the
[_Font Awesome Free License_](https://fontawesome.com/license/free). 
"""
                ),
            ],
            style={
                "width": "98%",
                "margin-right": "0",
                "padding": "10px",
            },
            className="twelve columns pretty_container",
        ),
    ]
)
