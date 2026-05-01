from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

# Inicializamos la aplicación FastAPI
app = FastAPI(
    title="Logística de Envíos API",
    description="API para gestionar la logística de envíos, incluyendo rutas, vehículos y entregas.",
    version="1.0.0"
)

# Endpoint raíz para verificar que la API está funcionando
@app.get("/")
def root():
    #return "Bienvenido a la API de Logística de Envíos!"
    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Bienvenido a la API de Logística de Envíos!"}
            )