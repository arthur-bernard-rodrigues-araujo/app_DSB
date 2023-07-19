import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import locale

app = dash.Dash(__name__)

# List of London neighborhoods in alphabetical order
london_neighborhoods = [
    'Balham',
    'Barnes',
    'Battersea',
    'Belgravia',
    'Bermondsey',
    'Bethnal Green',
    'Blackheath',
    'Brixton',
    'Camden',
    'Canary Wharf',
    'Chiswick',
    'Clapham',
    'Covent Garden',
    'Dalston',
    'Deptford',
    'Ealing',
    'Earls Court',
    'Finsbury Park',
    'Fulham',
    'Greenwich',
    'Hackney',
    'Hammersmith',
    'Hampstead',
    'Highbury',
    'Highgate',
    'Holborn',
    'Hoxton',
    'Islington',
    'Kensington',
    'Kentish Town',
    'Kilburn',
    'Kings Cross',
    'Knightsbridge',
    'Lambeth',
    'London Bridge',
    'Maida Vale',
    'Marylebone',
    'Mayfair',
    'Mile End',
    'Notting Hill',
    'Paddington',
    'Peckham',
    'Primrose Hill',
    'Putney',
    'Richmond',
    'Shoreditch',
    'Soho',
    'South Bank',
    'St John’s Wood',
    'Stratford',
    'Streatham',
    'Tooting',
    'Vauxhall',
    'Wandsworth',
    'Westminster'
]

# Set the locale to the UK for formatting numbers as monetary values (pounds)
#locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')

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
        dcc.Input(id='area-input', type='number', placeholder='Property Area (m²)', value=50, style={'width': '300px', 'height': '50px', 'marginBottom': '10px', 'fontSize': '16px', 'fontFamily': 'Arial', 'textAlign': 'center'}),
        html.Label("Distance to Tube (m):", style={'fontSize': '18px', 'fontFamily': 'Arial'}),
        dcc.Input(id='distance-input', type='number', placeholder='Distance to Tube (m)', value=100, style={'width': '300px', 'height': '50px', 'marginBottom': '10px', 'fontSize': '16px', 'fontFamily': 'Arial', 'textAlign': 'center'}),
        html.Label("Number of Bathrooms:", style={'fontSize': '18px', 'fontFamily': 'Arial'}),
        dcc.Input(id='bathrooms-input', type='number', placeholder='Number of Bathrooms', value=1, style={'width': '300px', 'height': '50px', 'marginBottom': '30px', 'fontSize': '16px', 'fontFamily': 'Arial', 'textAlign': 'center'}),
        html.Button('Calculate Price', id='button', n_clicks=0, style={'textAlign': 'center', 'width': '300px', 'height': '50px', 'fontSize': '18px', 'fontFamily': 'Arial'}),
        html.Div(id='output', style={'marginTop': '30px', 'fontSize': '20px', 'fontFamily': 'Arial'})
    ]
)


# Média de preço por metro quadrado em Londres (em pounds)
average_price_per_sqm = 10

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

            # Calculate the estimated price based on the average price per square meter
            estimated_price = area_m2 * average_price_per_sqm

            # Add additional cost based on the distance to the tube and number of bathrooms
            estimated_price += distance_m * 5  # Assuming £5 per meter to the tube
            estimated_price += bathrooms * 10000  # Assuming £10,000 per bathroom

            # Format the estimated price as a monetary value (pounds)
            #formatted_price = locale.currency(estimated_price, grouping=True)

            return f"The estimated price for {neighborhood} is: {estimated_price}"

if __name__ == '__main__':
    app.run_server(debug=True)
