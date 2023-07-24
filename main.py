
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

url = 'https://github.com/arthur-bernard-rodrigues-araujo/app_DSB/raw/main/LondonHousingData.xlsx'

app = dash.Dash(__name__)
server = app.server

# List of London neighborhoods in alphabetical order
london_neighborhoods = [
    'Barking & Dagenham',
    'Barnet',
    'Bexley',
    'Brent',
    'Bromley',
    'Camden',
    'City of London',
    'Croydon',
    'Ealing',
    'Enfield',
    'Greenwich',
    'Hackney',
    'Hammersmith & Fulham',
    'Haringey',
    'Harrow',
    'Havering',
    'Hillingdon',
    'Hounslow',
    'Islington',
    'Kensington & Chelsea',
    'Kingston upon Thames',
    'Lambeth',
    'Lewisham',
    'Merton',
    'Newham',
    'Redbridge',
    'Richmond upon Thames',
    'Southwark',
    'Sutton',
    'Tower Hamlets',
    'Waltham Forest',
    'Wandsworth',
    'Westminster'
]

# App layout with custom style
app.layout = html.Div(
    style={
        'textAlign': 'center',
        'background': '#ffffff',
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
                            "Property Area (m²):",
                            style={'fontSize': '18px', 'fontFamily': 'Arial', 'fontWeight': 'bold'},
                        ),
                        dcc.Input(
                            id='area-input',
                            type='number',
                            placeholder='Property Area (m²)',
                            value=1455,
                            style={'width': '100%', 'height': '50px', 'marginBottom': '10px', 'fontSize': '16px', 'fontFamily': 'Arial', 'textAlign': 'center'},
                        ),
                        html.Label(
                            "Distance to Tube (m):",
                            style={'fontSize': '18px', 'fontFamily': 'Arial', 'fontWeight': 'bold'}
                        ),
                        dcc.Input(
                            id='distance-input',
                            type='number',
                            placeholder='Distance to Tube (m)',
                            value=949,
                            style={'width': '100%', 'height': '50px', 'marginBottom': '10px', 'fontSize': '16px', 'fontFamily': 'Arial', 'textAlign': 'center'},
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
