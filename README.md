# 🚚 Sistema de Gestión Logística

Bienvenido al **Sistema de Gestión Logística**, una solución integral diseñada para optimizar y controlar el flujo de mercancías a través de transportes terrestres y marítimos. Esta aplicación permite a los clientes gestionar sus propios envíos, calcular costos con descuentos dinámicos y realizar un seguimiento en tiempo real del estado de sus productos.

### 🌟 Características Principales
- **Logística Terrestre**: Gestión de envíos a bodegas con validación de placas vehiculares.
- **Logística Marítima**: Gestión de envíos a puertos internacionales con control de números de flota.
- **Seguridad y Privacidad**: Autenticación mediante JWT, asegurando que cada cliente solo tenga acceso a su propia información.
- **Cálculo Automático**: Aplicación de descuentos por volumen (5% en terrestre y 3% en marítimo para más de 10 unidades).
- **Interfaz Moderna**: Dashboard dinámico construido con React y Shadcn UI.

---

## 🛠️ Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:
1. **Visual Studio Code** (o tu editor de preferencia).
2. **Docker Desktop** (esencial para levantar los servicios).
3. **Git** (para clonar el repositorio).

---

## 🚀 Guía de Instalación y Ejecución

Sigue estos pasos para poner en marcha el proyecto en menos de 5 minutos:

### 1. Clonar el repositorio
Abre una terminal y ejecuta:
```bash
git clone <url-del-repositorio>
cd logisitca-envios
```

### 2. Configurar variables de entorno
Crea un archivo llamado `.env` en la raíz del proyecto (donde está el `docker-compose.yml`). Puedes copiar el contenido de `.env.example`:

```bash
# Configuración Postgres
POSTGRES_DB=logistica_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=admin

# Configuración Backend
SECRET_KEY=tu_clave_secreta_super_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 3. Levantar el sistema con Docker
El proyecto está totalmente contenedorizado. Ejecuta el siguiente comando para construir e iniciar todos los servicios:

```bash
docker compose up -d --build
```

### 4. Cargar el esquema de Base de Datos (Manual)
Si es la primera vez que ejecutas el proyecto o si los datos de prueba no se cargaron automáticamente, ejecuta el siguiente comando en **PowerShell** desde la raíz del proyecto:

```powershell
Get-Content .\schema.sql | docker exec -i logistica_bd psql -U postgres -d logistica_db
```

---

## 🔗 Rutas de Acceso

Una vez que Docker termine de levantar los contenedores, podrás acceder a:

| Servicio | URL |
| :--- | :--- |
| **Frontend (Aplicación)** | [http://localhost:5174](http://localhost:5174) |
| **Backend (Documentación Swagger)** | [http://localhost:8001/docs](http://localhost:8001/docs) |

---

## 📝 Primeros Pasos

1. **Crear un Usuario**:
   - Ve al Frontend y haz clic en "Registrarse".
   - O usa el usuario de prueba ya creado en el sistema:
     - **Email**: `admin@logistica.com`
     - **Password**: `Admin123!`

2. **Gestionar Envíos**:
   - Una vez logueado, verás tu panel de control vacío (o con tus datos previos).
   - Haz clic en **"Nuevo Envío"**.
   - El sistema detectará automáticamente si el producto es Terrestre o Marítimo según tu selección y ajustará el formulario.
   - **Formatos Requeridos**:
     - Placa Vehículo: `AAA000` (3 letras y 3 números).
     - Número Flota: `AAA0000A` (3 letras, 4 números y 1 letra).

---

## ⚠️ Notas Importantes de Desarrollo

### Advertencias de Importación en el Editor (IDE)
Es posible que al abrir el proyecto en VS Code veas errores o advertencias en los `imports` (subrayados en rojo). 
- **Razón**: Las librerías de Python y Node.js están instaladas **dentro de los contenedores de Docker**, no necesariamente en tu máquina local.
- **Impacto**: Esto **NO afecta la ejecución** del proyecto. El sistema funcionará perfectamente al ejecutar `docker compose up`. 

---

## 🏗️ Stack Tecnológico
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Shadcn UI, Zustand.
- **Backend**: Python 3.11, FastAPI, SQLAlchemy.
- **Base de Datos**: PostgreSQL 15.
- **Infraestructura**: Docker & Docker Compose.

---
© 2026 - Sistema de Gestión Logística.