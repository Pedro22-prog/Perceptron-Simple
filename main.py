import numpy as np
from perceptron import Perceptron
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

class InterfazPerceptron:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.geometry("1000x800")
        self.ventana.title("Perceptrón - Tarea 1")

        self.crear_componentes()
        self.cargar_configuracion_inicial("inicio.txt")

    def crear_componentes(self):
        marco_controles = ttk.Frame(self.ventana)
        marco_controles.pack(pady=10, fill=X, padx=10)

        ttk.Label(marco_controles, text="Función de Activación:").pack(side=LEFT)
        self.variable_activacion = StringVar(value="escalon")
        self.selector_activacion = ttk.Combobox(marco_controles,
                                                textvariable=self.variable_activacion,
                                                values=["escalon", "sigmoide"],
                                                width=10,
                                                state="readonly")
        self.selector_activacion.pack(side=LEFT, padx=5)

        ttk.Label(marco_controles, text="Sesgo:").pack(side=LEFT, padx=5)
        self.campo_sesgo = ttk.Entry(marco_controles, width=10)
        self.campo_sesgo.pack(side=LEFT, padx=5)

        ttk.Button(marco_controles, text="Guardar", command=self.guardar_estado).pack(side=LEFT, padx=5)
        ttk.Button(marco_controles, text="Cargar", command=self.cargar_archivo).pack(side=LEFT, padx=5)
        ttk.Button(marco_controles, text="Calcular", command=self.calcular).pack(side=LEFT, padx=5)
        ttk.Button(marco_controles, text="Reiniciar", command=self.reiniciar).pack(side=LEFT, padx=5)

        marco_entradas = ttk.Frame(self.ventana)
        marco_entradas.pack(pady=10, fill=BOTH, expand=True, padx=10)

        ttk.Label(marco_entradas, text="Entradas (separadas por comas):").pack(anchor=W)
        self.campo_entradas = Text(marco_entradas, height=5, width=50)
        self.campo_entradas.pack(fill=X, pady=5)

        ttk.Label(marco_entradas, text="Pesos (separados por comas):").pack(anchor=W)
        self.campo_pesos = Text(marco_entradas, height=5, width=50)
        self.campo_pesos.pack(fill=X, pady=5)

        self.tabla_resultados = ttk.Treeview(self.ventana,
                                             columns=("Entradas", "Pesos", "Sesgo", "Salida"),
                                             show="headings",
                                             height=15)
        self.tabla_resultados.heading("Entradas", text="Entradas")
        self.tabla_resultados.heading("Pesos", text="Pesos")
        self.tabla_resultados.heading("Sesgo", text="Sesgo")
        self.tabla_resultados.heading("Salida", text="Salida")
        self.tabla_resultados.pack(fill=BOTH, expand=True, padx=10, pady=10)

    def validar_entradas(self, entradas, pesos):
        try:
            lista_entradas = [float(x.strip()) for x in entradas.split(',') if x.strip()]
            lista_pesos = [float(x.strip()) for x in pesos.split(',') if x.strip()]

            if not lista_entradas or not lista_pesos:
                raise ValueError("No se ingresaron valores")

            if len(lista_entradas) != len(lista_pesos):
                messagebox.showerror("Error",
                                     f"La cantidad de entradas ({len(lista_entradas)}) y pesos ({len(lista_pesos)}) no coinciden")
                return None, None

            return lista_entradas, lista_pesos

        except ValueError as e:
            messagebox.showerror("Error", f"Valores inválidos: {str(e)}")
            return None, None

    def cargar_configuracion_inicial(self, ruta_archivo):
        try:
            with open(ruta_archivo, 'r') as archivo:
                contenido = archivo.read().strip()

                if ',' in contenido and '\n' not in contenido:
                    valores = [x.strip() for x in contenido.split(',')]
                    if len(valores) < 1:
                        raise ValueError("Formato incorrecto: Debe incluir al menos el sesgo")

                    self.campo_sesgo.delete(0, END)
                    self.campo_sesgo.insert(0, valores[0])

                    if len(valores) > 1:
                        pesos = ','.join(valores[1:])
                        self.campo_pesos.delete(1.0, END)
                        self.campo_pesos.insert(END, pesos)

                    float(self.campo_sesgo.get())
                    [float(x) for x in self.campo_pesos.get(1.0, END).strip().split(',') if x.strip()]

                else:
                    lineas = contenido.split('\n')
                    if len(lineas) != 3:
                        raise ValueError("Formato incorrecto: Debe tener 3 líneas (sesgo, entradas, pesos)")

                    self.campo_sesgo.delete(0, END)
                    self.campo_sesgo.insert(0, lineas[0].strip())

                    self.campo_entradas.delete(1.0, END)
                    self.campo_entradas.insert(END, lineas[1].strip())

                    self.campo_pesos.delete(1.0, END)
                    self.campo_pesos.insert(END, lineas[2].strip())
                    float(self.campo_sesgo.get())
                    [float(x) for x in self.campo_entradas.get(1.0, END).strip().split(',') if x.strip()]
                    [float(x) for x in self.campo_pesos.get(1.0, END).strip().split(',') if x.strip()]

        except Exception as e:
            messagebox.showerror("Error", f"Error en formato del archivo:\n{str(e)}")

    def cargar_archivo(self):
        ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if ruta_archivo:
            self.cargar_configuracion_inicial(ruta_archivo)

    def guardar_estado(self):
        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt")]
        )
        if ruta_archivo:
            try:
                with open(ruta_archivo, 'w') as archivo:
                    archivo.write(f"{self.campo_sesgo.get()}\n")
                    archivo.write(f"{self.campo_entradas.get(1.0, END).strip()}\n")
                    archivo.write(f"{self.campo_pesos.get(1.0, END).strip()}\n")
                messagebox.showinfo("Éxito", "Configuración guardada correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")

    def calcular(self):
        try:
            entradas = self.campo_entradas.get(1.0, END).strip()
            pesos = self.campo_pesos.get(1.0, END).strip()
            sesgo = float(self.campo_sesgo.get())

            lista_entradas, lista_pesos = self.validar_entradas(entradas, pesos)
            if not lista_entradas or not lista_pesos:
                return

            perceptron = Perceptron(lista_entradas, lista_pesos, sesgo, self.variable_activacion.get())
            salida = perceptron.resultado()

            self.tabla_resultados.insert("", "end",
                                         values=(lista_entradas, lista_pesos, sesgo, salida))

        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {str(e)}")

    def reiniciar(self):
        self.campo_sesgo.delete(0, END)
        self.campo_entradas.delete(1.0, END)
        self.campo_pesos.delete(1.0, END)
        self.tabla_resultados.delete(*self.tabla_resultados.get_children())
        messagebox.showinfo("Reinicio", "Todos los campos han sido reiniciados")

if __name__ == "__main__":
    ventana_principal = Tk()
    aplicacion = InterfazPerceptron(ventana_principal)
    ventana_principal.mainloop()