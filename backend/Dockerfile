FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema (opcional, por si se necesitan)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt y instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código (se sobrescribe con volumen en desarrollo)
COPY ./src ./src

# Comando por defecto para desarrollo (con recarga)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]