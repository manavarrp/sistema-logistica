/**
 * Servicios para envíos terrestres y marítimos.
 * Sigue el flujo: axios → service → hook → componente
 */
import httpClient from '@/axios/httpclient'
import type {
  CrearEnvioMaritimoRequest,
  CrearEnvioTerrestreRequest,
  EnvioMaritimo,
  EnvioTerrestre,
  EstadoEnvio,
} from '@/interfaces'

// ── TERRESTRES ───────────────────────────────────────────────
export const envioTerrestreService = {
  listar: async (): Promise<EnvioTerrestre[]> => {
    const res = await httpClient.get<EnvioTerrestre[]>('/envios-terrestres/')
    return res.data
  },

  obtener: async (id: number): Promise<EnvioTerrestre> => {
    const res = await httpClient.get<EnvioTerrestre>(`/envios-terrestres/${id}`)
    return res.data
  },

  crear: async (data: CrearEnvioTerrestreRequest): Promise<EnvioTerrestre> => {
    const res = await httpClient.post<EnvioTerrestre>('/envios-terrestres/', data)
    return res.data
  },

  cambiarEstado: async (id: number, estado: EstadoEnvio): Promise<EnvioTerrestre> => {
    const res = await httpClient.patch<EnvioTerrestre>(
      `/envios-terrestres/${id}/estado`,
      { estado }
    )
    return res.data
  },
}

// ── MARÍTIMOS ────────────────────────────────────────────────
export const envioMaritimoService = {
  listar: async (): Promise<EnvioMaritimo[]> => {
    const res = await httpClient.get<EnvioMaritimo[]>('/envios-maritimos/')
    return res.data
  },

  obtener: async (id: number): Promise<EnvioMaritimo> => {
    const res = await httpClient.get<EnvioMaritimo>(`/envios-maritimos/${id}`)
    return res.data
  },

  crear: async (data: CrearEnvioMaritimoRequest): Promise<EnvioMaritimo> => {
    const res = await httpClient.post<EnvioMaritimo>('/envios-maritimos/', data)
    return res.data
  },

  cambiarEstado: async (id: number, estado: EstadoEnvio): Promise<EnvioMaritimo> => {
    const res = await httpClient.patch<EnvioMaritimo>(
      `/envios-maritimos/${id}/estado`,
      { estado }
    )
    return res.data
  },
}

