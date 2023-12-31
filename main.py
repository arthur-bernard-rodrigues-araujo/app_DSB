import dash
from dash import dcc, html, Input, Output, State
import pandas as pd

# Função para calcular o valor do imóvel (exemplo simples)
def calculate_property_value(neighborhood, distance_m, num_rooms, zone, property_type, area, data, data_gain):
    filtered_data = data[
        (data['District'] == neighborhood) &
        (data['Distance_to_station'] == distance_m) &
        (data['No_of_Bedrooms'] == num_rooms) &
        (data['London_zone'] == zone) &
        (data['House_Type'] == property_type)
    ]
    filtered_gain = data_gain[
        (data_gain['District'] == neighborhood)
        ]

    if filtered_data.empty:
        return 0, 0  # Retorna 0 se não encontrar nenhum elemento no filtro
    else:
        base_value = filtered_data['Predicted_value'].iloc[0]
        estimated_value = base_value * area
        expected_gain = filtered_gain['Percent_5_years'].iloc[0]*100
        return estimated_value, expected_gain

# Função para obter os valores únicos da coluna "London_zone" filtrados pelo bairro selecionado
def get_unique_values_sorted(neighborhood, column):
    if neighborhood is not None:
        filtered_df = df[df['District'] == neighborhood]
        unique_values = filtered_df[column].unique()
        sorted_unique_values = sorted(unique_values)  # Ordenar os valores alfabeticamente
        return [{"label": value, "value": value} for value in sorted_unique_values]

    return []

# Importar o banco de dados
url = 'https://github.com/arthur-bernard-rodrigues-araujo/app_DSB/raw/main/LondonHousingData.xlsx'
df = pd.read_excel(url, sheet_name='Planilha3')
df_gain = pd.read_excel(url, sheet_name='Planilha2')

# Obter os valores únicos das colunas do BD em ordem alfabética ou crescente
district_values = sorted(df['District'].unique())
house_type_values = sorted(df['House_Type'].unique())
zone_values = sorted(df['London_zone'].unique())
distance_values = sorted(df['Distance_to_station'].unique())
#area_values = sorted(df['Area_in_sq_ft'].unique())

# Inicialização da aplicação
app = dash.Dash(__name__, title="ValueVision - T1")
server = app.server

# Layout da aplicação
app.layout = html.Div(
    style={"font-family": "Arial", "text-align": "center"},
    children=[
        html.Div(
            style={
                "width": "100vw",  # 100% da largura da janela
                "aspect-ratio": "1920/138",  # Proporções da imagem (largura/altura)
                "background-image": "url(https://github.com/arthur-bernard-rodrigues-araujo/app_DSB/raw/main/Header_2.png)",
                "background-size": "cover",
                "background-position": "center",
            }
        ),
        # Grid com 7 colunas
        html.Div(
            style={"display": "grid", "grid-template-columns": "repeat(7, 1fr)", "grid-gap": "10px", "padding": "10px"},
            children=[
                # Labels e Componentes
                html.Div(
                    children=[
                        html.Label("Neighborhood:", style={"font-weight": "bold", "font-size": "14px"}),
                        dcc.Dropdown(
                            id="neighborhood-dropdown",
                            options=[{"label": district, "value": district} for district in district_values],
                            value=district_values[-6] if district_values else None,
                            style={"font-size": "12px"},
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Label("Property Area (ft²): ", style={"font-weight": "bold", "font-size": "14px"}),
                        #dcc.Dropdown(
                        #    id="property-area-dropdown",
                        #    options=[{"label": str(area), "value": area} for area in area_values],
                        #    value=783,
                        #),
                        dcc.Slider(
                            id="property-area-slider",
                            min=500,
                            max=5000,
                            value=700,
                            marks={i: str(i) for i in range(500, 5001, 1500)},
                            included=False,
                            updatemode="drag",
                            tooltip={"placement": "bottom"},
                            step=500,
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Label("Distance to station (m): ", style={"font-weight": "bold", "font-size": "12px"}),
                #        dcc.Dropdown(
                #            id="distance-dropdown",
                #            options=[{"label": str(distance), "value": distance} for distance in distance_values],
                #            value=100,
                #        ),
                        dcc.Slider(
                            id="distance-slider",
                            min=0,
                            max=3000,
                            value=700,
                            marks={i: str(i) for i in range(0, 3001, 1000)},
                            included=False,
                            updatemode="drag",
                            tooltip={"placement": "bottom"},
                            step=100,
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Label("# Rooms: ", style={"font-weight": "bold", "font-size": "14px"}),
                        dcc.Slider(
                            id="rooms-slider",
                            min=1,
                            max=8,
                            value=3,
                            marks={i: str(i) for i in range(1, 9)},
                            included=False,
                            updatemode="drag",
                            tooltip={"placement": "bottom"},
                            step=1,
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Label("Zone:", style={"font-weight": "bold", "font-size": "14px"}),
                        dcc.Dropdown(
                            id="zone-dropdown",
                            options=[{"label": zone, "value": zone} for zone in zone_values],
                            value=df[df['District'] == df['District'].unique()[0]]['London_zone'].unique()[0],
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Label("Property Type:", style={"font-weight": "bold", "font-size": "14px"}),
                        dcc.Dropdown(
                            id="property-type-dropdown",
                            options=[{"label": house_type, "value": house_type} for house_type in house_type_values],
                            value=df[df['District'] == df['District'].unique()[0]]['House_Type'].unique()[0],
                            style={"font-size": "12px"},
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Button("Calculate", id="calculate-button", style={"width": "100%", "padding": "17px"}),
                    ],
                ),
            ],
        ),
        html.Div(
            style={"display": "flex", "padding": "10px"},
            children=[
                html.Div(
                    style={"flex": 1, "text-align": "center"},
                    children=[
                        html.Label("Estimated current value: ", style={"font-weight": "bold"}),
                        html.Label(id="property-value-output"),
                    ],
                ),
                html.Div(
                    style={"flex": 1, "text-align": "center"},
                    children=[
                        html.Label("Expected gain after 5 years: ", style={"font-weight": "bold"}),
                        html.Label(id="future-value-output"),
                    ],
                ),
            ],
        ),
        html.Div(
            style={
                "width": "100vw",
                "aspect-ratio": "1280/517",
                "background-image": "url(https://github.com/arthur-bernard-rodrigues-araujo/app_DSB/raw/main/conteudo.png)",
                "background-size": "cover",
                "background-position": "center"
            },
        ),
    ]
)

# Callback para calcular e exibir o valor do imóvel
@app.callback(
    [Output("property-value-output", "children"),
     Output("future-value-output", "children")],
    Input("calculate-button", "n_clicks"),
    State("neighborhood-dropdown", "value"),
    State("distance-slider", "value"),
    State("rooms-slider", "value"),
    State("zone-dropdown", "value"),
    State("property-type-dropdown", "value"),
    State("property-area-slider", "value"),
)

def calculate_final_values(n_clicks, neighborhood, distance_m, num_rooms, zone, property_type, area):
    if n_clicks is not None:
        property_value, expected_gain = calculate_property_value(neighborhood, distance_m, num_rooms, zone, property_type, area, df, df_gain)

        # Cálculo da faixa de valores (5% acima e abaixo do property_value)
        #lower_bound_value = property_value * 0.95
        #upper_bound_value = property_value * 1.05
        #lower_bound_gain = expected_gain - 10
        #upper_bound_gain = expected_gain + 10

        # Formatação do property_value como uma faixa de valores
        if property_value > 100000:
            formatted_property_value = "£{:.3f}M".format(property_value / 1000000)
        else:
            formatted_property_value = "£{:,}".format(property_value)

        # Formatação do future_value permanece inalterada
        formatted_expected_gain = "{:,.1f}%".format(expected_gain)

        return formatted_property_value, formatted_expected_gain

    return "", ""

# Callback para atualizar os valores do zone-dropdown e property-type-dropdown de acordo com o bairro selecionado
@app.callback(
    [Output("zone-dropdown", "options"),
     Output("property-type-dropdown", "options"),
     #Output("distance-dropdown", "options"),
     #Output("property-area-dropdown", "options"),
     ],
    Input("neighborhood-dropdown", "value"),
)
def update_dropdown_options(neighborhood):
    zone_options = get_unique_values_sorted(neighborhood, "London_zone")
    property_type_options = get_unique_values_sorted(neighborhood, "House_Type")
    #property_area_options = get_unique_values_sorted(neighborhood, "Area_in_sq_ft")
    #distance_options = get_unique_values_sorted(neighborhood, "Distance_to_station")

    return zone_options, property_type_options#, distance_options, property_area_options

# Execução do servidor local
if __name__ == "__main__":
    app.run_server(debug=True)
