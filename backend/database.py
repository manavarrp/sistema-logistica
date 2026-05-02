from sqlmodel import create_engine, Session
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")
# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=True)