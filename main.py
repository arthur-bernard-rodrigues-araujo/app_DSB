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
        'background': '#ffffff',  # Background branco
        'height': '100vh',
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
        'fontFamily': 'Arial',  # Fonte Arial
    },
    children=[
        html.H1("London Housing Prices Calculator", style={'marginBottom': '20px', 'fontSize': '36px', 'fontFamily': 'Arial'}),
        html.Label("Select a neighborhood:", style={'fontSize': '18px', 'fontFamily': 'Arial'}),
        dcc.Dropdown(
            id='neighborhood-dropdown',
            options=[{'label': neighborhood, 'value': neighborhood} for neighborhood in london_neighborhoods],
            value=london_neighborhoods[0],
            style={'width': '300px', 'height': '50px', 'marginBottom': '10px', 'fontSize': '16px', 'fontFamily': 'Arial'},
        ),
        html.Label("Property Area (m²):", style={'fontSize': '18px', 'fontFamily': 'Arial'}),
        dcc.Input(id='area-input', type='number', placeholder='Property Area (m²)', value=1455, style={'width': '300px', 'height': '50px', 'marginBottom': '10px', 'fontSize': '16px', 'fontFamily': 'Arial', 'textAlign': 'center'}),
        html.Label("Distance to Tube (m):", style={'fontSize': '18px', 'fontFamily': 'Arial'}),
        dcc.Input(id='distance-input', type='number', placeholder='Distance to Tube (m)', value=949, style={'width': '300px', 'height': '50px', 'marginBottom': '10px', 'fontSize': '16px', 'fontFamily': 'Arial', 'textAlign': 'center'}),
        html.Label("Number of Bathrooms:", style={'fontSize': '18px', 'fontFamily': 'Arial'}),
        dcc.Input(id='bathrooms-input', type='number', placeholder='Number of Bathrooms', value=1, style={'width': '300px', 'height': '50px', 'marginBottom': '30px', 'fontSize': '16px', 'fontFamily': 'Arial', 'textAlign': 'center'}),
        html.Button('Calculate Price', id='button', n_clicks=0, style={'textAlign': 'center', 'width': '300px', 'height': '50px', 'fontSize': '18px', 'fontFamily': 'Arial'}),
        html.Div(id='output', style={'marginTop': '30px', 'fontSize': '20px', 'fontFamily': 'Arial'})
    ]
)

# Callback function to update the output div
@app.callback(
    Output('output', 'children'),
    [Input('button', 'n_clicks')],
    [dash.dependencies.State('neighborhood-dropdown', 'value'),
     dash.dependencies.State('area-input', 'value'),
     dash.dependencies.State('distance-input', 'value'),
     dash.dependencies.State('bathrooms-input', 'value')]
)
def update_output(n_clicks, neighborhood, area, distance, bathrooms):
    if n_clicks > 0:
        if neighborhood is None or area is None or distance is None or bathrooms is None:
            return "Please fill in all fields."
        else:
            # Convert area and distance to meters if needed (assuming they are initially provided in meters)
            area_m2 = int(area) if int(area) > 0 else 0
            distance_m = int(distance) if int(distance) > 0 else 0
            bathrooms = int(bathrooms) if int(bathrooms) > 0 else 0

            data = pd.read_excel(url, engine='openpyxl')
            # Filter the data based on the selected neighborhood, area, distance, and bathrooms
            filtered_data = data[(data['neighborhood'] == neighborhood) & (data['area'] == area_m2) & (
                        data['distance'] == distance_m) & (data['bathrooms'] == bathrooms)]

            if filtered_data.empty:
                return "No data available for the selected criteria."
            else:
                # Get the estimated price for the selected combination
                estimated_price = filtered_data['estimated_price'].values[0]

                # Format the estimated price as a monetary value (pounds)
                formatted_price = f'£{estimated_price:,.2f}'  # Adiciona o símbolo de libra esterlina e vírgula de milhar

                return f"The estimated price for {neighborhood} is: {formatted_price}"

if __name__ == '__main__':
    app.run_server(debug=True)
