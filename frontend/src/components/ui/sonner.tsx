"use client";
import { Toaster as Sonner } from "sonner";

const Toaster = ({ ...props }) => {
  return (
    <Sonner
      theme="dark"
      className="toaster group"
      toastOptions={{
        classNames: {
          toast:
            "group toast !bg-zinc-800 !text-white !border !border-zinc-700 !shadow-xl",
          title: "!text-white !font-semibold",
          description: "!text-zinc-300",
          actionButton: "!bg-blue-600 !text-white",
          cancelButton: "!bg-zinc-700 !text-zinc-200",
          error: "!bg-red-950 !border-red-700 !text-red-200",
          success: "!bg-emerald-950 !border-emerald-700 !text-emerald-200",
          warning: "!bg-yellow-950 !border-yellow-700 !text-yellow-200",
          info: "!bg-blue-950 !border-blue-700 !text-blue-200",
        },
      }}
      {...props}
    />
  );
};

export { Toaster };