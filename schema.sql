-- ============================================================
-- SISTEMA DE GESTIÓN LOGÍSTICA - POSTGRESQL
-- Modelo: Herencia (Tabla base + Tablas específicas)
-- ============================================================

-- Extensiones
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- TABLA: usuarios (Autenticación/Autorización)
-- ============================================================
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_usuarios_email ON usuarios(email);

-- ============================================================
-- TABLA: clientes
-- ============================================================
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER UNIQUE REFERENCES usuarios(id) ON DELETE SET NULL,
    nombre_completo VARCHAR(200) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(50),
    direccion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_clientes_email ON clientes(email);
CREATE INDEX idx_clientes_usuario_id ON clientes(usuario_id);

-- ============================================================
-- TABLA: productos
-- ============================================================
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    tipo_producto VARCHAR(100) NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL CHECK (precio_unitario > 0),
    tipo_logistica VARCHAR(20) NOT NULL CHECK (tipo_logistica IN ('terrestre', 'maritimo')),
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_productos_tipo_logistica ON productos(tipo_logistica);

-- ============================================================
-- TABLA: bodegas (Para logística terrestre)
-- ============================================================
CREATE TABLE bodegas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    ubicacion TEXT NOT NULL,
    ciudad VARCHAR(100),
    pais VARCHAR(100) DEFAULT 'Colombia',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLA: puertos (Para logística marítima)
-- ============================================================
CREATE TABLE puertos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    ubicacion TEXT NOT NULL,
    ciudad VARCHAR(100),
    pais VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLA BASE: envios
-- Campos comunes para todos los envíos
-- ============================================================
CREATE TABLE envios (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id) ON DELETE RESTRICT,
    producto_id INTEGER NOT NULL REFERENCES productos(id) ON DELETE RESTRICT,
    cantidad_producto INTEGER NOT NULL CHECK (cantidad_producto > 0),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_entrega DATE NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL CHECK (precio_unitario > 0),
    subtotal DECIMAL(10, 2) NOT NULL CHECK (subtotal >= 0),
    descuento DECIMAL(10, 2) DEFAULT 0 CHECK (descuento >= 0),
    total DECIMAL(10, 2) NOT NULL CHECK (total >= 0),
    estado VARCHAR(50) DEFAULT 'registrado' CHECK (estado IN ('registrado', 'en_transito', 'entregado', 'cancelado')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_envios_cliente ON envios(cliente_id);
CREATE INDEX idx_envios_producto ON envios(producto_id);
CREATE INDEX idx_envios_estado ON envios(estado);
CREATE INDEX idx_envios_fecha_entrega ON envios(fecha_entrega);

-- ============================================================
-- TABLA ESPECÍFICA: envios_terrestres
-- Hereda de envios (relación 1:1)
-- ============================================================
CREATE TABLE envios_terrestres (
    envio_id INTEGER PRIMARY KEY REFERENCES envios(id) ON DELETE CASCADE,
    placa VARCHAR(6) NOT NULL CHECK (placa ~ '^[A-Z]{3}[0-9]{3}$'),
    numero_guia VARCHAR(10) UNIQUE NOT NULL CHECK (LENGTH(numero_guia) = 10),
    bodega_id INTEGER NOT NULL REFERENCES bodegas(id) ON DELETE RESTRICT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_terrestres_placa ON envios_terrestres(placa);
CREATE INDEX idx_terrestres_bodega ON envios_terrestres(bodega_id);
CREATE UNIQUE INDEX idx_terrestres_numero_guia ON envios_terrestres(numero_guia);

-- ============================================================
-- TABLA ESPECÍFICA: envios_maritimos
-- Hereda de envios (relación 1:1)
-- ============================================================
CREATE TABLE envios_maritimos (
    envio_id INTEGER PRIMARY KEY REFERENCES envios(id) ON DELETE CASCADE,
    numero_flota VARCHAR(8) NOT NULL CHECK (numero_flota ~ '^[A-Z]{3}[0-9]{4}[A-Z]$'),
    numero_guia VARCHAR(10) UNIQUE NOT NULL CHECK (LENGTH(numero_guia) = 10),
    puerto_id INTEGER NOT NULL REFERENCES puertos(id) ON DELETE RESTRICT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_maritimos_flota ON envios_maritimos(numero_flota);
CREATE INDEX idx_maritimos_puerto ON envios_maritimos(puerto_id);
CREATE UNIQUE INDEX idx_maritimos_numero_guia ON envios_maritimos(numero_guia);

-- ============================================================
-- CONSTRAINT GLOBAL: numero_guia único entre ambas tablas
-- Se logra con índices únicos separados + validación en app
-- ============================================================

-- ============================================================
-- TRIGGERS: updated_at automático
-- ============================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_usuarios_updated_at BEFORE UPDATE ON usuarios
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_clientes_updated_at BEFORE UPDATE ON clientes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_productos_updated_at BEFORE UPDATE ON productos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_envios_updated_at BEFORE UPDATE ON envios
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================
-- DATOS DE PRUEBA (OPCIONAL)
-- ============================================================

-- Usuario de prueba (password: Admin123!)
INSERT INTO usuarios (email, password_hash) VALUES 
('admin@logistica.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyNqJVrXkZZi');

-- Clientes
INSERT INTO clientes (nombre_completo, email, telefono, direccion) VALUES 
('Juan Pérez', 'juan.perez@email.com', '3001234567', 'Calle 50 #23-45, Medellín'),
('María García', 'maria.garcia@email.com', '3109876543', 'Carrera 70 #80-12, Bogotá');

-- Bodegas
INSERT INTO bodegas (nombre, ubicacion, ciudad, pais) VALUES 
('Bodega Central Medellín', 'Zona Industrial Itagüí', 'Medellín', 'Colombia'),
('Bodega Norte Bogotá', 'Autopista Norte Km 15', 'Bogotá', 'Colombia');

-- Puertos
INSERT INTO puertos (nombre, ubicacion, ciudad, pais) VALUES 
('Puerto de Buenaventura', 'Costa Pacífica', 'Buenaventura', 'Colombia'),
('Puerto de Cartagena', 'Mar Caribe', 'Cartagena', 'Colombia'),
('Puerto de Miami', 'Florida', 'Miami', 'Estados Unidos');

-- Productos terrestres
INSERT INTO productos (tipo_producto, precio_unitario, tipo_logistica, descripcion) VALUES 
('Electrodomésticos', 50000.00, 'terrestre', 'Neveras, lavadoras, estufas'),
('Muebles', 35000.00, 'terrestre', 'Mesas, sillas, estanterías');

-- Productos marítimos
INSERT INTO productos (tipo_producto, precio_unitario, tipo_logistica, descripcion) VALUES 
('Contenedores 20ft', 850000.00, 'maritimo', 'Carga general internacional'),
('Vehículos', 1200000.00, 'maritimo', 'Automóviles y motos');

-- ============================================================
-- COMENTARIOS INFORMATIVOS
-- ============================================================
COMMENT ON TABLE envios IS 'Tabla base con campos comunes a todos los envíos';
COMMENT ON TABLE envios_terrestres IS 'Extensión para envíos por camión (herencia)';
COMMENT ON TABLE envios_maritimos IS 'Extensión para envíos por flota marítima (herencia)';
COMMENT ON COLUMN envios.subtotal IS 'precio_unitario * cantidad_producto';
COMMENT ON COLUMN envios.descuento IS '5% si cantidad>10 (terrestre) o 3% (marítimo)';
COMMENT ON COLUMN envios.total IS 'subtotal - descuento';
COMMENT ON COLUMN envios_terrestres.placa IS 'Formato: AAA123 (3 letras + 3 números)';
COMMENT ON COLUMN envios_maritimos.numero_flota IS 'Formato: AAA1234A (3 letras + 4 números + 1 letra)';
COMMENT ON COLUMN envios_terrestres.numero_guia IS '10 dígitos alfanuméricos únicos';
COMMENT ON COLUMN envios_maritimos.numero_guia IS '10 dígitos alfanuméricos únicos';