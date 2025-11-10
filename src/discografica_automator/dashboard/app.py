import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import requests
import logging

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# URL de nuestra API de backend
API_URL = "http://localhost:8080/api/campaigns"

app = dash.Dash(__name__)
app.title = "Panel de Control de Campañas"

# --- Layout de la Aplicación ---
app.layout = html.Div(children=[
    html.H1(children='Panel de Control de Campañas Discográficas', style={'textAlign': 'center'}),
    
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
        style_header={
            'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'white'
        },
        style_data={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        },
    ),
    
    # Componente para actualizar los datos periódicamente (cada 5 segundos)
    dcc.Interval(
        id='interval-component',
        interval=5*1000, # en milisegundos
        n_intervals=0
    )
])

# --- Callback para Actualizar la Tabla ---
@app.callback(
    [Output('campaign-table', 'data'), Output('live-update-text', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_table(n):
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Lanza un error si la petición falla
        data = response.json()
        df = pd.DataFrame(data)
        # Formatear fechas para una mejor lectura
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M:%S')
        return df.to_dict('records'), f"Última actualización: {pd.Timestamp.now().strftime('%H:%M:%S')}"
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al contactar la API: {e}")
        return [], "Error: No se pudo conectar con el backend. ¿Está el contenedor de la API en ejecución?"
    except Exception as e:
        logging.error(f"Error inesperado al procesar los datos: {e}")
        return [], "Error procesando los datos."

if __name__ == '__main__':
    # CORRECCIÓN: Usamos app.run() en lugar del obsoleto app.run_server()
    app.run(debug=True, host='0.0.0.0', port=8050)
