import { useCallback, useEffect, useState } from 'react'
import { envioMaritimoService, envioTerrestreService } from '@/service/envioService'
import { toast } from 'sonner'
import type {
  CrearEnvioMaritimoRequest,
  CrearEnvioTerrestreRequest,
  EnvioMaritimo,
  EnvioTerrestre,
  EstadoEnvio,
} from '@/interfaces'

// ── TERRESTRES ───────────────────────────────────────────────
export function useEnviosTerrestres() {
  const [envios, setEnvios] = useState<EnvioTerrestre[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const cargar = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await envioTerrestreService.listar()
      setEnvios(data)
    } catch {
      setError('Error al cargar envíos terrestres')
      toast.error('No se pudieron cargar los envíos terrestres')
    } finally {
      setLoading(false)
    }
  }, [])

  const crear = useCallback(async (data: CrearEnvioTerrestreRequest) => {
    try {
      const nuevo = await envioTerrestreService.crear(data)
      setEnvios((prev) => [nuevo, ...prev])
      toast.success('Envío terrestre creado exitosamente')
      return nuevo
    } catch (error: any) {
      const msg = error.response?.data?.detail || 'Error al crear envío terrestre'
      toast.error(msg)
      throw error
    }
  }, [])

  const cambiarEstado = useCallback(async (id: number, estado: EstadoEnvio) => {
    try {
      const actualizado = await envioTerrestreService.cambiarEstado(id, estado)
      setEnvios((prev) => prev.map((e) => (e.id === id ? actualizado : e)))
      toast.success(`Estado del envío #${id} actualizado a ${estado.replace('_', ' ')}`)
      return actualizado
    } catch (error: any) {
      const msg = error.response?.data?.detail || 'Error al cambiar estado'
      toast.error(msg)
      throw error
    }
  }, [])

  useEffect(() => { cargar() }, [cargar])

  return { envios, loading, error, refetch: cargar, crear, cambiarEstado }
}

// ── MARÍTIMOS ────────────────────────────────────────────────
export function useEnviosMaritimos() {
  const [envios, setEnvios] = useState<EnvioMaritimo[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const cargar = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await envioMaritimoService.listar()
      setEnvios(data)
    } catch {
      setError('Error al cargar envíos marítimos')
      toast.error('No se pudieron cargar los envíos marítimos')
    } finally {
      setLoading(false)
    }
  }, [])

  const crear = useCallback(async (data: CrearEnvioMaritimoRequest) => {
    try {
      const nuevo = await envioMaritimoService.crear(data)
      setEnvios((prev) => [nuevo, ...prev])
      toast.success('Envío marítimo creado exitosamente')
      return nuevo
    } catch (error: any) {
      const msg = error.response?.data?.detail || 'Error al crear envío marítimo'
      toast.error(msg)
      throw error
    }
  }, [])

  const cambiarEstado = useCallback(async (id: number, estado: EstadoEnvio) => {
    try {
      const actualizado = await envioMaritimoService.cambiarEstado(id, estado)
      setEnvios((prev) => prev.map((e) => (e.id === id ? actualizado : e)))
      toast.success(`Estado del envío #${id} actualizado a ${estado.replace('_', ' ')}`)
      return actualizado
    } catch (error: any) {
      const msg = error.response?.data?.detail || 'Error al cambiar estado'
      toast.error(msg)
      throw error
    }
  }, [])

  useEffect(() => { cargar() }, [cargar])

  return { envios, loading, error, refetch: cargar, crear, cambiarEstado }
}