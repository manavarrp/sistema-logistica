import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useNavigate, Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { authService, type RegisterResponse } from '@/service/authService';
import { useAuthStore } from '@/store/authStore';
import { toast } from 'sonner';

const registerSchema = z.object({
  nombre_completo: z.string().min(2, { message: 'Mínimo 2 caracteres' }),
  email: z.string().email({ message: 'Email inválido' }),
  password: z.string().min(6, { message: 'Mínimo 6 caracteres' }),
  telefono: z.string().min(7, { message: 'Mínimo 7 caracteres' }),
  direccion: z.string().min(5, { message: 'Mínimo 5 caracteres' }),
});

type RegisterFormValues = z.infer<typeof registerSchema>;

export const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const setToken = useAuthStore((state) => state.setToken);

  const form = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      nombre_completo: '',
      email: '',
      password: '',
      telefono: '',
      direccion: '',
    },
  });

  const onSubmit = async (data: RegisterFormValues) => {
    try {
      const res: RegisterResponse = await authService.register(data);
      setToken(res.token.access_token, res.token.cliente_id);
      toast.success('Registro exitoso');
      navigate('/dashboard');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Error en el registro');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-zinc-950 relative overflow-hidden py-12">
      {/* Background decoration */}
      <div className="absolute top-[-10%] right-[-10%] w-[40%] h-[40%] bg-emerald-600/30 blur-[120px] rounded-full mix-blend-screen pointer-events-none" />
      <div className="absolute bottom-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-600/30 blur-[120px] rounded-full mix-blend-screen pointer-events-none" />

      <div className="w-full max-w-md p-8 rounded-2xl bg-zinc-900/50 backdrop-blur-xl border border-zinc-800 shadow-2xl relative z-10">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white tracking-tight">Crear Cuenta</h1>
          <p className="text-zinc-400 mt-2">Regístrate para gestionar tus envíos</p>
        </div>

        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="nombre_completo"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="text-zinc-300">Nombre Completo</FormLabel>
                  <FormControl>
                    <Input placeholder="Juan Pérez" className="bg-zinc-800/50 border-zinc-700 text-white" {...field} />
                  </FormControl>
                  <FormMessage className="text-red-400" />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="text-zinc-300">Email</FormLabel>
                  <FormControl>
                    <Input placeholder="tu@email.com" className="bg-zinc-800/50 border-zinc-700 text-white" {...field} />
                  </FormControl>
                  <FormMessage className="text-red-400" />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="text-zinc-300">Contraseña</FormLabel>
                  <FormControl>
                    <Input type="password" placeholder="••••••••" className="bg-zinc-800/50 border-zinc-700 text-white" {...field} />
                  </FormControl>
                  <FormMessage className="text-red-400" />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="telefono"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="text-zinc-300">Teléfono</FormLabel>
                  <FormControl>
                    <Input placeholder="3001234567" className="bg-zinc-800/50 border-zinc-700 text-white" {...field} />
                  </FormControl>
                  <FormMessage className="text-red-400" />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="direccion"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="text-zinc-300">Dirección</FormLabel>
                  <FormControl>
                    <Input placeholder="Calle 123 #45-67" className="bg-zinc-800/50 border-zinc-700 text-white" {...field} />
                  </FormControl>
                  <FormMessage className="text-red-400" />
                </FormItem>
              )}
            />
            <Button
              type="submit"
              className="w-full mt-6 bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-2 rounded-lg transition-all duration-200 shadow-[0_0_20px_rgba(5,150,105,0.3)] hover:shadow-[0_0_25px_rgba(5,150,105,0.5)]"
            >
              Registrarse
            </Button>
          </form>
        </Form>

        <div className="mt-6 text-center">
          <p className="text-zinc-400 text-sm">
            ¿Ya tienes cuenta?{' '}
            <Link to="/login" className="text-emerald-400 hover:text-emerald-300 hover:underline transition-colors">
              Inicia sesión
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};
