from supabase import create_client, Client
from dotenv import load_dotenv
import os
load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

def conectar_db(url, key):
    try:
        supabase: Client = create_client(url, key)
        print("Conexión exitosa a Supabase")
        return supabase
    except ConnectionError as e:
        print(f"Error al conectar a Supabase: {e}")
        return
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return