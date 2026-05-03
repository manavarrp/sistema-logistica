import React, { useEffect, useState } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';

export const ProtectedRoute: React.FC = () => {
  const { isAuthenticated } = useAuthStore();
  // Flag para saber si zustand ya terminó de hidratar desde localStorage
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    // useAuthStore.persist.hasHydrated() puede no estar disponible en todas las versiones,
    // así que usamos un pequeño timeout de 0ms para dejar que zustand se hidrate primero.
    const unsub = useAuthStore.persist.onFinishHydration(() => {
      setHydrated(true);
    });

    // Si ya estaba hidratado antes de montar el componente
    if (useAuthStore.persist.hasHydrated()) {
      setHydrated(true);
    }

    return () => unsub();
  }, []);

  // Mientras hydrata, usar localStorage como fuente de verdad inmediata
  const tokenInStorage = localStorage.getItem('access_token');

  if (!hydrated) {
    // Aún hidratando: si hay token en storage dejamos pasar, si no redirigimos
    return tokenInStorage ? <Outlet /> : <Navigate to="/login" replace />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
};
