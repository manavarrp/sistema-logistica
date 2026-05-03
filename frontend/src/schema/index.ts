/**
 * Schemas de validación con Zod.
 * Se usan con react-hook-form mediante @hookform/resolvers/zod
 */
import { z } from 'zod'

// ── AUTH ─────────────────────────────────────────────────────
export const loginSchema = z.object({
  email: z.string().email('Email inválido'),
  password: z.string().min(6, 'Mínimo 6 caracteres'),
})

export const registerSchema = z.object({
  email: z.string().email('Email inválido'),
  password: z.string().min(6, 'Mínimo 6 caracteres'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Las contraseñas no coinciden',
  path: ['confirmPassword'],
})

// ── ENVÍO TERRESTRE ──────────────────────────────────────────
export const envioTerrestreSchema = z.object({
  cliente_id: z.number().int().positive(),
  producto_id: z.number().int().positive('Selecciona un producto'),
  cantidad_producto: z.number().int().min(1, 'Mínimo 1 unidad'),
  fecha_entrega: z.string().min(1, 'Fecha requerida'),
  placa: z
    .string()
    .toUpperCase()
    .regex(/^[A-Z]{3}[0-9]{3}$/, 'Formato: AAA123'),
  numero_guia: z
    .string()
    .toUpperCase()
    .regex(/^[A-Z0-9]{10}$/, 'Debe tener 10 caracteres alfanuméricos'),
  bodega_id: z.number().int().positive('Selecciona una bodega'),
})

// ── ENVÍO MARÍTIMO ────────────────────────────────────────────
export const envioMaritimoSchema = z.object({
  cliente_id: z.number().int().positive(),
  producto_id: z.number().int().positive('Selecciona un producto'),
  cantidad_producto: z.number().int().min(1, 'Mínimo 1 unidad'),
  fecha_entrega: z.string().min(1, 'Fecha requerida'),
  numero_flota: z
    .string()
    .toUpperCase()
    .regex(/^[A-Z]{3}[0-9]{4}[A-Z]$/, 'Formato: AAA1234A'),
  numero_guia: z
    .string()
    .toUpperCase()
    .regex(/^[A-Z0-9]{10}$/, 'Debe tener 10 caracteres alfanuméricos'),
  puerto_id: z.number().int().positive('Selecciona un puerto'),
})

// ── TIPOS INFERIDOS ──────────────────────────────────────────
export type LoginFormValues = z.infer<typeof loginSchema>
export type RegisterFormValues = z.infer<typeof registerSchema>
export type EnvioTerrestreFormValues = z.infer<typeof envioTerrestreSchema>
export type EnvioMaritimoFormValues = z.infer<typeof envioMaritimoSchema>