import tkinter as tk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Clase Nodo que representa cada nodo del ABB con datos del estudiante
class Nodo:
    def __init__(self, id_estudiante, nombres, apellidos, edad, correo, telefono):
        self.id = id_estudiante
        self.nombres = nombres
        self.apellidos = apellidos
        self.edad = edad
        self.correo = correo
        self.telefono = telefono
        self.izquierda = None
        self.derecha = None

# Clase ArbolBinarioBusqueda implementa las funciones del ABB
class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    # Agregar un nuevo estudiante al ABB
    def agregar_estudiante(self, id_estudiante, nombres, apellidos, edad, correo, telefono):
        if not self.raiz:
            self.raiz = Nodo(id_estudiante, nombres, apellidos, edad, correo, telefono)
        else:
            self._agregar(self.raiz, id_estudiante, nombres, apellidos, edad, correo, telefono)

    # Función recursiva para agregar un nodo al ABB
    def _agregar(self, nodo_actual, id_estudiante, nombres, apellidos, edad, correo, telefono):
        if id_estudiante < nodo_actual.id:
            if nodo_actual.izquierda:
                self._agregar(nodo_actual.izquierda, id_estudiante, nombres, apellidos, edad, correo, telefono)
            else:
                nodo_actual.izquierda = Nodo(id_estudiante, nombres, apellidos, edad, correo, telefono)
        elif id_estudiante > nodo_actual.id:
            if nodo_actual.derecha:
                self._agregar(nodo_actual.derecha, id_estudiante, nombres, apellidos, edad, correo, telefono)
            else:
                nodo_actual.derecha = Nodo(id_estudiante, nombres, apellidos, edad, correo, telefono)

    # Buscar un estudiante en el ABB
    def buscar_estudiante(self, id_estudiante):
        return self._buscar(self.raiz, id_estudiante)

    # Función recursiva para buscar un nodo en el ABB
    def _buscar(self, nodo_actual, id_estudiante):
        if nodo_actual is None or nodo_actual.id == id_estudiante:
            return nodo_actual
        if id_estudiante < nodo_actual.id:
            return self._buscar(nodo_actual.izquierda, id_estudiante)
        return self._buscar(nodo_actual.derecha, id_estudiante)

    # Eliminar un estudiante del ABB
    def eliminar_estudiante(self, id_estudiante):
        self.raiz = self._eliminar(self.raiz, id_estudiante)

    # Función recursiva para eliminar un nodo del ABB
    def _eliminar(self, nodo_actual, id_estudiante):
        if nodo_actual is None:
            return nodo_actual
        if id_estudiante < nodo_actual.id:
            nodo_actual.izquierda = self._eliminar(nodo_actual.izquierda, id_estudiante)
        elif id_estudiante > nodo_actual.id:
            nodo_actual.derecha = self._eliminar(nodo_actual.derecha, id_estudiante)
        else:
            if nodo_actual.izquierda is None:
                return nodo_actual.derecha
            elif nodo_actual.derecha is None:
                return nodo_actual.izquierda
            temp = self._minValueNode(nodo_actual.derecha)
            nodo_actual.id = temp.id
            nodo_actual.nombres = temp.nombres
            nodo_actual.apellidos = temp.apellidos
            nodo_actual.edad = temp.edad
            nodo_actual.correo = temp.correo
            nodo_actual.telefono = temp.telefono
            nodo_actual.derecha = self._eliminar(nodo_actual.derecha, temp.id)
        return nodo_actual

    # Función para encontrar el nodo con el valor mínimo
    def _minValueNode(self, nodo):
        current = nodo
        while current.izquierda is not None:
            current = current.izquierda
        return current

    # Listar todos los estudiantes en orden ascendente
    def listar_estudiantes(self):
        resultado = []
        self._inOrden(self.raiz, resultado)
        return resultado

    # Función recursiva para realizar el recorrido in-order
    def _inOrden(self, nodo_actual, resultado):
        if nodo_actual:
            self._inOrden(nodo_actual.izquierda, resultado)
            resultado.append((nodo_actual.id, nodo_actual.nombres, nodo_actual.apellidos, nodo_actual.edad, nodo_actual.correo, nodo_actual.telefono))
            self._inOrden(nodo_actual.derecha, resultado)

    # Agregar estudiantes desde la entrada del usuario
    def agregar_estudiantes_desde_usuario(self):
        print("Ingrese los datos del estudiante:")
        id_estudiante = int(input("ID: "))
        nombres = input("Nombres: ")
        apellidos = input("Apellidos: ")
        edad = int(input("Edad: "))
        correo = input("Correo electrónico: ")
        telefono = input("Teléfono: ")
        self.agregar_estudiante(id_estudiante, nombres, apellidos, edad, correo, telefono)
        print(f"Estudiante {nombres} {apellidos} agregado correctamente.")

    # Exportar el listado de estudiantes a un archivo PDF
    def exportar_a_pdf(self, filename):
        estudiantes = self.listar_estudiantes()
        c = canvas.Canvas(filename, pagesize=letter)
        c.drawString(100, 800, "Listado de Estudiantes")
        y_position = 780
        for estudiante in estudiantes:
            c.drawString(100, y_position, f"ID: {estudiante[0]}, Nombres: {estudiante[1]}, Apellidos: {estudiante[2]}, Edad: {estudiante[3]}, Correo: {estudiante[4]}, Teléfono: {estudiante[5]}")
            y_position -= 20
        c.save()

# Clase para visualizar el ABB utilizando tkinter
class VisualizadorABB(tk.Tk):
    def __init__(self, arbol):
        super().__init__()
        self.title("Visualizador del ABB")
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack()
        self.arbol = arbol
        self.dibujar_arbol(self.arbol.raiz, 400, 30, 200)

    # Función recursiva para dibujar el ABB
    def dibujar_arbol(self, nodo, x, y, espacio):
        if nodo:
            texto = f"{nodo.id}\n{nodo.nombres}\n{nodo.apellidos}"
            self.canvas.create_text(x, y, text=texto, font=("Arial", 8, "bold"))
            if nodo.izquierda:
                self.canvas.create_line(x, y, x - espacio, y + 50)
                self.dibujar_arbol(nodo.izquierda, x - espacio, y + 50, espacio / 2)
            if nodo.derecha:
                self.canvas.create_line(x, y, x + espacio, y + 50)
                self.dibujar_arbol(nodo.derecha, x + espacio, y + 50, espacio / 2)

def agregar_estudiante_desde_interfaz():
    agregar_estudiante_window = tk.Toplevel()
    agregar_estudiante_window.title("Agregar Estudiante")

    id_label = tk.Label(agregar_estudiante_window, text="ID:")
    id_label.grid(row=0, column=0)
    id_entry = tk.Entry(agregar_estudiante_window)
    id_entry.grid(row=0, column=1)

    nombres_label = tk.Label(agregar_estudiante_window, text="Nombres:")
    nombres_label.grid(row=1, column=0)
    nombres_entry = tk.Entry(agregar_estudiante_window)
    nombres_entry.grid(row=1, column=1)

    apellidos_label = tk.Label(agregar_estudiante_window, text="Apellidos:")
    apellidos_label.grid(row=2, column=0)
    apellidos_entry = tk.Entry(agregar_estudiante_window)
    apellidos_entry.grid(row=2, column=1)

    edad_label = tk.Label(agregar_estudiante_window, text="Edad:")
    edad_label.grid(row=3, column=0)
    edad_entry = tk.Entry(agregar_estudiante_window)
    edad_entry.grid(row=3, column=1)

    correo_label = tk.Label(agregar_estudiante_window, text="Correo electrónico:")
    correo_label.grid(row=4, column=0)
    correo_entry = tk.Entry(agregar_estudiante_window)
    correo_entry.grid(row=4, column=1)

    telefono_label = tk.Label(agregar_estudiante_window, text="Teléfono:")
    telefono_label.grid(row=5, column=0)
    telefono_entry = tk.Entry(agregar_estudiante_window)
    telefono_entry.grid(row=5, column=1)

    def agregar():
        id_estudiante = int(id_entry.get())
        nombres = nombres_entry.get()
        apellidos = apellidos_entry.get()
        edad = int(edad_entry.get())
        correo = correo_entry.get()
        telefono = telefono_entry.get()
        abb.agregar_estudiante(id_estudiante, nombres, apellidos, edad, correo, telefono)
        agregar_estudiante_window.destroy()

    agregar_button = tk.Button(agregar_estudiante_window, text="Agregar", command=agregar)
    agregar_button.grid(row=6, columnspan=2)

def buscar_estudiante_por_id():
    buscar_id_window = tk.Toplevel()
    buscar_id_window.title("Buscar Estudiante por ID")

    id_label = tk.Label(buscar_id_window, text="ID:")
    id_label.grid(row=0, column=0)
    id_entry = tk.Entry(buscar_id_window)
    id_entry.grid(row=0, column=1)

    resultado_label = tk.Label(buscar_id_window, text="")
    resultado_label.grid(row=1, columnspan=2)

    def buscar():
        id_estudiante = int(id_entry.get())
        estudiante = abb.buscar_estudiante(id_estudiante)
        if estudiante:
            resultado_label.config(text=f"ID: {estudiante.id}, Nombres: {estudiante.nombres}, Apellidos: {estudiante.apellidos}, Edad: {estudiante.edad}, Correo: {estudiante.correo}, Teléfono: {estudiante.telefono}")
        else:
            resultado_label.config(text="Estudiante no encontrado.")

    buscar_button = tk.Button(buscar_id_window, text="Buscar", command=buscar)
    buscar_button.grid(row=2, columnspan=2)

def exportar_estudiantes_pdf():
    estudiantes = abb.listar_estudiantes()
    pdf_filename = "listado_estudiantes.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.drawString(100, 800, "Listado de Estudiantes")
    y_position = 780
    for estudiante in estudiantes:
        c.drawString(100, y_position, f"ID: {estudiante[0]}, Nombres: {estudiante[1]}, Apellidos: {estudiante[2]}, Edad: {estudiante[3]}, Correo: {estudiante[4]}, Teléfono: {estudiante[5]}")
        y_position -= 20
    c.save()
    print(f"El listado de estudiantes se ha exportado a {pdf_filename}")

abb = ArbolBinarioBusqueda()
estudiantes = [
    (45, "Juan", "Perez", 20, "juanperez12@gmail.com", "12345678"),
    (32, "Ana", "Gomez", 22, "anagomez34@hotmail.com", "87654321"),
    (60, "Luis", "Martinez", 21, "luismartinez56@gmail.com", "45678912"),
    (20, "Carlos", "Lopez", 23, "carloslopez78@hotmail.com", "78912345"),
    (38, "Maria", "Rodriguez", 19, "mariarodriguez90@gmail.com", "32165498"),
    (50, "Jose", "Fernandez", 24, "josefernandez11@hotmail.com", "65498732"),
    (70, "Laura", "Garcia", 22, "lauragarcia23@gmail.com", "15975348"),
]

for estudiante in estudiantes:
    abb.agregar_estudiante(*estudiante)

app = VisualizadorABB(abb)

agregar_button = tk.Button(app, text="Agregar Estudiante", command=agregar_estudiante_desde_interfaz)
agregar_button.pack()

buscar_button = tk.Button(app, text="Buscar Estudiante por ID", command=buscar_estudiante_por_id)
buscar_button.pack()

exportar_pdf_button = tk.Button(app, text="Exportar Listado a PDF", command=exportar_estudiantes_pdf)
exportar_pdf_button.pack()

app.mainloop()


