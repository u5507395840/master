"""
Script de utilidad para realizar la autenticación inicial con la API de YouTube.
"""
from discografica_automator.integrations import youtube_uploader

if __name__ == '__main__':
    print("Ejecutando script de autenticación de YouTube...")
    print("Se abrirá una ventana en tu navegador para que autorices la aplicación.")
    youtube_uploader.get_authenticated_service()
    print("¡Autenticación completada! El archivo 'token.json' ha sido creado/actualizado.")
