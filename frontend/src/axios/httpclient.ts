/**
 * Instancia base de Axios.
 * Responsabilidades:
 * - Adjunta el token JWT en cada request automáticamente
 * - Intercepta 401 y limpia sesión
 */
import axios from 'axios'

const httpClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL ? `${import.meta.env.VITE_API_URL}/api/v1` : '/api/v1',
  headers: { 'Content-Type': 'application/json' },
  timeout: 10_000,
})

// Request interceptor → adjunta Bearer token
httpClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor → maneja 401 globalmente (excepto en rutas de auth)
httpClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const isAuthRoute = error.config?.url?.includes('/auth/')
    if (error.response?.status === 401 && !isAuthRoute) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default httpClient
// Forced update for Vercel cache casing fix