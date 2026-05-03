/**
 * Store global de modals con Zustand.
 * Centraliza la apertura/cierre de modals desde cualquier componente
 * sin necesidad de prop drilling.
 */
import { create } from 'zustand'

type ModalType = 'crear-envio' | 'editar-estado' | null

// modalStore.ts — ampliar ModalPayload
interface ModalPayload {
  envioId?: number
  tipoLogistica?: 'terrestre' | 'maritimo'
  onRefresh?: () => void
  crearTerrestre?: (data: any) => Promise<any>
  crearMaritimo?: (data: any) => Promise<any>
}

interface ModalState {
  activeModal: ModalType
  payload: ModalPayload
  openModal: (modal: ModalType, payload?: ModalPayload) => void
  closeModal: () => void
}

export const useModalStore = create<ModalState>((set) => ({
  activeModal: null,
  payload: {},
  openModal: (modal, payload = {}) => set({ activeModal: modal, payload }),
  closeModal: () => {
    const payload = useModalStore.getState().payload;
    if (payload.onRefresh) payload.onRefresh();
    set({ activeModal: null, payload: {} });
  },
}))