/**
 * Store de autenticación con Zustand.
 * Solo persiste el token JWT — el cliente se maneja por email en el backend.
 */
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AuthState {
  token: string | null
  clienteId: number | null
  isAuthenticated: boolean
  setToken: (token: string, clienteId: number) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      clienteId: null,
      isAuthenticated: false,

      setToken: (token: string, clienteId: number) => {
        localStorage.setItem('access_token', token)
        set({ token, clienteId, isAuthenticated: true })
      },

      logout: () => {
        localStorage.removeItem('access_token')
        set({ token: null, clienteId: null, isAuthenticated: false })
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ 
        token: state.token, 
        clienteId: state.clienteId,
        isAuthenticated: state.isAuthenticated 
      }),
      onRehydrateStorage: () => (state) => {
        // ✅ Recuperar clienteId del token si falta (para sesiones activas)
        if (state?.token && !state.clienteId) {
          try {
            const payload = JSON.parse(atob(state.token.split('.')[1]))
            if (payload.cliente_id) {
              state.clienteId = payload.cliente_id
            }
          } catch (e) {
            console.error('Error decoding token', e)
          }
        }

        // Si el token persiste pero localStorage fue limpiado externamente, sincronizamos
        if (state?.token) {
          localStorage.setItem('access_token', state.token)
        }
      },
    }
  )
)