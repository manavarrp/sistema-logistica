import * as React from "react"
import { cn } from "@/lib/utils"

// 1. Definimos la interfaz de las props
export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> { }

// 2. Usamos forwardRef para que el componente pueda recibir la ref de Shadcn/React-Hook-Form
const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          "flex h-9 w-full rounded-md border border-input bg-zinc-950 px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-zinc-500 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-blue-600 disabled:cursor-not-allowed disabled:opacity-50",
          className
        )}
        ref={ref} // <--- ¡Esto es lo más importante!
        {...props}
      />
    )
  }
)

Input.displayName = "Input"

export { Input }