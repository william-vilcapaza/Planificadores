import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns

def dibujar_barra_horizontal(valorfinal, tiempos_espera, tiempos_inicio, tiempos_duracion):
    fig, ax = plt.subplots(figsize=(8, 2))
    colores = sns.color_palette("husl", n_colors=len(tiempos_espera))
    y_coord = 0.5

    for proceso, tiempo_espera in tiempos_espera.items():
        tiempo_inicio = tiempos_inicio[proceso]
        tiempo_duracion = tiempos_duracion[proceso]

        ax.barh(y_coord, tiempo_duracion, left=tiempo_inicio, color=colores.pop(0), label=proceso)

        y_coord += 0.5

    # Configurar ejes y etiquetas
    ax.set_xlim(0, valorfinal + 1)
    ax.set_xlabel('Tiempo')
    ax.set_yticks([])
    ax.set_xticks(np.arange(0, valorfinal + 1, 1))
    ax.set_xticklabels([str(i) for i in range(int(valorfinal) + 1)])

    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=ventana_sjf)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def sjf(procesos):
    # Ordenar los procesos por duración de manera ascendente
    procesos_ordenados = sorted(procesos, key=lambda x: x['duracion'])

    tiempo_espera = 0
    tiempo_retorno = 0
    tiempo_actual = 0

    tiempos_espera_por_proceso = {}  # Almacenar tiempos de espera por proceso
    tiempos_inicio = {}  # Almacenar tiempos de inicio
    tiempos_duracion = {}  # Almacenar tiempos de duración

    for proceso in procesos_ordenados:
        # Calcular el tiempo de espera para cada proceso
        tiempos_espera_por_proceso[proceso['nombre']] = max(0, tiempo_actual)
        tiempo_espera += tiempos_espera_por_proceso[proceso['nombre']]

        tiempo_retorno += tiempo_actual + proceso['duracion']

        # Almacenar tiempos de inicio y duración
        tiempos_inicio[proceso['nombre']] = tiempo_actual
        tiempos_duracion[proceso['nombre']] = proceso['duracion']

        tiempo_actual += proceso['duracion']

    promedio_tiempo_espera = tiempo_espera / len(procesos)

    valorfinal = sum(proceso['duracion'] for proceso in procesos)

    return tiempos_espera_por_proceso, promedio_tiempo_espera, tiempos_inicio, tiempos_duracion, valorfinal

def ejecutar_sjf():
    # Obtener la lista de procesos desde la entrada de texto
    entrada_procesos = entrada_procesos_texto.get("1.0", tk.END)
    lineas = entrada_procesos.strip().split("\n")
    
    procesos = []

    for linea in lineas:
        partes = linea.split(',')
        if len(partes) == 2:
            nombre = partes[0].strip()
            duracion = int(partes[1].strip())
            proceso = {'nombre': nombre, 'duracion': duracion}
            procesos.append(proceso)

    if not procesos:
        messagebox.showwarning("Advertencia", "Por favor, ingresa al menos un proceso.")
        return

    tiempos_espera, promedio_tiempo_espera, tiempos_inicio, tiempos_duracion, valorfinal = sjf(procesos)

    # Mostrar los resultados en una nueva ventana
    ventana_resultados = tk.Toplevel()
    ventana_resultados.title("Resultados SJF")

    etiqueta_resultados = tk.Label(ventana_resultados, text="Resultados SJF", font=('Arial', 16))
    etiqueta_resultados.pack(pady=10)

    # Mostrar los tiempos de espera, inicio y duración por proceso
    for proceso, tiempo_espera in tiempos_espera.items():
        etiqueta_proceso = tk.Label(ventana_resultados, text=f"{proceso}: Tiempo de Espera = {tiempo_espera}, Tiempo de Inicio = {tiempos_inicio[proceso]}, Duración = {tiempos_duracion[proceso]}", font=('Arial', 12))
        etiqueta_proceso.pack()

    etiqueta_promedio = tk.Label(ventana_resultados, text=f"Promedio Tiempo de Espera: {promedio_tiempo_espera}", font=('Arial', 12))
    etiqueta_promedio.pack(pady=10)

    etiqueta_valorfinal = tk.Label(ventana_resultados, text=f"Suma de Tiempos de Ráfaga: {valorfinal}", font=('Arial', 12))
    etiqueta_valorfinal.pack(pady=10)

    dibujar_barra_horizontal(valorfinal, tiempos_espera, tiempos_inicio, tiempos_duracion)

ventana_sjf = tk.Tk()
ventana_sjf.title("Ingreso de Procesos SJF")

instrucciones_sjf = tk.Label(ventana_sjf, text="Ingresa los procesos en el formato: nombre, duración\nEjemplo: P1, 10", font=('Arial', 12))
instrucciones_sjf.pack(pady=10)

entrada_procesos_texto = tk.Text(ventana_sjf, height=10, width=40, font=('Arial', 12))
entrada_procesos_texto.pack(pady=10)

# Botón para ejecutar el algoritmo SJF
btn_ejecutar_sjf = tk.Button(ventana_sjf, text="Ejecutar SJF", command=ejecutar_sjf, font=('Arial', 14))
btn_ejecutar_sjf.pack(pady=10)

ventana_sjf.mainloop()
