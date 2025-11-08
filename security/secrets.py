from dotenv import load_dotenv
import os

load_dotenv()

def get_env(key: str, default=None):
    return os.getenv(key, default)

# Ejemplo de uso: SECRET = get_env('SECRET_KEY')
