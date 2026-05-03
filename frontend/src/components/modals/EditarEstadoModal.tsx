import React, { useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useModalStore } from '@/store/modalStore'
import { useEnviosTerrestres, useEnviosMaritimos } from '@/hooks/useEnvios'
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
} from '@/components/ui/dialog'
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from '@/components/ui/form'
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue
} from '@/components/ui/select'
import { Button } from '@/components/ui/button'

const estados = ['registrado', 'en_transito', 'entregado', 'cancelado'] as const
type Estado = typeof estados[number]

const formSchema = z.object({
    estado: z.enum(estados),
})

export const EditarEstadoModal: React.FC = () => {
    const { activeModal, closeModal, payload } = useModalStore()
    const isOpen = activeModal === 'editar-estado'

    const { cambiarEstado: cambiarTerrestre } = useEnviosTerrestres()
    const { cambiarEstado: cambiarMaritimo } = useEnviosMaritimos()

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: { estado: 'registrado' },
    })

    useEffect(() => {
        if (isOpen) {
            form.reset({ estado: 'registrado' })
        }
    }, [isOpen, form])

    const onSubmit = async (data: { estado: Estado }) => {
        if (!payload.envioId || !payload.tipoLogistica) return
        try {
            if (payload.tipoLogistica === 'terrestre') {
                await cambiarTerrestre(payload.envioId, data.estado)
            } else {
                await cambiarMaritimo(payload.envioId, data.estado)
            }

            if (payload.onRefresh) {
                payload.onRefresh()
            }

            closeModal()
        } catch {

        }
    }

    return (
        <Dialog open={isOpen} onOpenChange={closeModal}>
            <DialogContent className="sm:max-w-[400px] bg-zinc-900 border-zinc-800 text-white">
                <DialogHeader>
                    <DialogTitle>Cambiar estado del envío</DialogTitle>
                    <DialogDescription className="text-zinc-400">
                        Envío #{payload.envioId} — selecciona el nuevo estado
                    </DialogDescription>
                </DialogHeader>
                <Form {...form}>
                    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                        <FormField
                            control={form.control}
                            name="estado"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel className="text-zinc-300">Estado</FormLabel>
                                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                                        <FormControl>
                                            <SelectTrigger className="bg-zinc-800/50 border-zinc-700 text-white">
                                                <SelectValue placeholder="Selecciona un estado" />
                                            </SelectTrigger>
                                        </FormControl>
                                        <SelectContent className="bg-zinc-800 border-zinc-700 text-white">
                                            {estados.map((est) => (
                                                <SelectItem key={est} value={est}>
                                                    {est.replace('_', ' ').toUpperCase()}
                                                </SelectItem>
                                            ))}
                                        </SelectContent>
                                    </Select>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                        <div className="flex justify-end gap-3 pt-4 border-t border-zinc-800">
                            <Button type="button" variant="outline" className="border-zinc-700 bg-zinc-900 hover:bg-zinc-800" onClick={closeModal}>
                                Cancelar
                            </Button>
                            <Button type="submit" className="bg-blue-600 hover:bg-blue-700">
                                Guardar cambio
                            </Button>
                        </div>
                    </form>
                </Form>
            </DialogContent>
        </Dialog>
    )
}