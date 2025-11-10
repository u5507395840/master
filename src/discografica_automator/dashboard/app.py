import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import requests
import logging
from datetime import datetime

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# URL de nuestra API de backend
API_URL = "http://localhost:8080/api/campaigns"

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Panel de Control de Campañas"

# --- Layout de la Aplicación ---
app.layout = html.Div(children=[
    html.H1(children='Panel de Control de Campañas Discográficas', style={'textAlign': 'center'}),

    # --- Sección de Creación de Campaña ---
    html.Div([
        html.H3("Crear Nueva Campaña"),
        dcc.Input(id='input-artist', type='text', placeholder='Nombre del Artista...', style={'marginRight':'10px'}),
        dcc.Input(id='input-track', type='text', placeholder='Nombre de la Pista...', style={'marginRight':'10px'}),
        html.Button('Crear Campaña', id='create-campaign-button', n_clicks=0),
        html.Div(id='create-campaign-output', style={'marginTop': '10px'})
    ], style={'textAlign': 'center', 'padding': '20px', 'border': '1px solid #444', 'borderRadius': '5px', 'marginBottom': '20px'}),

    # --- Sección de Visualización de Campañas ---
    html.H3("Campañas Activas"),
    html.Div(id='live-update-text', style={'textAlign': 'center', 'padding': '10px'}),
    dash_table.DataTable(
        id='campaign-table',
        columns=[
            {"name": "ID", "id": "id"},
            {"name": "Artista", "id": "artist"},
            {"name": "Pista", "id": "track"},
            {"name": "Estado", "id": "status"},
            {"name": "Creado", "id": "created_at"},
        ],
        style_cell={'textAlign': 'left'},
        style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
        style_data={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
    ),
    
    dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0)
])

# --- Callback para Actualizar la Tabla ---
@app.callback(
    [Output('campaign-table', 'data'), Output('live-update-text', 'children')],
    [Input('interval-component', 'n_intervals'), Input('create-campaign-button', 'n_clicks')]
)
def update_table(n_intervals, n_clicks):
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
        if not df.empty:
            df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M:%S')
        return df.to_dict('records'), f"Última actualización: {datetime.now().strftime('%H:%M:%S')}"
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al contactar la API: {e}")
        return [], "Error: No se pudo conectar con el backend."
    except Exception as e:
        logging.error(f"Error inesperado al procesar los datos: {e}")
        return [], "Error procesando los datos."

# --- Callback para Crear una Nueva Campaña ---
@app.callback(
    Output('create-campaign-output', 'children'),
    [Input('create-campaign-button', 'n_clicks')],
    [State('input-artist', 'value'), State('input-track', 'value')],
    prevent_initial_call=True
)
def create_campaign(n_clicks, artist, track):
    if not artist or not track:
        return html.Div("El artista y la pista son obligatorios.", style={'color': 'red'})
    
    try:
        payload = {'artist': artist, 'track': track, 'video_prompt': f'promotional video for the song {track} by {artist}'}
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        new_campaign = response.json()
        return html.Div(f"✅ Campaña '{new_campaign['id']}' creada y en cola para '{artist} - {track}'.", style={'color': 'green'})
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al crear la campaña: {e}")
        return html.Div(f"Error al crear la campaña: {e}", style={'color': 'red'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
