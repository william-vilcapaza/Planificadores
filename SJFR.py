import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.lines import Line2D

def dibujar_barra_horizontal(resultados):
    # Crear la figura y el eje
    fig, ax = plt.subplots(figsize=(10, 5))

    # Colores para cada proceso
    colores = plt.cm.get_cmap('tab10', len(resultados))

    # Diccionario para mapear colores a procesos
    color_por_proceso = {proceso: colores(i) for i, (tiempo, proceso) in enumerate(resultados)}

    # Recorrer los resultados y dibujar barras
    for i, (tiempo, proceso) in enumerate(resultados):
        ax.add_line(Line2D([i, i+1], [0, 0], color=color_por_proceso[proceso], linewidth=10))

    # Configurar ejes y etiquetas
    ax.set_xlim(0, len(resultados) + 1)
    ax.set_xlabel('Tiempo')
    ax.set_yticks([])

    # Configurar los valores en el eje x de 1 en 1
    ax.set_xticks(np.arange(0, len(resultados) + 1, 1))
    ax.set_xticklabels([str(i) for i in range(len(resultados) + 1)])

    # Mostrar la leyenda
    handles = [Line2D([0], [0], color=color_por_proceso[proceso], label=proceso) for proceso in set(color_por_proceso.keys())]
    ax.legend(handles=handles, loc='upper left', bbox_to_anchor=(1, 1))

    # Mostrar la figura
    canvas = FigureCanvasTkAgg(fig, master=ventana_sjfr)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def planificar_sjfr(procesos):
    procesos.sort(key=lambda x: x['llegada'])
    resultado = []
    tiempo_actual = 0

    while procesos:
        procesos_en_espera = [proceso for proceso in procesos if proceso['llegada'] <= tiempo_actual]

        if procesos_en_espera:
            proceso_ejecutado = min(procesos_en_espera, key=lambda x: (x['duracion'], x['llegada']))
            resultado.append((tiempo_actual, proceso_ejecutado['nombre']))

            proceso_ejecutado['duracion'] -= 1

            if proceso_ejecutado['duracion'] == 0:
                procesos.remove(proceso_ejecutado)

        tiempo_actual += 1

    return resultado

def ejecutar_sjfr():
    # Obtener la lista de procesos desde la entrada de texto
    entrada_procesos = entrada_procesos_texto.get("1.0", tk.END)
    lineas = entrada_procesos.strip().split("\n")

    procesos = []
    for linea in lineas:
        partes = linea.split(',')
        if len(partes) == 3:
            nombre = partes[0].strip()
            duracion = int(partes[1].strip())
            llegada = int(partes[2].strip())
            proceso = {'nombre': nombre, 'duracion': duracion, 'llegada': llegada}
            procesos.append(proceso)

    # Verificar que se hayan ingresado procesos
    if not procesos:
        messagebox.showwarning("Advertencia", "Por favor, ingresa al menos un proceso.")
        return

    # Ejecutar el algoritmo SJFR y obtener resultados
    resultados = planificar_sjfr(procesos)

    # Mostrar los resultados en una nueva ventana
    ventana_resultados = tk.Toplevel()
    ventana_resultados.title("Resultados SJFR")

    etiqueta_resultados = tk.Label(ventana_resultados, text="Resultados SJFR", font=('Arial', 16))
    etiqueta_resultados.pack(pady=10)

    # Mostrar los resultados
    for i, (tiempo, proceso) in enumerate(resultados):
        etiqueta_proceso = tk.Label(ventana_resultados, text=f"segundo {i} a segundo {i + 1} = {proceso}", font=('Arial', 12))
        etiqueta_proceso.pack()

    # Dibujar la barra horizontal con leyenda
    dibujar_barra_horizontal(resultados)

# Crear la ventana de ingreso de procesos SJFR
ventana_sjfr = tk.Tk()
ventana_sjfr.title("Ingreso de Procesos SJFR")

# Crear etiqueta e instrucciones
instrucciones = tk.Label(ventana_sjfr, text="Ingresa los procesos en el formato: nombre, duración, llegada\nEjemplo: p1, 8, 0", font=('Arial', 12))
instrucciones.pack(pady=10)

# Crear entrada de texto para procesos
entrada_procesos_texto = tk.Text(ventana_sjfr, height=10, width=40, font=('Arial', 12))
entrada_procesos_texto.pack(pady=10)

# Botón para ejecutar el algoritmo SJFR
btn_ejecutar_sjfr = tk.Button(ventana_sjfr, text="Ejecutar SJFR", command=ejecutar_sjfr, font=('Arial', 14))
btn_ejecutar_sjfr.pack(pady=10)

# Ejecutar la aplicación
ventana_sjfr.mainloop()
