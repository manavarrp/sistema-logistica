/**
 * Hooks de catálogos.
 * Cargan datos de solo lectura necesarios para los formularios de envío.
 */
import { useCallback, useEffect, useState } from 'react'
import { bodegaService, productoService, puertoService } from '@/service/catalogoService'
import type { Bodega, Producto, Puerto } from '@/interfaces'

export function useProductos() {
  const [productos, setProductos] = useState<Producto[]>([])
  const [loading, setLoading] = useState(false)

  const cargar = useCallback(async () => {
    setLoading(true)
    try {
      const data = await productoService.listar()
      setProductos(data)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { cargar() }, [cargar])

  return { productos, loading, refetch: cargar }
}

export function useBodegas() {
  const [bodegas, setBodegas] = useState<Bodega[]>([])
  const [loading, setLoading] = useState(false)

  const cargar = useCallback(async () => {
    setLoading(true)
    try {
      const data = await bodegaService.listar()
      setBodegas(data)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { cargar() }, [cargar])

  return { bodegas, loading }
}

export function usePuertos() {
  const [puertos, setPuertos] = useState<Puerto[]>([])
  const [loading, setLoading] = useState(false)

  const cargar = useCallback(async () => {
    setLoading(true)
    try {
      const data = await puertoService.listar()
      setPuertos(data)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { cargar() }, [cargar])

  return { puertos, loading }
}