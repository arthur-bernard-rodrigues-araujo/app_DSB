import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

url = 'https://github.com/arthur-bernard-rodrigues-araujo/app_DSB/raw/main/LondonHousingData.xlsx'

app = dash.Dash(__name__)
server = app.server

# Function to get unique values for neighborhood, area and distance to the station from the Excel file
def get_unique_values(column_name):
    data = pd.read_excel(url, engine='openpyxl')
    return data[column_name].unique()

unique_areas = get_unique_values('area')
unique_distances = get_unique_values('distance')
london_neighborhoods = get_unique_values('neighborhood')

# Function to get the min and max values for area and distance to the station from the Excel file
def get_min_max_values():
    data = pd.read_excel(url, engine='openpyxl')
    min_area = data['area'].min()
    max_area = data['area'].max()
    min_distance = data['distance'].min()
    max_distance = data['distance'].max()
    return min_area, max_area, min_distance, max_distance

min_area, max_area, min_distance, max_distance = get_min_max_values()

# App layout with custom style
app.layout = html.Div(
    style={
        'textAlign': 'center',
        'backgroundImage': 'url(https://github.com/arthur-bernard-rodrigues-araujo/app_DSB/raw/main/background.PNG)',
        'backgroundRepeat': 'no-repeat',
        'backgroundSize': 'cover',
        'backgroundPosition': 'center',
        'height': '100vh',
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'fontFamily': 'Arial',
    },
    children=[
        html.H1(
            "London Housing Prices Calculator",
            style={'marginTop': '20px', 'marginBottom': '20px', 'fontSize': '36px', 'fontFamily': 'Arial'}
        ),
        html.Div(
            style={'display': 'flex', 'flexDirection': 'row', 'width': '80%'},
            children=[
                html.Div(
                    style={'flex': '1', 'padding': '20px'},
                    children=[
                        html.Label(
                            "Select a neighborhood:",
                            style={'fontSize': '18px', 'fontFamily': 'Arial', 'fontWeight': 'bold'}
                        ),
                        dcc.Dropdown(
                            id='neighborhood-dropdown',
                            options=[{'label': neighborhood, 'value': neighborhood} for neighborhood in london_neighborhoods],
                            value=london_neighborhoods[0],
                            style={'width': '100%', 'height': '50px', 'marginBottom': '10px', 'fontSize': '16px', 'fontFamily': 'Arial'},
                        ),
                        html.Label(
                            id='area-label',  # Add an ID to the label to update its text
                            style={'fontSize': '18px', 'fontFamily': 'Arial', 'fontWeight': 'bold'},
                        ),
                        dcc.Slider(
                            id='area-input',
                            min=min_area,
                            max=max_area,
                            step=100,
                            value=min_area,
                            marks={i: str(i) for i in range(min_area, max_area, 1000)}
                        ),
                        html.Label(
                            id='distance-label',  # Add an ID to the label to update its text
                            style={'fontSize': '18px', 'fontFamily': 'Arial', 'fontWeight': 'bold'}
                        ),
                        dcc.Slider(
                            id='distance-input',
                            min=min_distance,
                            max=max_distance,
                            step=100,
                            value=min_distance,
                            marks={i: str(i) for i in range(min_distance, max_distance + 1, 100)}
                        ),
                        html.Label(
                            "Number of Bathrooms:",
                            style={'fontSize': '18px', 'fontFamily': 'Arial', 'fontWeight': 'bold'}
                        ),
                        dcc.Input(
                            id='bathrooms-input',
                            type='number',
                            placeholder='Number of Bathrooms',
                            value=1,
                            style={'width': '100%', 'height': '50px', 'marginBottom': '30px', 'fontSize': '16px', 'fontFamily': 'Arial', 'textAlign': 'center'},
                        ),
                        html.Button(
                            'Calculate Price',
                            id='button',
                            n_clicks=0,
                            style={'textAlign': 'center', 'width': '100%', 'height': '50px', 'fontSize': '18px', 'fontFamily': 'Arial'}
                        ),
                    ]
                ),
                html.Div(
                    style={'flex': '1', 'padding': '20px', 'fontSize': '20px', 'fontFamily': 'Arial', 'textAlign': 'center'},
                    children=[
                        html.Div(
                            style={'marginTop': '20px', 'fontWeight': 'bold'},
                            id='output-value-container'
                        ),
                        html.Div(
                            style={'marginTop': '30px', 'fontSize': '18px', 'fontFamily': 'Arial'},
                            id='price-container'
                        )
                    ]
                )
            ]
        ),
    ]
)
# Callback function to update the label text for the area slider
@app.callback(
    Output('area-label', 'children'),
    [Input('area-input', 'value')]
)
def update_area_label(value):
    return f"Property Area (m²): {value}"

# Callback function to update the label text for the distance slider
@app.callback(
    Output('distance-label', 'children'),
    [Input('distance-input', 'value')]
)
def update_distance_label(value):
    return f"Distance to Station (m): {value}"

# Callback function to update the output div
@app.callback(
    [Output('output-value-container', 'children'),
     Output('price-container', 'children')],
    [Input('button', 'n_clicks')],
    [dash.dependencies.State('neighborhood-dropdown', 'value'),
     dash.dependencies.State('area-input', 'value'),
     dash.dependencies.State('distance-input', 'value'),
     dash.dependencies.State('bathrooms-input', 'value')]
)
def update_output(n_clicks, neighborhood, area, distance, bathrooms):
    if neighborhood is not None:
        neighborhood_text = neighborhood
    else:
        neighborhood_text = ""

    if n_clicks > 0 and area is not None and distance is not None and bathrooms is not None:
        # Convert area and distance to meters if needed (assuming they are initially provided in meters)
        area_m2 = int(area) if int(area) > 0 else 0
        distance_m = int(distance) if int(distance) > 0 else 0
        bathrooms = int(bathrooms) if int(bathrooms) > 0 else 0

        data = pd.read_excel(url, engine='openpyxl')
        # Filter the data based on the selected neighborhood, area, distance, and bathrooms
        filtered_data = data[(data['neighborhood'] == neighborhood) & (data['area'] == area_m2) & (
                    data['distance'] == distance_m) & (data['bathrooms'] == bathrooms)]

        if filtered_data.empty:
            return "No data available for the selected criteria.", ""

        # Get the estimated price for the selected combination
        estimated_price = filtered_data['estimated_price'].values[0]

        # Calculate future price (estimated price * 2)
        future_price = estimated_price * 2

        # Format the estimated price and future price as monetary values (pounds)
        formatted_price = f'£{estimated_price:,.2f}'
        formatted_future_price = f'£{future_price:,.2f}'

        # Set the color based on the value
        color = 'red' if estimated_price > 1000000 else 'green'

        # Prepare the output text
        output_text = f"The estimated price for {neighborhood_text} is: {formatted_price}"

        # Combine both prices into a single text with different colors for estimated and future prices
        price_text = html.Div([
            "The estimated property price for the next 5 years is: ", html.Span(formatted_future_price, style={'color': color})
        ])

        return output_text, price_text
    else:
        return "Please fill in all fields.", ""

if __name__ == '__main__':
    app.run_server(debug=True)
