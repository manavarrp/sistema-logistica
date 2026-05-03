import React, { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useModalStore } from '@/store/modalStore';
import { useAuthStore } from '@/store/authStore';
import { useProductos, useBodegas, usePuertos } from '@/hooks/useCatalogo';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from '@/components/ui/dialog';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { toast } from 'sonner';

const baseSchema = z.object({
  producto_id: z.string().min(1, 'Seleccione un producto'),
  cantidad_producto: z.number().min(1, 'Mínimo 1'),
  fecha_entrega: z.string().min(1, 'Requerido').refine((val) => {
    const selectedDate = new Date(val + 'T00:00:00');
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return selectedDate >= today;
  }, { message: 'La fecha no puede ser anterior a hoy' }),
  numero_guia: z.string().length(10, 'Debe tener exactamente 10 caracteres'),
});

const terrestreSchema = baseSchema.extend({
  placa: z.string().regex(/^[A-Za-z]{3}[0-9]{3}$/, 'Formato AAA000'),
  bodega_id: z.string().min(1, 'Requerido'),
});

const maritimoSchema = baseSchema.extend({
  numero_flota: z.string().regex(/^[A-Za-z]{3}[0-9]{4}[A-Za-z]$/, 'Formato AAA0000A'),
  puerto_id: z.string().min(1, 'Requerido'),
});

export const EnvioModal: React.FC = () => {
  // ✅ Se agrega payload a la desestructuración
  const { activeModal, closeModal, payload } = useModalStore();
  const { clienteId } = useAuthStore();
  const isOpen = activeModal === 'crear-envio';

  const { productos } = useProductos();
  const { bodegas } = useBodegas();
  const { puertos } = usePuertos();

  const [tipoLogistica, setTipoLogistica] = useState<'terrestre' | 'maritimo' | null>(null);

  const generateGuia = () => Math.random().toString(36).substring(2, 12).toUpperCase();

  const currentSchema =
    tipoLogistica === 'terrestre'
      ? terrestreSchema
      : tipoLogistica === 'maritimo'
        ? maritimoSchema
        : baseSchema;

  const form = useForm<z.infer<typeof currentSchema>>({
    resolver: zodResolver(currentSchema),
    defaultValues: {
      producto_id: '',
      cantidad_producto: 1,
      fecha_entrega: '',
      numero_guia: generateGuia(),
      placa: '',
      bodega_id: '',
      numero_flota: '',
      puerto_id: '',
    },
  });

  const watchProductoId = form.watch('producto_id');

  useEffect(() => {
    if (watchProductoId) {
      const prod = productos.find((p) => p.id.toString() === watchProductoId);
      if (prod) {
        setTipoLogistica(prod.tipo_logistica);
      }
    } else {
      setTipoLogistica(null);
    }
  }, [watchProductoId, productos]);

  // ✅ Limpiar estado al cerrar/abrir el modal
  useEffect(() => {
    if (!isOpen) {
      form.reset();
      setTipoLogistica(null);
    }
  }, [isOpen]);

  const onSubmit = async (data: any) => {
    if (!clienteId) {
      toast.error('Error: No se encontró el ID del cliente. Por favor, re-inicia sesión.');
      return;
    }
    try {
      const body = { 
        ...data, 
        producto_id: parseInt(data.producto_id, 10),
        cliente_id: clienteId,
        placa: data.placa?.toUpperCase(),
        numero_flota: data.numero_flota?.toUpperCase()
      };

      if (tipoLogistica === 'terrestre') {
        body.bodega_id = parseInt(data.bodega_id, 10);
        // ✅ Usa la función que viene del payload (del Dashboard)
        await payload.crearTerrestre!(body);
      } else {
        body.puerto_id = parseInt(data.puerto_id, 10);
        // ✅ Usa la función que viene del payload (del Dashboard)
        await payload.crearMaritimo!(body);
      }

      // ✅ Refrescar el panel si existe la función en el payload
      if (payload.onRefresh) {
        payload.onRefresh();
      }

      closeModal();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Error al crear el envío');
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={closeModal}>
      <DialogContent className="sm:max-w-[500px] bg-zinc-900 border-zinc-800 text-white shadow-2xl">
        <DialogHeader>
          <DialogTitle className="text-xl font-bold">Crear Nuevo Envío</DialogTitle>
          <DialogDescription className="text-zinc-400">
            Completa los datos. El tipo de envío se asignará según el producto seleccionado.
          </DialogDescription>
        </DialogHeader>

        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="producto_id"
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel className="text-zinc-300">Producto</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                      <FormControl>
                        <SelectTrigger className="bg-zinc-800/50 border-zinc-700 text-white">
                          <SelectValue placeholder="Seleccione un producto" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent className="bg-zinc-800 border-zinc-700 text-white">
                        {productos.map((p) => (
                          <SelectItem key={p.id} value={p.id.toString()}>
                            {p.tipo_producto} - ${p.precio_unitario} ({p.tipo_logistica})
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage className="text-red-400" />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="cantidad_producto"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="text-zinc-300">Cantidad</FormLabel>
                    <FormControl>
                      <Input
                        type="number"
                        min={1}
                        className="bg-zinc-800/50 border-zinc-700 text-white"
                        {...field}
                        onChange={(e) => field.onChange(Number(e.target.value))}
                      />
                    </FormControl>
                    <FormMessage className="text-red-400" />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="fecha_entrega"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="text-zinc-300">Fecha de Entrega</FormLabel>
                    <FormControl>
                      <Input type="date" className="bg-zinc-800/50 border-zinc-700 text-white" {...field} />
                    </FormControl>
                    <FormMessage className="text-red-400" />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="numero_guia"
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel className="text-zinc-300">Número de Guía</FormLabel>
                    <FormControl>
                      <Input
                        className="bg-zinc-800/50 border-zinc-700 text-white uppercase font-mono"
                        maxLength={10}
                        {...field}
                      />
                    </FormControl>
                    <FormMessage className="text-red-400" />
                  </FormItem>
                )}
              />
            </div>

            {tipoLogistica === 'terrestre' && (
              <div className="grid grid-cols-2 gap-4 p-4 mt-4 bg-blue-900/10 border border-blue-900/30 rounded-lg">
                <FormField
                  control={form.control}
                  name="placa"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-blue-300">Placa Vehículo</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="AAA000"
                          className="bg-zinc-800/50 border-zinc-700 text-white uppercase"
                          maxLength={6}
                          {...field}
                        />
                      </FormControl>
                      <FormMessage className="text-red-400" />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="bodega_id"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-blue-300">Bodega de Entrega</FormLabel>
                      <Select onValueChange={field.onChange} defaultValue={field.value}>
                        <FormControl>
                          <SelectTrigger className="bg-zinc-800/50 border-zinc-700 text-white">
                            <SelectValue placeholder="Seleccione bodega" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent className="bg-zinc-800 border-zinc-700 text-white">
                          {bodegas.map((b) => (
                            <SelectItem key={b.id} value={b.id.toString()}>
                              {b.nombre} - {b.ciudad}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <FormMessage className="text-red-400" />
                    </FormItem>
                  )}
                />
              </div>
            )}

            {tipoLogistica === 'maritimo' && (
              <div className="grid grid-cols-2 gap-4 p-4 mt-4 bg-purple-900/10 border border-purple-900/30 rounded-lg">
                <FormField
                  control={form.control}
                  name="numero_flota"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-purple-300">Número de Flota</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="AAA0000A"
                          className="bg-zinc-800/50 border-zinc-700 text-white uppercase"
                          maxLength={8}
                          {...field}
                        />
                      </FormControl>
                      <FormMessage className="text-red-400" />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="puerto_id"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-purple-300">Puerto de Entrega</FormLabel>
                      <Select onValueChange={field.onChange} defaultValue={field.value}>
                        <FormControl>
                          <SelectTrigger className="bg-zinc-800/50 border-zinc-700 text-white">
                            <SelectValue placeholder="Seleccione puerto" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent className="bg-zinc-800 border-zinc-700 text-white">
                          {puertos.map((p) => (
                            <SelectItem key={p.id} value={p.id.toString()}>
                              {p.nombre} - {p.ciudad}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <FormMessage className="text-red-400" />
                    </FormItem>
                  )}
                />
              </div>
            )}

            <div className="flex justify-end gap-3 pt-4 border-t border-zinc-800">
              <Button
                type="button"
                variant="outline"
                className="border-zinc-700 bg-zinc-900 text-white hover:bg-zinc-800"
                onClick={closeModal}
              >
                Cancelar
              </Button>
              <Button type="submit" disabled={!tipoLogistica} className="bg-blue-600 hover:bg-blue-700">
                Guardar Envío
              </Button>
            </div>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
};