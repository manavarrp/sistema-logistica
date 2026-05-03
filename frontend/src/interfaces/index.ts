/**
 * Interfaces TypeScript que reflejan los schemas del backend.
 * Cada interfaz corresponde a un response schema de FastAPI.
 */

// ── AUTH ────────────────────────────────────────────────────
export interface TokenResponse {
  access_token: string
  token_type: string
  cliente_id: number
}

export interface UsuarioResponse {
  id: number
  email: string
  is_active: boolean
}

// ── CLIENTE ─────────────────────────────────────────────────
export interface Cliente {
  id: number
  nombre_completo: string
  email: string
  telefono: string | null
  direccion: string | null
}

// ── PRODUCTO ────────────────────────────────────────────────
export interface Producto {
  id: number
  tipo_producto: string
  precio_unitario: number
  tipo_logistica: 'terrestre' | 'maritimo'
  descripcion: string | null
}

// ── BODEGA ──────────────────────────────────────────────────
export interface Bodega {
  id: number
  nombre: string
  ubicacion: string
  ciudad: string | null
  pais: string
}

// ── PUERTO ──────────────────────────────────────────────────
export interface Puerto {
  id: number
  nombre: string
  ubicacion: string
  ciudad: string | null
  pais: string
}

// ── ENVÍO TERRESTRE ─────────────────────────────────────────
export interface EnvioTerrestre {
  id: number
  cliente_id: number
  producto_id: number
  cantidad_producto: number
  fecha_registro: string
  fecha_entrega: string
  precio_unitario: number
  subtotal: number
  descuento: number
  total: number
  estado: EstadoEnvio
  placa: string
  numero_guia: string
  bodega_id: number
}

// ── ENVÍO MARÍTIMO ──────────────────────────────────────────
export interface EnvioMaritimo {
  id: number
  cliente_id: number
  producto_id: number
  cantidad_producto: number
  fecha_registro: string
  fecha_entrega: string
  precio_unitario: number
  subtotal: number
  descuento: number
  total: number
  estado: EstadoEnvio
  numero_flota: string
  numero_guia: string
  puerto_id: number
}

export type EstadoEnvio = 'registrado' | 'en_transito' | 'entregado' | 'cancelado'

// ── UNION TYPE para listas mixtas ────────────────────────────
export type Envio = EnvioTerrestre | EnvioMaritimo

// ── REQUESTS ────────────────────────────────────────────────
export interface RegisterRequest {
  email: string
  password: string
  nombre_completo: string
  telefono?: string
  direccion?: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface CrearEnvioTerrestreRequest {
  cliente_id: number
  producto_id: number
  cantidad_producto: number
  fecha_entrega: string
  placa: string
  numero_guia: string
  bodega_id: number
}

export interface CrearEnvioMaritimoRequest {
  cliente_id: number
  producto_id: number
  cantidad_producto: number
  fecha_entrega: string
  numero_flota: string
  numero_guia: string
  puerto_id: number
}

export interface EstadoUpdateRequest {
  estado: EstadoEnvio
}