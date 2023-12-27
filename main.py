import tkinter as tk
from tkinter import messagebox
import os

def ejecutar_algoritmo(algoritmo):
    archivo = f"{algoritmo}.py"
    if os.path.exists(archivo):
        os.system(f"python {archivo}")
    else:
        messagebox.showerror("Error", f"El archivo {archivo} no existe.")

def seleccionar_algoritmo(algoritmo):
    ejecutar_algoritmo(algoritmo)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Selector de Algoritmos")

# Estilo para los botones
estilo_botones = {
    'font': ('Arial', 14),
    'width': 15,
    'height': 2,
    'bg': '#3498db',  # color de fondo azul
    'fg': 'white',    # color de texto blanco
    'border': 0,      # sin borde
}

# Crear etiqueta
etiqueta = tk.Label(ventana, text="Selecciona un algoritmo:", font=('Arial', 18))
etiqueta.pack(pady=20)

# Crear y estilizar botones
algoritmos = ["FCFS", "SJF", "SJFR", "RR", "RRprioridad"]
for algoritmo in algoritmos:
    boton = tk.Button(ventana, text=algoritmo, command=lambda algo=algoritmo: seleccionar_algoritmo(algo), **estilo_botones)
    boton.pack(pady=10)

# Ejecutar la aplicación
ventana.mainloop()
