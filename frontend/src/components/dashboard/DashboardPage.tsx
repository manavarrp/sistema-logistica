import React, { useState } from 'react';
import { useAuthStore } from '@/store/authStore';
import { useModalStore } from '@/store/modalStore';
import { useEnviosTerrestres, useEnviosMaritimos } from '@/hooks/useEnvios';
import { EnvioModal } from '@/components/modals/EnvioModal';
import { EditarEstadoModal } from '@/components/modals/EditarEstadoModal';
import { Button } from '@/components/ui/button';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { LogOut, Plus } from 'lucide-react';
import type { Envio } from '@/interfaces';

export const DashboardPage: React.FC = () => {
  const logout = useAuthStore((state) => state.logout);
  const openModal = useModalStore((state) => state.openModal);
  const [tab, setTab] = useState<'terrestres' | 'maritimos'>('terrestres');

  // ✅ Llamamos cada hook una sola vez y extraemos todo lo necesario
  const {
    envios: terrestres,
    loading: loadT,
    crear: crearTerrestre,
    refetch: refetchTerrestres,
  } = useEnviosTerrestres();

  const {
    envios: maritimos,
    loading: loadM,
    crear: crearMaritimo,
    refetch: refetchMaritimos,
  } = useEnviosMaritimos();

  const envios = tab === 'terrestres' ? terrestres : maritimos;
  const loading = tab === 'terrestres' ? loadT : loadM;

  // ✅ Función que retorna el refresh según la pestaña activa
  const getRefresh = () => (tab === 'terrestres' ? refetchTerrestres : refetchMaritimos);

  // ✅ Manejador para abrir el modal de creación con el refresh adecuado
  // ✅ Pasarlos en el payload del modal
  const handleNuevoEnvio = () => {
    openModal('crear-envio', {
      crearTerrestre,             // ← agregar
      crearMaritimo,              // ← agregar
      onRefresh: () => {
        refetchTerrestres();
        refetchMaritimos();
      },
    });
  };

  // ✅ Manejador para abrir el modal de edición de estado con el refresh adecuado
  const handleEditarEstado = (envioId: number, tipo: 'terrestre' | 'maritimo') => {
    openModal('editar-estado', {
      envioId,
      tipoLogistica: tipo,
      onRefresh: getRefresh(),
    });
  };


  return (
    <div className="min-h-screen bg-zinc-950 text-white p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        <header className="flex justify-between items-center pb-6 border-b border-zinc-800">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Panel de Envíos</h1>
            <p className="text-zinc-400 mt-1">Gestiona tus envíos terrestres y marítimos</p>
          </div>
          <div className="flex gap-4">
            <Button
              onClick={handleNuevoEnvio}  // ✅ Cambiado
              className="bg-blue-600 hover:bg-blue-700 shadow-[0_0_15px_rgba(37,99,235,0.3)]"
            >
              <Plus className="w-4 h-4 mr-2" />
              Nuevo Envío
            </Button>
            <Button
              variant="outline"
              className="border-zinc-700 bg-zinc-900 text-white hover:bg-zinc-800 hover:text-white"
              onClick={logout}
            >
              <LogOut className="w-4 h-4 mr-2" />
              Salir
            </Button>
          </div>
        </header>

        <div className="flex space-x-4 mb-4">
          <Button
            variant={tab === 'terrestres' ? 'default' : 'secondary'}
            className={
              tab === 'terrestres'
                ? 'bg-blue-600 hover:bg-blue-700'
                : 'bg-zinc-800 hover:bg-zinc-700 text-zinc-300'
            }
            onClick={() => setTab('terrestres')}
          >
            Terrestres
          </Button>
          <Button
            variant={tab === 'maritimos' ? 'default' : 'secondary'}
            className={
              tab === 'maritimos'
                ? 'bg-purple-600 hover:bg-purple-700 text-white'
                : 'bg-zinc-800 hover:bg-zinc-700 text-zinc-300'
            }
            onClick={() => setTab('maritimos')}
          >
            Marítimos
          </Button>
        </div>

        <div className="rounded-xl border border-zinc-800 bg-zinc-900/50 backdrop-blur-sm overflow-hidden shadow-2xl">
          {loading ? (
            <div className="p-8 text-center text-zinc-400">Cargando envíos...</div>
          ) : envios.length === 0 ? (
            <div className="p-8 text-center text-zinc-400">No hay envíos registrados.</div>
          ) : (
            <Table>
              <TableHeader className="bg-zinc-800/50">
                <TableRow className="border-zinc-800 hover:bg-transparent">
                  <TableHead className="text-zinc-300">Guía</TableHead>
                  <TableHead className="text-zinc-300">Fecha Registro</TableHead>
                  <TableHead className="text-zinc-300">Fecha Entrega</TableHead>
                  <TableHead className="text-zinc-300">Estado</TableHead>
                  <TableHead className="text-zinc-300">Cantidad</TableHead>
                  <TableHead className="text-zinc-300 text-right">Total</TableHead>
                  <TableHead className="text-zinc-300 text-right">Acciones</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {envios.map((envio: Envio) => (
                  <TableRow key={envio.id} className="border-zinc-800 hover:bg-zinc-800/50 transition-colors">
                    <TableCell className="font-medium text-blue-400">{envio.numero_guia}</TableCell>
                    <TableCell>{new Date(envio.fecha_registro).toLocaleDateString()}</TableCell>
                    <TableCell>{new Date(envio.fecha_entrega).toLocaleDateString()}</TableCell>
                    <TableCell>
                      <span
                        className={`px-2 py-1 rounded-full text-xs font-medium capitalize
                          ${envio.estado === 'registrado' ? 'bg-blue-500/20 text-blue-300' : ''}
                          ${envio.estado === 'en_transito' ? 'bg-purple-500/20 text-purple-300' : ''}
                          ${envio.estado === 'entregado' ? 'bg-emerald-500/20 text-emerald-300' : ''}
                          ${envio.estado === 'cancelado' ? 'bg-red-500/20 text-red-300' : ''}
                        `}
                      >
                        {envio.estado.replace('_', ' ')}
                      </span>
                    </TableCell>
                    <TableCell>{envio.cantidad_producto}</TableCell>
                    <TableCell className="text-right font-semibold text-emerald-400">
                      ${Number(envio.total).toFixed(2)}
                    </TableCell>
                    <TableCell className="text-right">
                      <Button
                        variant="ghost"
                        size="sm"
                        className="text-blue-400 hover:text-blue-300 hover:bg-zinc-800"
                        onClick={() =>
                          handleEditarEstado(
                            envio.id,
                            tab === 'terrestres' ? 'terrestre' : 'maritimo'
                          )
                        }
                      >
                        Cambiar estado
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </div>
      </div>

      <EnvioModal />
      <EditarEstadoModal />
    </div>
  );
};