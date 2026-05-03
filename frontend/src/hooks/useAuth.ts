/**
 * Hook de autenticación.
 * Login persiste solo el token — el backend maneja el cliente por email.
 */
import { useCallback, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authService } from '@/service/authService'
import { useAuthStore } from '@/store/authStore'
import type { LoginFormValues, RegisterFormValues } from '@/schema'

export function useAuth() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const { setToken, logout, isAuthenticated } = useAuthStore()
  const navigate = useNavigate()

  const login = useCallback(async (data: LoginFormValues) => {
    setLoading(true)
    setError(null)
    try {
      const result = await authService.login(data)
      setToken(result.access_token)
      navigate('/dashboard')
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } } })
        ?.response?.data?.detail ?? 'Error al iniciar sesión'
      setError(msg)
    } finally {
      setLoading(false)
    }
  }, [setToken, navigate])

  const register = useCallback(async (data: RegisterFormValues) => {
    setLoading(true)
    setError(null)
    try {
      await authService.register({ email: data.email, password: data.password })
      navigate('/login')
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } } })
        ?.response?.data?.detail ?? 'Error al registrarse'
      setError(msg)
    } finally {
      setLoading(false)
    }
  }, [navigate])

  const handleLogout = useCallback(() => {
    logout()
    navigate('/login')
  }, [logout, navigate])

  return { login, register, logout: handleLogout, loading, error, isAuthenticated }
}