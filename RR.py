import tkinter as tk
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Proceso:
    def __init__(self, nombre, rafaga):
        self.nombre = nombre
        self.rafaga = rafaga

class RoundRobin:
    def __init__(self, procesos, quantum):
        self.procesos = deque(procesos)
        self.quantum = quantum
        self.resultados = []

    def ejecutar(self):
        tiempo_actual = 0

        while self.procesos:
            proceso_actual = self.procesos.popleft()
            proceso_color = colores[proceso_actual.nombre]

            for _ in range(min(self.quantum, proceso_actual.rafaga)):
                self.resultados.append((tiempo_actual, proceso_actual.nombre))
                proceso_actual.rafaga -= 1
                tiempo_actual += 1

                if proceso_actual.rafaga == 0:
                    break

            if proceso_actual.rafaga > 0:
                self.procesos.append(proceso_actual)

def ejecutar_planificacion():
    global colores

    procesos_input = entry_procesos.get().split(';')
    procesos = []
    colores = {}
    
    for i, proceso_str in enumerate(procesos_input):
        nombre, rafaga = proceso_str.split(',')
        procesos.append(Proceso(nombre, int(rafaga)))
        colores[nombre] = colores_disponibles[i]

    quantum = int(entry_quantum.get())

    planificador = RoundRobin(procesos, quantum)
    planificador.ejecutar()

    # Crear y mostrar el gráfico
    crear_grafico(planificador.resultados)

def crear_grafico(resultados):
    fig, ax = plt.subplots()
    
    for tiempo, proceso in resultados:
        ax.barh(proceso, 1, left=tiempo, color=colores[proceso], edgecolor='black')

    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Proceso')
    ax.set_title('Planificación Round Robin')

    # Crear leyenda
    handles = [plt.Rectangle((0, 0), 1, 1, color=color, edgecolor='black') for color in colores_disponibles]
    labels = colores.keys()
    ax.legend(handles, labels, loc='upper left', bbox_to_anchor=(1, 1))

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

    # Mostrar resultados en el área de texto
    resultado_text.delete(1.0, tk.END)
    for tiempo, proceso in resultados:
        resultado_text.insert(tk.END, f'Segundo {tiempo} a segundo {tiempo + 1}={proceso}\n')

root = tk.Tk()
root.title("Planificador Round Robin")

label_procesos = tk.Label(root, text="Ingrese procesos (nombre, ráfagas separados por ;):")
entry_procesos = tk.Entry(root)
label_quantum = tk.Label(root, text="Ingrese quantum:")
entry_quantum = tk.Entry(root)

label_procesos.pack(pady=5)
entry_procesos.pack(pady=5)
label_quantum.pack(pady=5)
entry_quantum.pack(pady=5)

button_ejecutar = tk.Button(root, text="Ejecutar Planificación", command=ejecutar_planificacion)
button_ejecutar.pack(pady=10)
colores_disponibles = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']

# Resultado de la planificación
resultado_text = tk.Text(root, height=15, width=40)
resultado_text.pack(pady=10)

root.mainloop()
