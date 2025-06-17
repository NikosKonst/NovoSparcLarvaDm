import os
os.environ['DASH_SERVER_MAX_TIMEOUT'] = '60'

import dash
from dash import dcc, html, Input, Output, State, ctx
import pandas as pd
import plotly.graph_objs as go
import matplotlib.colors as mcolors
import numpy as np
import plotly.io as pio
import base64
from io import BytesIO
from PIL import Image
import io
from sklearn.cluster import KMeans

# Load your normalized CSV data
data_path = 'lessDecimals.csv'
chunk_size = 1000  # Adjust based on available memory
chunks = pd.read_csv(data_path, chunksize=chunk_size)


# Combine all chunks into a single DataFrame (if required)
df = pd.concat(chunks, ignore_index=True)

# Load the gene correlation data
gene_correlation_path = 'Spearman_For2.csv'
chunks2_size = 1000
chunks2 = pd.read_csv(gene_correlation_path, chunksize=chunks2_size)
gene_correlation_data = pd.concat(
    pd.read_csv(gene_correlation_path, chunksize=chunks2_size, index_col=0)
)

# Extract coordinate columns and genes
coords = df[['xcoord', 'ycoord', 'zcoord']]
genes = sorted(df.columns[3:])  # Assuming the first 3 columns are coordinates and sorting genes alphabetically

# Define color options for overlay on greyscale
color_options = {
    'Black (Greyscale)': (0, 0, 0),
    'Yellow': (1, 1, 0),
    'Green': (0, 1, 0),
    'Red': (1, 0, 0),
    'Blue': (0, 0, 1),
    'Cyan': (0, 1, 1),
    'Magenta': (1, 0, 1)
}

# Create a Dash app
app = dash.Dash(__name__)

# Define the layout

app.layout = html.Div([
    html.H1("3D Novosparc Reconstruction of Drosophila Developing Optic Lobe single cell data", style={'text-align': 'center'}),

    html.Div([
        # First gene settings
        html.Div([
            html.Label("Select the first gene:", style={'font-weight': 'bold'}),
            dcc.Dropdown(
                id='gene-dropdown-1',
                options=[{'label': gene, 'value': gene} for gene in genes],
                value=genes[0],  # Default value
                style={'margin-bottom': '15px'}
            ),
            html.Div([
                html.Label("Top 20 correlated genes:", style={'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='correlated-genes-dropdown',
                    options=[],
                    disabled=False,  # Non-interactive
                    style={'margin-bottom': '15px'}
                )
            ]),

            html.Div(  # Histogram for threshold visualization
                id='threshold-helper-histogram',
                style={'margin-top': '10px', 'margin-bottom': '20px'}
            ),
            html.Label("Choose a color for the first gene:", style={'font-weight': 'bold'}),
            dcc.Dropdown(
                id='color-dropdown-1',
                options=[{'label': color, 'value': color} for color in color_options.keys()],
                value='Red',  # Default value
                style={'margin-bottom': '15px'}
            ),
            html.Label("Set thresholds for visualizing the first gene:", style={'font-weight': 'bold'}),
            html.Div([
                dcc.Input(id='threshold-min-1', type='number', value=0, min=0, max=1, step=0.01,
                          style={'width': '48%', 'margin-right': '5px'}),
                dcc.Input(id='threshold-max-1', type='number', value=1, min=0, max=1, step=0.01,
                          style={'width': '48%'})
            ], style={'display': 'flex', 'margin-bottom': '15px'}),
        ], style={'width': '48%', 'display': 'inline-block'})
    ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '30px'}),

    # Second gene settings
    html.Div([
        html.Label("Enable second gene visualization:", style={'font-weight': 'bold'}),
        dcc.Checklist(
            id='second-gene-checkbox',
            options=[{'label': '', 'value': 'enable'}],
            value=[],  # Default unchecked
            style={'margin-bottom': '15px'}
        ),
        html.Div(id='second-gene-settings', children=[
            html.Label("Select the second gene:", style={'font-weight': 'bold'}),
            dcc.Dropdown(
                id='gene-dropdown-2',
                options=[{'label': gene, 'value': gene} for gene in genes],
                style={'margin-bottom': '15px'}
            ),
            html.Div([
                html.Label("Top 20 correlated genes:", style={'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='correlated-genes-dropdown-2',
                    options=[],
                    disabled=False,  # Allow interaction
                    style={'margin-bottom': '15px'}
                )
            ]),

            html.Div(  # Histogram for second gene
                id='threshold-helper-histogram-2',
                style={'margin-top': '10px', 'margin-bottom': '20px'}
            ),
            html.Label("Choose a color for the second gene:", style={'font-weight': 'bold'}),
            dcc.Dropdown(
                id='color-dropdown-2',
                options=[{'label': color, 'value': color} for color in color_options.keys()],
                value='Yellow',  # Default value
                style={'margin-bottom': '15px'}
            ),
            html.Label("Set thresholds for visualizing the second gene:", style={'font-weight': 'bold'}),
            html.Div([
                dcc.Input(id='threshold-min-2', type='number', value=0, min=0, max=1, step=0.01,
                          style={'width': '48%', 'margin-right': '5px'}),
                dcc.Input(id='threshold-max-2', type='number', value=1, min=0, max=1, step=0.01,
                          style={'width': '48%'})
            ], style={'display': 'flex', 'margin-bottom': '15px'})
        ], style={'display': 'none'})

    ], style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top'}),

    # Third gene settings
    html.Div([
        html.Label("Enable third gene visualization:", style={'font-weight': 'bold'}),
        dcc.Checklist(
            id='third-gene-checkbox',
            options=[{'label': '', 'value': 'enable'}],
            value=[],  # Default unchecked
            style={'margin-bottom': '15px'}
        ),
        html.Div(id='third-gene-settings', children=[
            html.Label("Select the third gene:", style={'font-weight': 'bold'}),
            dcc.Dropdown(
                id='gene-dropdown-3',
                options=[{'label': gene, 'value': gene} for gene in genes],
                style={'margin-bottom': '15px'}
            ),
            html.Div([
                html.Label("Top 20 correlated genes:", style={'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='correlated-genes-dropdown-3',
                    options=[],
                    disabled=False,  # Allow interaction
                    style={'margin-bottom': '15px'}
                )
            ]),

            html.Div(  # Histogram for third gene
                id='threshold-helper-histogram-3',
                style={'margin-top': '10px', 'margin-bottom': '20px'}
            ),
            html.Label("Choose a color for the third gene:", style={'font-weight': 'bold'}),
            dcc.Dropdown(
                id='color-dropdown-3',
                options=[{'label': color, 'value': color} for color in color_options.keys()],
                value='Blue',  # Default value
                style={'margin-bottom': '15px'}
            ),
            html.Label("Set thresholds for visualizing the third gene:", style={'font-weight': 'bold'}),
            html.Div([
                dcc.Input(id='threshold-min-3', type='number', value=0, min=0, max=1, step=0.01,
                          style={'width': '48%', 'margin-right': '5px'}),
                dcc.Input(id='threshold-max-3', type='number', value=1, min=0, max=1, step=0.01,
                          style={'width': '48%'})
            ], style={'display': 'flex', 'margin-bottom': '15px'})
        ], style={'display': 'none'})
    ], style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top'}),

    # Axis filtering
    html.Div([
        html.Label("Filter x-axis:", style={'font-weight': 'bold'}),
        dcc.RangeSlider(
            id='x-slider',
            min=coords['xcoord'].min(),
            max=coords['xcoord'].max(),
            value=[coords['xcoord'].min(), coords['xcoord'].max()]
        ),
        html.Label("Filter y-axis:", style={'font-weight': 'bold', 'margin-top': '15px'}),
        dcc.RangeSlider(
            id='y-slider',
            min=coords['ycoord'].min(),
            max=coords['ycoord'].max(),
            value=[coords['ycoord'].min(), coords['ycoord'].max()]
        ),
        html.Label("Filter z-axis:", style={'font-weight': 'bold', 'margin-top': '15px'}),
        dcc.RangeSlider(
            id='z-slider',
            min=coords['zcoord'].min(),
            max=coords['zcoord'].max(),
            value=[coords['zcoord'].min(), coords['zcoord'].max()]
        ),
        html.Button("Refresh Scatter Plot", id='refresh-button', style={'margin-top': '15px', 'margin-bottom': '15px'}),
        html.Button("Download Displayed Data", id='download-button', style={'margin-top': '15px'}),
        dcc.Download(id="download-dataframe-csv")
    ], style={'width': '90%', 'margin': 'auto', 'padding': '20px'}),
    # Color filtering section
    html.Div([
        html.Label("Filter by Colors:", style={'font-weight': 'bold'}),
        html.Div(id='color-selection-div')  # Dynamically populated checkboxes
    ], style={'width': '90%', 'margin': 'auto', 'padding': '20px', 'margin-top': '30px'}),
    dcc.Store(id='camera-state', data=None),  # To store camera state
        html.Div([
            html.Label("Set View:", style={'font-weight': 'bold'}),
            html.Div([
                html.Button("X", id="view-x", style={'margin-right': '5px'}),
                html.Button("-X", id="view-neg-x", style={'margin-right': '5px'}),
                html.Button("Y", id="view-y", style={'margin-right': '5px'}),
                html.Button("-Y", id="view-neg-y", style={'margin-right': '5px'}),
                html.Button("Z", id="view-z", style={'margin-right': '5px'}),
                html.Button("-Z", id="view-neg-z")
            ], style={'margin-bottom': '20px'})
        ], style={'text-align': 'center'}),
    dcc.Graph(id='3d-scatter', style={'height': '600px'})
])


@app.callback(
    Output('threshold-helper-histogram', 'children'),
    [Input('gene-dropdown-1', 'value'),
     Input('color-dropdown-1', 'value')]
)
def update_histogram_image(selected_gene, selected_color):
    if selected_gene is None:
        return dash.no_update

    # Get gene expression values
    expression_values = df[selected_gene].dropna().to_numpy()

    # Calculate histogram with 100 bins
    bins = np.linspace(expression_values.min(), expression_values.max(), 101)  # 100 bins
    hist, bin_edges = np.histogram(expression_values, bins=bins)

    # Get the RGB color tuple from the color options
    color_rgb = color_options[selected_color]
    # Convert RGB values to hexadecimal for Plotly
    color_hex = mcolors.to_hex(color_rgb)

    # Create bar plot data for histogram
    fig = go.Figure(
        data=[
            go.Bar(
                x=bin_edges[:-1],  # Left edges of bins
                y=hist,  # Counts of cells in each bin
                width=np.diff(bin_edges),  # Bin widths
                marker=dict(color=color_hex, opacity=0.8),
                name=f'{selected_gene} Expression Histogram'
            )
        ],
        layout=go.Layout(
            title=f"Expression Distribution of {selected_gene}",
            xaxis_title="Expression Value (binned)",
            yaxis_title="Number of Cells",
            bargap=0.1,  # Adjust gap between bars
            template="plotly_white"
        )
    )

    # Adjust aspect ratio
    fig.update_layout(height=400, width=600)

    # Render the figure to a static image
    image_bytes = BytesIO()
    pio.write_image(fig, image_bytes, format="png")
    image_base64 = base64.b64encode(image_bytes.getvalue()).decode()

    # Return the image in a format suitable for Dash
    return html.Img(src=f"data:image/png;base64,{image_base64}", style={"width": "100%", "height": "auto"})

@app.callback(
    Output('threshold-helper-histogram-2', 'children'),
    [Input('gene-dropdown-2', 'value'),
     Input('color-dropdown-2', 'value'),
     Input('second-gene-checkbox', 'value')]
)
def update_second_histogram(selected_gene, selected_color, checkbox_value):
    if not checkbox_value or selected_gene is None:
        return None  # Hide the histogram if the second gene is not enabled or selected

    # Get gene expression values
    expression_values = df[selected_gene].dropna().to_numpy()

    # Calculate histogram with 100 bins
    bins = np.linspace(expression_values.min(), expression_values.max(), 101)  # 100 bins
    hist, bin_edges = np.histogram(expression_values, bins=bins)

    # Get the RGB color tuple from the color options
    color_rgb = color_options[selected_color]
    # Convert RGB values to hexadecimal for Plotly
    color_hex = mcolors.to_hex(color_rgb)

    # Create bar plot data for histogram
    fig = go.Figure(
        data=[
            go.Bar(
                x=bin_edges[:-1],  # Left edges of bins
                y=hist,  # Counts of cells in each bin
                width=np.diff(bin_edges),  # Bin widths
                marker=dict(color=color_hex, opacity=0.8),
                name=f'{selected_gene} Expression Histogram'
            )
        ],
        layout=go.Layout(
            title=f"Expression Distribution of {selected_gene}",
            xaxis_title="Expression Value (binned)",
            yaxis_title="Number of Cells",
            bargap=0.1,  # Adjust gap between bars
            template="plotly_white"
        )
    )

    # Adjust aspect ratio
    fig.update_layout(height=400, width=600)

    # Render the figure to a static image
    image_bytes = BytesIO()
    pio.write_image(fig, image_bytes, format="png")
    image_base64 = base64.b64encode(image_bytes.getvalue()).decode()

    # Return the image in a format suitable for Dash
    return html.Img(src=f"data:image/png;base64,{image_base64}", style={"width": "100%", "height": "auto"})

# Callback to show/hide the second gene settings
@app.callback(
    Output('second-gene-settings', 'style'),
    Input('second-gene-checkbox', 'value')
)
def toggle_second_gene_settings(checkbox_value):
    return {'display': 'block'} if 'enable' in checkbox_value else {'display': 'none'}

# Callback to show/hide the third gene settings
@app.callback(
    Output('third-gene-settings', 'style'),
    Input('third-gene-checkbox', 'value')
)
def toggle_third_gene_settings(checkbox_value):
    return {'display': 'block'} if 'enable' in checkbox_value else {'display': 'none'}

@app.callback(
    Output('correlated-genes-dropdown', 'options'),
    Input('gene-dropdown-1', 'value')
)
def update_correlated_genes(selected_gene):
    if not selected_gene:
        return []


    # Retrieve correlation values
    correlations = gene_correlation_data.loc[selected_gene]

    # Get top correlated genes
    top_correlated = correlations.drop(selected_gene).nlargest(20)

    return [
        {'label': f"{gene} ({correlation:.3f})", 'value': gene}
        for gene, correlation in top_correlated.items()
    ]
@app.callback(
    Output('correlated-genes-dropdown-2', 'options'),
    Input('gene-dropdown-2', 'value'),
    Input('second-gene-checkbox', 'value')
)
def update_correlated_genes_2(selected_gene, enabled):
    if not selected_gene or 'enable' not in enabled:
        return []

    correlations = gene_correlation_data.loc[selected_gene]
    top_correlated = correlations.drop(selected_gene).nlargest(20)

    return [
        {'label': f"{gene} ({correlation:.3f})", 'value': gene}
        for gene, correlation in top_correlated.items()
    ]
@app.callback(
    Output('correlated-genes-dropdown-3', 'options'),
    Input('gene-dropdown-3', 'value'),
    Input('third-gene-checkbox', 'value')
)
def update_correlated_genes_3(selected_gene, enabled):
    if not selected_gene or 'enable' not in enabled:
        return []

    correlations = gene_correlation_data.loc[selected_gene]
    top_correlated = correlations.drop(selected_gene).nlargest(20)

    return [
        {'label': f"{gene} ({correlation:.3f})", 'value': gene}
        for gene, correlation in top_correlated.items()
    ]

@app.callback(
    Output('threshold-helper-histogram-3', 'children'),
    [Input('gene-dropdown-3', 'value'),
     Input('color-dropdown-3', 'value'),
     Input('third-gene-checkbox', 'value')]
)
def update_third_histogram(selected_gene, selected_color, checkbox_value):
    if not checkbox_value or selected_gene is None:
        return None  # Hide the histogram if the third gene is not enabled or selected

    # Get gene expression values
    expression_values = df[selected_gene].dropna().to_numpy()

    # Calculate histogram with 100 bins
    bins = np.linspace(expression_values.min(), expression_values.max(), 101)  # 100 bins
    hist, bin_edges = np.histogram(expression_values, bins=bins)

    # Get the RGB color tuple from the color options
    color_rgb = color_options[selected_color]
    # Convert RGB values to hexadecimal for Plotly
    color_hex = mcolors.to_hex(color_rgb)

    # Create bar plot data for histogram
    fig = go.Figure(
        data=[
            go.Bar(
                x=bin_edges[:-1],  # Left edges of bins
                y=hist,  # Counts of cells in each bin
                width=np.diff(bin_edges),  # Bin widths
                marker=dict(color=color_hex, opacity=0.8),
                name=f'{selected_gene} Expression Histogram'
            )
        ],
        layout=go.Layout(
            title=f"Expression Distribution of {selected_gene}",
            xaxis_title="Expression Value (binned)",
            yaxis_title="Number of Cells",
            bargap=0.1,  # Adjust gap between bars
            template="plotly_white"
        )
    )

    # Adjust aspect ratio
    fig.update_layout(height=400, width=600)

    # Render the figure to a static image
    image_bytes = BytesIO()
    pio.write_image(fig, image_bytes, format="png")
    image_base64 = base64.b64encode(image_bytes.getvalue()).decode()

    # Return the image in a format suitable for Dash
    return html.Img(src=f"data:image/png;base64,{image_base64}", style={"width": "100%", "height": "auto"})


def generate_color_swatch(hex_color):
    """Generate a small color swatch as a base64-encoded image."""
    size = (20, 20)  # Size of the swatch
    # Convert the color from [0, 1] to [0, 255]
    rgb_color = tuple(int(c * 255) for c in hex_color)
    image = Image.new("RGB", size, rgb_color)
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

@app.callback(
    Output('color-selection-div', 'children'),
    [Input('refresh-button', 'n_clicks')],
    [State('gene-dropdown-1', 'value'),
     State('color-dropdown-1', 'value'),
     State('threshold-min-1', 'value'),
     State('threshold-max-1', 'value'),
     State('second-gene-checkbox', 'value'),
     State('gene-dropdown-2', 'value'),
     State('color-dropdown-2', 'value'),
     State('threshold-min-2', 'value'),
     State('threshold-max-2', 'value'),
     State('third-gene-checkbox', 'value'),
     State('gene-dropdown-3', 'value'),
     State('color-dropdown-3', 'value'),
     State('threshold-min-3', 'value'),
     State('threshold-max-3', 'value')]
)
def update_color_checkboxes(refresh_clicks, selected_gene1, color1, threshold_min1, threshold_max1,
                            second_gene_enabled, selected_gene2, color2, threshold_min2, threshold_max2,
                            third_gene_enabled, selected_gene3, color3, threshold_min3, threshold_max3):
    if refresh_clicks is None:
        raise dash.exceptions.PreventUpdate

    # Normalize gene values
    def normalize_within_threshold(values, min_threshold, max_threshold):
        norm_values = (values - min_threshold) / max(max_threshold - min_threshold, 1e-10)
        return np.clip(norm_values, 0, 1)

    norm_values1 = normalize_within_threshold(df[selected_gene1].to_numpy(), threshold_min1, threshold_max1)
    norm_values2 = normalize_within_threshold(df[selected_gene2].to_numpy(), threshold_min2, threshold_max2) if 'enable' in second_gene_enabled else np.zeros_like(norm_values1)
    norm_values3 = normalize_within_threshold(df[selected_gene3].to_numpy(), threshold_min3, threshold_max3) if 'enable' in third_gene_enabled else np.zeros_like(norm_values1)

    total_expression = norm_values1 + norm_values2 + norm_values3
    total_expression = np.clip(total_expression, 1e-5, None)  # Prevent division by zero
    weights1 = norm_values1 / total_expression
    weights2 = norm_values2 / total_expression
    weights3 = norm_values3 / total_expression

    color_rgb1 = np.array(color_options[color1])
    color_rgb2 = np.array(color_options[color2]) if 'enable' in second_gene_enabled else np.array([0, 0, 0])
    color_rgb3 = np.array(color_options[color3]) if 'enable' in third_gene_enabled else np.array([0, 0, 0])

    # Blend colors
    blended_colors = (
        weights1[:, None] * color_rgb1 +
        weights2[:, None] * color_rgb2 +
        weights3[:, None] * color_rgb3
    )
    blended_colors = np.clip(blended_colors, 0, 1)

    # K-Means clustering
    kmeans = KMeans(n_clusters=8, random_state=42)
    clustered_colors = kmeans.fit_predict(blended_colors)
    dominant_colors = kmeans.cluster_centers_

    # Ensure all values in dominant_colors are within [0, 1]
    dominant_colors = np.clip(dominant_colors, 0, 1)

    # Map clusters to colors
    cluster_color_mapping = {i: mcolors.to_hex(dominant_colors[i]) for i in range(len(dominant_colors))}

    # Generate checkboxes with color swatches
    cluster_counts = np.bincount(clustered_colors)
    sorted_clusters = np.argsort(-cluster_counts)
    sorted_counts = cluster_counts[sorted_clusters]
    sorted_colors = [cluster_color_mapping[cluster] for cluster in sorted_clusters]

    checkboxes = [
        html.Div([
            html.Div(
                style={'display': 'flex', 'align-items': 'center'},
                children=[
                    dcc.Checklist(
                        options=[{'label': f' {color} (Count: {count})', 'value': color}],
                        value=[color],
                        id={'type': 'color-checkbox', 'index': i},
                        inline=True,
                        style={'margin-right': '10px'}
                    ),
                    html.Img(
                        src=f"data:image/png;base64,{generate_color_swatch(mcolors.hex2color(color))}",
                        style={'height': '20px', 'width': '20px'}
                    )
                ]
            )
        ]) for i, (color, count) in enumerate(zip(sorted_colors, sorted_counts))
    ]

    return checkboxes

@app.callback(
    [Output('3d-scatter', 'figure'),
     Output('download-dataframe-csv', 'data')],
    [Input('refresh-button', 'n_clicks'),
     Input('download-button', 'n_clicks'),
     Input({'type': 'color-checkbox', 'index': dash.ALL}, 'value')],
    [State('gene-dropdown-1', 'value'),
     State('color-dropdown-1', 'value'),
     State('threshold-min-1', 'value'),
     State('threshold-max-1', 'value'),
     State('x-slider', 'value'),
     State('y-slider', 'value'),
     State('z-slider', 'value'),
     State('second-gene-checkbox', 'value'),
     State('gene-dropdown-2', 'value'),
     State('color-dropdown-2', 'value'),
     State('threshold-min-2', 'value'),
     State('threshold-max-2', 'value'),
     State('third-gene-checkbox', 'value'),
     State('gene-dropdown-3', 'value'),
     State('color-dropdown-3', 'value'),
     State('threshold-min-3', 'value'),
     State('threshold-max-3', 'value')]
)
def update_3d_scatter_and_download(
        refresh_clicks, download_clicks, selected_colors, selected_gene1, color1, threshold_min1, threshold_max1,
        x_range, y_range, z_range,
        second_gene_enabled, selected_gene2, color2, threshold_min2, threshold_max2,
        third_gene_enabled, selected_gene3, color3, threshold_min3, threshold_max3):
    if refresh_clicks is None:
        raise dash.exceptions.PreventUpdate

    # Filter DataFrame based on axis ranges
    filtered_df = df[
        (df['xcoord'].between(x_range[0], x_range[1])) &
        (df['ycoord'].between(y_range[0], y_range[1])) &
        (df['zcoord'].between(z_range[0], z_range[1]))
    ].copy()


    if filtered_df.empty:
        return {
            'data': [],
            'layout': go.Layout(title="No Data to Display")
        }, None

    # Normalize gene values within thresholds
    def normalize_within_threshold(values, min_threshold, max_threshold):
        norm_values = (values - min_threshold) / max(max_threshold - min_threshold, 1e-10)
        return np.clip(norm_values, 0, 1)

    norm_values1 = normalize_within_threshold(filtered_df[selected_gene1].to_numpy(), threshold_min1, threshold_max1)
    norm_values2 = normalize_within_threshold(filtered_df[selected_gene2].to_numpy(), threshold_min2, threshold_max2) if 'enable' in second_gene_enabled else np.zeros_like(norm_values1)
    norm_values3 = normalize_within_threshold(filtered_df[selected_gene3].to_numpy(), threshold_min3, threshold_max3) if 'enable' in third_gene_enabled else np.zeros_like(norm_values1)

    total_expression = norm_values1 + norm_values2 + norm_values3
    total_expression = np.clip(total_expression, 1e-10, None)  # Avoid divide-by-zero issues

    weights1 = norm_values1 / total_expression
    weights2 = norm_values2 / total_expression
    weights3 = norm_values3 / total_expression


    color_rgb1 = np.array(color_options[color1])
    color_rgb2 = np.array(color_options[color2]) if 'enable' in second_gene_enabled else np.zeros_like(color_rgb1)
    color_rgb3 = np.array(color_options[color3]) if 'enable' in third_gene_enabled else np.zeros_like(color_rgb1)

    # Blend colors
    blended_colors = weights1[:, None] * color_rgb1 + weights2[:, None] * color_rgb2 + weights3[:, None] * color_rgb3
    blended_colors = np.clip(blended_colors, 0, 1)


    if len(blended_colors) == 0:
        return {
            'data': [],
            'layout': go.Layout(title="No Data to Display")
        }, None

    # K-Means clustering
    kmeans = KMeans(n_clusters=8, random_state=42)
    clustered_colors = kmeans.fit_predict(blended_colors)
    dominant_colors = kmeans.cluster_centers_

    # Ensure all values in dominant_colors are within [0, 1]
    dominant_colors = np.clip(dominant_colors, 0, 1)
    cluster_color_mapping = {i: mcolors.to_hex(dominant_colors[i]) for i in range(len(dominant_colors))}
    filtered_df['cluster_id'] = clustered_colors
    filtered_df['blended_colors'] = filtered_df['cluster_id'].map(cluster_color_mapping)

    # Apply selected colors filter
    if selected_colors:
        selected_colors_set = {color for checkbox in selected_colors for color in checkbox}
        filtered_df = filtered_df[filtered_df['blended_colors'].isin(selected_colors_set)]


    # Generate the 3D scatter plot
    trace = go.Scatter3d(
        x=filtered_df['xcoord'],
        y=filtered_df['ycoord'],
        z=filtered_df['zcoord'],
        mode='markers',
        marker=dict(size=5, color=filtered_df['blended_colors']),
        showlegend=False  # Remove from legend
    )

    # Add axis arrows with custom labels
    axis_arrows = [
        go.Scatter3d(
            x=[-1, -1], y=[-0.9, 1], z=[1, 1],
            mode='lines+text',
            line=dict(color='blue', width=4),
            text=['V', 'D'],
            textposition='top center',
            name="Dorso-Ventral Axis"  # Custom label
        ),
        go.Scatter3d(
            x=[-0.9, 1], y=[-1, -1], z=[1, 1],
            mode='lines+text',
            line=dict(color='green', width=4),
            text=['P', 'A'],
            textposition='top center',
            name="Antero-Posterior Axis"  # Custom label
        ),
        go.Scatter3d(
            x=[-1, -1], y=[-1, -1], z=[0, 0.9],
            mode='lines+text',
            line=dict(color='red', width=4),
            text=['M', 'L'],
            textposition='top center',
            name="Medio-Lateral Axis"  # Custom label
        )
    ]
    # Default camera configuration
    camera_config = dict(eye=dict(x=1.25, y=1.25, z=1.25))

    # Combine the traces and layout
    figure = {
        'data': [trace] + axis_arrows,
        'layout': go.Layout(
            scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z', camera=camera_config),
            margin=dict(l=0, r=0, b=0, t=0),
            legend=dict(itemsizing='constant')  # Ensure the legend is properly aligned
        )
    }

    # Handle download functionality
    if download_clicks and ctx.triggered and 'download-button' in ctx.triggered[0]['prop_id']:
        return figure, dcc.send_data_frame(filtered_df.to_csv, "filtered_data.csv")

    return figure, None

@app.callback(
    Output('3d-scatter', 'figure', allow_duplicate=True),
    [Input('view-x', 'n_clicks'),
     Input('view-neg-x', 'n_clicks'),
     Input('view-y', 'n_clicks'),
     Input('view-neg-y', 'n_clicks'),
     Input('view-z', 'n_clicks'),
     Input('view-neg-z', 'n_clicks')],
    State('3d-scatter', 'figure'),  # Use the current figure state
    prevent_initial_call=True  # Prevent initial callback execution
)
def update_camera(view_x, view_neg_x, view_y, view_neg_y, view_z, view_neg_z, current_figure):
    # Define camera views
    camera_views = {
        'view-x': dict(eye=dict(x=2, y=0, z=0)),
        'view-neg-x': dict(eye=dict(x=-2, y=0, z=0)),
        'view-y': dict(eye=dict(x=0, y=2, z=0)),
        'view-neg-y': dict(eye=dict(x=0, y=-2, z=0)),
        'view-z': dict(eye=dict(x=0, y=0, z=2), up=dict(x=0, y=-1, z=0)),
        'view-neg-z': dict(eye=dict(x=0, y=0, z=-2), up=dict(x=0, y=1, z=0))
    }

    # Identify which button was clicked
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    new_camera = camera_views.get(button_id, None)

    if not new_camera or not current_figure:
        raise dash.exceptions.PreventUpdate

    # Update the camera configuration in the current figure
    current_figure['layout']['scene']['camera'] = new_camera
    return current_figure



if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
