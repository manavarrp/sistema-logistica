/**
 * Servicio de autenticación.
 * Conecta con los endpoints /auth del backend.
 */
import httpClient from '@/axios/httpclient'
import type { LoginRequest, RegisterRequest, TokenResponse, Cliente } from '@/interfaces'

export interface RegisterResponse {
  cliente: Cliente
  token: TokenResponse
}

export const authService = {
  register: async (data: RegisterRequest): Promise<RegisterResponse> => {
    const res = await httpClient.post<RegisterResponse>('/auth/register', data)
    return res.data
  },

  login: async (data: LoginRequest): Promise<TokenResponse> => {
    const res = await httpClient.post<TokenResponse>('/auth/login', data)
    return res.data
  },
}