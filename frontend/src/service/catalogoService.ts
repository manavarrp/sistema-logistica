/**
 * Servicios para catálogos: Productos, Bodegas, Puertos.
 * Son de solo lectura desde el frontend del cliente.
 */
import httpClient from '@/axios/httpClient'
import type { Bodega, Producto, Puerto } from '@/interfaces'

export const productoService = {
  listar: async (): Promise<Producto[]> => {
    const res = await httpClient.get<Producto[]>('/productos/')
    return res.data
  },
}

export const bodegaService = {
  listar: async (): Promise<Bodega[]> => {
    const res = await httpClient.get<Bodega[]>('/bodegas/')
    return res.data
  },
}

export const puertoService = {
  listar: async (): Promise<Puerto[]> => {
    const res = await httpClient.get<Puerto[]>('/puertos/')
    return res.data
  },
}