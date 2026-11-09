"""Interfaz gráfica didáctica para visualizar y manipular un ABB."""

import json
import random
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

from arbol_binario import Arbol, Nodo


class AplicacionArbol(tk.Tk):
    """Ventana principal del visualizador de árboles binarios."""

    EJEMPLO = [50, 30, 70, 20, 40, 60, 80]

    def __init__(self):
        super().__init__()
        self.title("Árbol binario de búsqueda | Laboratorio visual")
        self.geometry("1120x760")
        self.minsize(900, 620)
        self.configure(bg="#F2F5FA")

        self.arbol = Arbol()
        self.valor_var = tk.StringVar()
        self.estado_var = tk.StringVar(value="Listo. Inserta un número o carga el ejemplo.")
        self.resultado_var = tk.StringVar(value="Los recorridos aparecerán aquí.")
        self.tipo_recorrido_var = tk.StringVar(value="Inorden")
        self._valor_encontrado = None
        self._valor_activo = None
        self._pasos_recorrido = []
        self._indice_recorrido = 0
        self._trabajo_animacion = None

        self._configurar_estilos()
        self._crear_interfaz()
        self.protocol("WM_DELETE_WINDOW", self._cerrar)
        self._actualizar_vista()

    def _configurar_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("TFrame", background="#F2F5FA")
        estilo.configure("Card.TFrame", background="#FFFFFF")
        estilo.configure(
            "TLabel", background="#FFFFFF", foreground="#1B2940", font=("Segoe UI", 10)
        )
        estilo.configure(
            "Muted.TLabel", background="#FFFFFF", foreground="#68778D", font=("Segoe UI", 9)
        )
        estilo.configure(
            "Title.TLabel", background="#F2F5FA", foreground="#18263D",
            font=("Segoe UI", 21, "bold")
        )
        estilo.configure(
            "Subtitle.TLabel", background="#F2F5FA", foreground="#64748B",
            font=("Segoe UI", 10)
        )
        estilo.configure("Section.TLabel", font=("Segoe UI", 11, "bold"))
        estilo.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=(10, 8))
        estilo.map(
            "Primary.TButton",
            background=[("active", "#1D4ED8"), ("!disabled", "#2563EB")],
            foreground=[("!disabled", "#FFFFFF")],
        )
        estilo.configure("TButton", font=("Segoe UI", 9), padding=(8, 6))
        estilo.configure("TEntry", padding=7)
        estilo.configure("TCombobox", padding=5)

    def _crear_interfaz(self):
        encabezado = ttk.Frame(self, padding=(24, 18, 24, 10))
        encabezado.grid(row=0, column=0, sticky="ew")
        encabezado.columnconfigure(0, weight=1)
        ttk.Label(encabezado, text="Árbol binario de búsqueda", style="Title.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            encabezado,
            text="Construye, explora y comprende cómo se organiza cada nodo.",
            style="Subtitle.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(3, 0))
        ttk.Label(
            encabezado, text="ESTRUCTURAS DE DATOS  ·  PYTHON", style="Subtitle.TLabel"
        ).grid(row=0, column=1, rowspan=2, sticky="e", padx=(12, 0))

        contenido = ttk.Frame(self, padding=(24, 8, 24, 18))
        contenido.grid(row=1, column=0, sticky="nsew")
        contenido.columnconfigure(0, weight=0, minsize=280)
        contenido.columnconfigure(1, weight=1)
        contenido.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        panel_contenedor = ttk.Frame(contenido, style="Card.TFrame")
        panel_contenedor.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        panel_contenedor.columnconfigure(0, weight=1)
        panel_contenedor.rowconfigure(0, weight=1)
        panel_canvas = tk.Canvas(
            panel_contenedor, width=280, bg="#FFFFFF", highlightthickness=0
        )
        panel_scroll = ttk.Scrollbar(
            panel_contenedor, orient="vertical", command=panel_canvas.yview
        )
        panel_canvas.configure(yscrollcommand=panel_scroll.set)
        panel_canvas.grid(row=0, column=0, sticky="nsew")
        panel_scroll.grid(row=0, column=1, sticky="ns")
        panel = ttk.Frame(panel_canvas, style="Card.TFrame", padding=16)
        ventana_panel = panel_canvas.create_window((0, 0), window=panel, anchor="nw")
        panel.columnconfigure(0, weight=1)
        panel.bind(
            "<Configure>",
            lambda _evento: panel_canvas.configure(scrollregion=panel_canvas.bbox("all")),
        )
        panel_canvas.bind(
            "<Configure>",
            lambda evento: panel_canvas.itemconfigure(ventana_panel, width=evento.width),
        )
        self._crear_panel(panel)

        visual = ttk.Frame(contenido, style="Card.TFrame", padding=14)
        visual.grid(row=0, column=1, sticky="nsew")
        visual.columnconfigure(0, weight=1)
        visual.rowconfigure(1, weight=1)
        self._crear_visualizacion(visual)

        barra_estado = ttk.Frame(self, padding=(24, 0, 24, 12))
        barra_estado.grid(row=2, column=0, sticky="ew")
        ttk.Label(barra_estado, textvariable=self.estado_var, style="Subtitle.TLabel").pack(
            side="left"
        )

    def _crear_panel(self, panel):
        ttk.Label(panel, text="Operaciones", style="Section.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(panel, text="Valor entero", style="Muted.TLabel").grid(
            row=1, column=0, sticky="w", pady=(13, 4)
        )
        entrada = ttk.Entry(panel, textvariable=self.valor_var, font=("Segoe UI", 12))
        entrada.grid(row=2, column=0, sticky="ew")
        entrada.bind("<Return>", lambda _evento: self.insertar())
        self.entrada = entrada

        acciones = ttk.Frame(panel, style="Card.TFrame")
        acciones.grid(row=3, column=0, sticky="ew", pady=(8, 16))
        acciones.columnconfigure(0, weight=1)
        acciones.columnconfigure(1, weight=1)
        ttk.Button(
            acciones, text="＋ Insertar", style="Primary.TButton", command=self.insertar
        ).grid(row=0, column=0, sticky="ew", padx=(0, 4), pady=3)
        ttk.Button(acciones, text="⌕ Buscar", command=self.buscar).grid(
            row=0, column=1, sticky="ew", padx=(4, 0), pady=3
        )
        ttk.Button(acciones, text="− Eliminar", command=self.eliminar).grid(
            row=1, column=0, columnspan=2, sticky="ew", pady=3
        )

        ttk.Separator(panel).grid(row=4, column=0, sticky="ew", pady=12)
        ttk.Label(panel, text="Recorrido paso a paso", style="Section.TLabel").grid(
            row=5, column=0, sticky="w"
        )
        self.selector_recorrido = ttk.Combobox(
            panel,
            textvariable=self.tipo_recorrido_var,
            values=("Inorden", "Preorden", "Postorden", "Por niveles"),
            state="readonly",
        )
        self.selector_recorrido.grid(row=6, column=0, sticky="ew", pady=(8, 5))
        ttk.Button(
            panel, text="▶  Animar recorrido", style="Primary.TButton", command=self.animar_recorrido
        ).grid(row=7, column=0, sticky="ew")
        ttk.Label(
            panel,
            text="Inorden visita izquierda, raíz y derecha; en un ABB produce los valores ordenados.",
            style="Muted.TLabel",
            wraplength=240,
            justify="left",
        ).grid(row=8, column=0, sticky="w", pady=(7, 2))

        ttk.Separator(panel).grid(row=9, column=0, sticky="ew", pady=12)
        ttk.Label(panel, text="Herramientas", style="Section.TLabel").grid(
            row=10, column=0, sticky="w"
        )
        herramientas = ttk.Frame(panel, style="Card.TFrame")
        herramientas.grid(row=11, column=0, sticky="ew", pady=(6, 0))
        herramientas.columnconfigure(0, weight=1)
        herramientas.columnconfigure(1, weight=1)
        ttk.Button(herramientas, text="Cargar ejemplo", command=self.cargar_ejemplo).grid(
            row=0, column=0, columnspan=2, sticky="ew", pady=3
        )
        ttk.Button(herramientas, text="Árbol aleatorio", command=self.crear_aleatorio).grid(
            row=1, column=0, columnspan=2, sticky="ew", pady=3
        )
        ttk.Button(herramientas, text="Abrir JSON", command=self.abrir_json).grid(
            row=2, column=0, sticky="ew", padx=(0, 4), pady=3
        )
        ttk.Button(herramientas, text="Guardar", command=self.guardar_json).grid(
            row=2, column=1, sticky="ew", padx=(4, 0), pady=3
        )
        ttk.Button(herramientas, text="Vaciar árbol", command=self.vaciar).grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=3
        )

        ttk.Separator(panel).grid(row=12, column=0, sticky="ew", pady=12)
        ttk.Label(panel, text="Resumen", style="Section.TLabel").grid(
            row=13, column=0, sticky="w"
        )
        resumen = ttk.Frame(panel, style="Card.TFrame")
        resumen.grid(row=14, column=0, sticky="ew", pady=(7, 0))
        resumen.columnconfigure(0, weight=1)
        resumen.columnconfigure(1, weight=1)
        self.estadisticas = {}
        for indice, (clave, titulo) in enumerate(
            (("nodos", "Nodos"), ("altura", "Altura"), ("hojas", "Hojas"), ("extremos", "Mín. / Máx."))
        ):
            fila, columna = divmod(indice, 2)
            tarjeta = ttk.Frame(resumen, style="Card.TFrame", padding=(5, 5))
            tarjeta.grid(row=fila, column=columna, sticky="ew", padx=2, pady=2)
            ttk.Label(tarjeta, text=titulo, style="Muted.TLabel").pack(anchor="w")
            valor = ttk.Label(tarjeta, text="0", font=("Segoe UI", 14, "bold"))
            valor.pack(anchor="w")
            self.estadisticas[clave] = valor

    def _crear_visualizacion(self, visual):
        encabezado = ttk.Frame(visual, style="Card.TFrame")
        encabezado.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        encabezado.columnconfigure(0, weight=1)
        ttk.Label(encabezado, text="Visualización", style="Section.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            encabezado, text="Cada círculo es un objeto Nodo", style="Muted.TLabel"
        ).grid(row=0, column=1, sticky="e")

        area = ttk.Frame(visual, style="Card.TFrame")
        area.grid(row=1, column=0, sticky="nsew")
        area.columnconfigure(0, weight=1)
        area.rowconfigure(0, weight=1)
        self.canvas = tk.Canvas(
            area, bg="#FBFCFE", highlightthickness=0, relief="flat",
        )
        barra_y = ttk.Scrollbar(area, orient="vertical", command=self.canvas.yview)
        barra_x = ttk.Scrollbar(area, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=barra_x.set, yscrollcommand=barra_y.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        barra_y.grid(row=0, column=1, sticky="ns")
        barra_x.grid(row=1, column=0, sticky="ew")

        pie = ttk.Frame(visual, style="Card.TFrame", padding=(2, 10, 2, 0))
        pie.grid(row=2, column=0, sticky="ew")
        pie.columnconfigure(0, weight=1)
        ttk.Label(pie, text="Salida del recorrido", style="Section.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            pie, textvariable=self.resultado_var, style="Muted.TLabel", wraplength=680
        ).grid(row=1, column=0, sticky="w", pady=(3, 0))

    def _leer_valor(self):
        texto = self.valor_var.get().strip()
        try:
            return int(texto)
        except ValueError:
            messagebox.showwarning("Dato no válido", "Escribe un número entero, por ejemplo 42.")
            self.entrada.focus_set()
            return None

    def _detener_animacion(self):
        if self._trabajo_animacion is not None:
            try:
                self.after_cancel(self._trabajo_animacion)
            except tk.TclError:
                pass
        self._trabajo_animacion = None
        self._valor_activo = None

    def insertar(self):
        valor = self._leer_valor()
        if valor is None:
            return
        self._detener_animacion()
        self._valor_encontrado = None
        if self.arbol.insertar(valor):
            mensaje = f"Se insertó {valor}. Menores a la izquierda; mayores a la derecha."
            self.resultado_var.set(f"Insertado: {valor}")
        else:
            mensaje = f"El valor {valor} ya existe; el ABB no admite duplicados."
            self.resultado_var.set(f"Sin cambios: {valor} ya estaba en el árbol.")
        self.estado_var.set(mensaje)
        self._actualizar_vista()
        self.valor_var.set("")
        self.entrada.focus_set()

    def buscar(self):
        valor = self._leer_valor()
        if valor is None:
            return
        self._detener_animacion()
        encontrado = self.arbol.buscar(valor)
        self._valor_encontrado = valor if encontrado else None
        self.estado_var.set(
            f"{valor} está en el árbol." if encontrado else f"No se encontró {valor}."
        )
        self.resultado_var.set(
            f"Búsqueda: {valor} encontrado." if encontrado else f"Búsqueda: {valor} no encontrado."
        )
        self._dibujar_arbol()

    def eliminar(self):
        valor = self._leer_valor()
        if valor is None:
            return
        self._detener_animacion()
        self._valor_encontrado = None
        if self.arbol.eliminar(valor):
            mensaje = f"Se eliminó {valor}; el árbol conserva el orden del ABB."
            self.resultado_var.set(f"Eliminado: {valor}")
        else:
            mensaje = f"No se encontró {valor}; el árbol no cambió."
            self.resultado_var.set(f"No se pudo eliminar {valor} porque no existe.")
        self.estado_var.set(mensaje)
        self._actualizar_vista()
        self.valor_var.set("")
        self.entrada.focus_set()

    def animar_recorrido(self):
        self._detener_animacion()
        if self.arbol.es_vacio():
            self.estado_var.set("El árbol está vacío; no hay nodos para recorrer.")
            return
        metodos = {
            "Inorden": (self.arbol.inorden, "Izquierda → raíz → derecha"),
            "Preorden": (self.arbol.preorden, "Raíz → izquierda → derecha"),
            "Postorden": (self.arbol.postorden, "Izquierda → derecha → raíz"),
            "Por niveles": (self.arbol.recorrido_por_niveles, "De arriba hacia abajo, por nivel"),
        }
        metodo, explicacion = metodos[self.tipo_recorrido_var.get()]
        self._pasos_recorrido = metodo()
        self._indice_recorrido = 0
        self._valor_encontrado = None
        self.estado_var.set(f"Recorrido {self.tipo_recorrido_var.get()}: {explicacion}.")
        self.resultado_var.set("Orden visitado: ")
        self._paso_animacion()

    def _paso_animacion(self):
        if self._indice_recorrido >= len(self._pasos_recorrido):
            self._valor_activo = None
            self.resultado_var.set(
                "Resultado: " + " → ".join(map(str, self._pasos_recorrido))
            )
            self._trabajo_animacion = None
            self._dibujar_arbol()
            return
        valor = self._pasos_recorrido[self._indice_recorrido]
        self._valor_activo = valor
        visitados = self._pasos_recorrido[: self._indice_recorrido + 1]
        self.resultado_var.set("Visitando: " + " → ".join(map(str, visitados)))
        self._indice_recorrido += 1
        self._dibujar_arbol()
        self._trabajo_animacion = self.after(550, self._paso_animacion)

    def _confirmar_reemplazo(self):
        if self.arbol.es_vacio():
            return True
        return messagebox.askyesno(
            "Reemplazar árbol", "Esta acción reemplazará los nodos actuales. ¿Continuar?"
        )

    def _reemplazar_valores(self, valores, mensaje):
        temporal = Arbol()
        for valor in valores:
            if not temporal.insertar(valor):
                raise ValueError(f"El archivo contiene el valor duplicado {valor}.")
        self._detener_animacion()
        self.arbol = temporal
        self._valor_encontrado = None
        self.valor_var.set("")
        self.resultado_var.set("Árbol actualizado.")
        self.estado_var.set(mensaje)
        self._actualizar_vista()

    def cargar_ejemplo(self):
        if not self._confirmar_reemplazo():
            return
        self._reemplazar_valores(
            self.EJEMPLO, "Ejemplo cargado: inserta los números en el orden mostrado."
        )

    def crear_aleatorio(self):
        cantidad = simpledialog.askinteger(
            "Árbol aleatorio", "¿Cuántos nodos quieres? (1 a 15)",
            minvalue=1, maxvalue=15, parent=self,
        )
        if cantidad is None:
            return
        if not self._confirmar_reemplazo():
            return
        valores = random.sample(range(1, 100), cantidad)
        self._reemplazar_valores(valores, f"Árbol aleatorio creado con {cantidad} nodos.")

    def vaciar(self):
        if self.arbol.es_vacio():
            self.estado_var.set("El árbol ya está vacío.")
            return
        if not messagebox.askyesno("Vaciar árbol", "¿Eliminar todos los nodos?"):
            return
        self._detener_animacion()
        self.arbol.limpiar()
        self._valor_encontrado = None
        self.resultado_var.set("Árbol vacío.")
        self.estado_var.set("Se eliminaron todos los nodos.")
        self._actualizar_vista()

    def guardar_json(self):
        ruta = filedialog.asksaveasfilename(
            title="Guardar árbol", defaultextension=".json",
            filetypes=(("Archivo JSON", "*.json"), ("Todos los archivos", "*.*")),
        )
        if not ruta:
            return
        datos = {
            "tipo": "árbol binario de búsqueda",
            "version": 1,
            "valores_por_niveles": self.arbol.recorrido_por_niveles(),
        }
        try:
            with open(ruta, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=2)
        except OSError as error:
            messagebox.showerror("No se pudo guardar", str(error))
            return
        self.estado_var.set(f"Árbol guardado en {ruta}.")

    def abrir_json(self):
        ruta = filedialog.askopenfilename(
            title="Abrir árbol", filetypes=(("Archivo JSON", "*.json"), ("Todos los archivos", "*.*"))
        )
        if not ruta:
            return
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            valores = datos["valores_por_niveles"]
            if not isinstance(valores, list) or any(
                isinstance(valor, bool) or not isinstance(valor, int) for valor in valores
            ):
                raise ValueError("La lista 'valores_por_niveles' debe contener solo enteros.")
            temporal = Arbol()
            for valor in valores:
                if not temporal.insertar(valor):
                    raise ValueError(f"El archivo contiene el valor duplicado {valor}.")
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            messagebox.showerror("Archivo no válido", f"No se pudo abrir el árbol:\n{error}")
            return
        if not self._confirmar_reemplazo():
            return
        self._reemplazar_valores(valores, f"Árbol abierto desde {ruta}.")

    def _actualizar_vista(self):
        total = self.arbol.contar_nodos()
        minimo = self.arbol.obtener_minimo()
        maximo = self.arbol.obtener_maximo()
        self.estadisticas["nodos"].configure(text=str(total))
        self.estadisticas["altura"].configure(text=str(self.arbol.altura()))
        self.estadisticas["hojas"].configure(text=str(self.arbol.contar_hojas()))
        extremos = f"{minimo} / {maximo}" if total else "— / —"
        self.estadisticas["extremos"].configure(text=extremos)
        self._dibujar_arbol()

    def _dibujar_arbol(self):
        self.canvas.delete("all")
        if self.arbol.es_vacio():
            self.canvas.configure(scrollregion=(0, 0, 650, 420))
            self.canvas.create_text(
                325, 195, text="🌱  Árbol vacío\nInserta un número para crear la raíz.",
                fill="#64748B", font=("Segoe UI", 15), justify="center", tags="empty",
            )
            return

        coordenadas = {}
        indice = 0

        def ubicar(nodo: Nodo, profundidad: int):
            nonlocal indice
            if nodo is None:
                return
            ubicar(nodo.izquierda, profundidad + 1)
            coordenadas[id(nodo)] = (62 + indice * 92, 54 + profundidad * 96)
            indice += 1
            ubicar(nodo.derecha, profundidad + 1)

        ubicar(self.arbol.raiz, 0)
        ancho = max(620, 124 + max(0, indice - 1) * 92)
        alto = max(410, 110 + max(0, self.arbol.altura() - 1) * 96)
        self.canvas.configure(scrollregion=(0, 0, ancho, alto))

        def dibujar_conexiones(nodo: Nodo):
            if nodo is None:
                return
            x, y = coordenadas[id(nodo)]
            for hijo in (nodo.izquierda, nodo.derecha):
                if hijo is not None:
                    hx, hy = coordenadas[id(hijo)]
                    self.canvas.create_line(
                        x, y + 23, hx, hy - 23, fill="#A9B7C9", width=2,
                        arrow="last", arrowshape=(7, 8, 3),
                    )
                    dibujar_conexiones(hijo)

        dibujar_conexiones(self.arbol.raiz)

        def dibujar_nodos(nodo: Nodo):
            if nodo is None:
                return
            x, y = coordenadas[id(nodo)]
            if nodo.valor == self._valor_activo:
                relleno, borde = "#F4B942", "#D58B0B"
            elif nodo.valor == self._valor_encontrado:
                relleno, borde = "#47B881", "#21865A"
            else:
                relleno, borde = "#FFFFFF", "#3675D4"
            radio = 25
            self.canvas.create_oval(
                x - radio, y - radio, x + radio, y + radio,
                fill=relleno, outline=borde, width=2,
            )
            color_texto = "#FFFFFF" if nodo.valor in (self._valor_activo, self._valor_encontrado) else "#183153"
            self.canvas.create_text(
                x, y, text=str(nodo.valor), fill=color_texto,
                font=("Segoe UI", 10, "bold"),
            )
            dibujar_nodos(nodo.izquierda)
            dibujar_nodos(nodo.derecha)

        dibujar_nodos(self.arbol.raiz)

    def _cerrar(self):
        self._detener_animacion()
        self.destroy()


if __name__ == "__main__":
    AplicacionArbol().mainloop()
