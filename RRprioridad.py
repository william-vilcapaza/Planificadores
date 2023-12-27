import tkinter as tk
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Proceso:
    def __init__(self, nombre, rafaga, prioridad):
        self.nombre = nombre
        self.rafaga = rafaga
        self.prioridad = prioridad
        self.tiempo_llegada = None
        self.tiempo_respuesta = None

class RoundRobinPrioridad:
    def __init__(self, procesos, quantum):
        self.procesos_por_prioridad = {}
        for proceso in procesos:
            if proceso.prioridad not in self.procesos_por_prioridad:
                self.procesos_por_prioridad[proceso.prioridad] = deque()
            self.procesos_por_prioridad[proceso.prioridad].append(proceso)

        self.quantum = quantum
        self.resultados = []

    def ejecutar(self):
        tiempo_actual = 0

        while self.procesos_por_prioridad:
            prioridades = sorted(self.procesos_por_prioridad.keys())
            for prioridad in prioridades:
                cola_prioridad = self.procesos_por_prioridad[prioridad]

                while cola_prioridad:
                    proceso_actual = cola_prioridad.popleft()
                    proceso_color = colores[proceso_actual.nombre]

                    if proceso_actual.tiempo_llegada is None:
                        proceso_actual.tiempo_llegada = tiempo_actual

                    for _ in range(min(self.quantum, proceso_actual.rafaga)):
                        self.resultados.append((tiempo_actual, proceso_actual.nombre))
                        proceso_actual.rafaga -= 1
                        tiempo_actual += 1

                    if proceso_actual.rafaga > 0:
                        cola_prioridad.append(proceso_actual)
                    else:
                        proceso_actual.tiempo_respuesta = tiempo_actual - proceso_actual.tiempo_llegada

            # Eliminar prioridades sin procesos
            prioridades_sin_procesos = [prioridad for prioridad, cola in self.procesos_por_prioridad.items() if not cola]
            for prioridad in prioridades_sin_procesos:
                del self.procesos_por_prioridad[prioridad]

def ejecutar_planificacion():
    global colores, procesos

    procesos_input = entry_procesos.get().split(';')
    procesos = []
    colores = {}

    for i, proceso_str in enumerate(procesos_input):
        nombre, rafaga, prioridad = proceso_str.split(',')
        procesos.append(Proceso(nombre, int(rafaga), int(prioridad)))
        colores[nombre] = colores_disponibles[i]

    quantum = int(entry_quantum.get())

    planificador = RoundRobinPrioridad(procesos, quantum)
    planificador.ejecutar()

    crear_grafico(planificador.resultados, procesos)

def crear_grafico(resultados, procesos):
    fig, ax = plt.subplots()

    for tiempo, proceso in resultados:
        ax.barh(proceso, 1, left=tiempo, color=colores[proceso], edgecolor='black')

    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Proceso')
    ax.set_title('Planificación Round Robin con Prioridad')

    handles = [plt.Rectangle((0, 0), 1, 1, color=color, edgecolor='black') for color in colores_disponibles]
    labels = colores.keys()
    ax.legend(handles, labels, loc='upper left', bbox_to_anchor=(1, 1))

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

    resultado_text.delete(1.0, tk.END)
    for tiempo, proceso in resultados:
        resultado_text.insert(tk.END, f'Segundo {tiempo} a segundo {tiempo + 1}={proceso}\n')

    resultado_text.insert(tk.END, '\nTiempo de Respuesta por Proceso:\n')
    for proceso_key in colores.keys():
        proceso_objeto = next((p for p in procesos if p.nombre == proceso_key), None)
        if proceso_objeto:
            tiempo_respuesta = proceso_objeto.tiempo_respuesta
            resultado_text.insert(tk.END, f'{proceso_key}: {tiempo_respuesta} segundos\n')

root = tk.Tk()
root.title("Planificador Round Robin con Prioridad")

label_procesos = tk.Label(root, text="Ingrese procesos (nombre, ráfagas, prioridad separados por ;):")
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
resultado_text = tk.Text(root, height=15, width=40)
resultado_text.pack(pady=10)

root.mainloop()
