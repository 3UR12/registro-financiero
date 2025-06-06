#Interfaz gráfica con Tkinter y ttkbootstrap
# interfaz.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import ttkbootstrap as tb

from modelo import Cliente, Registro
from utils import exportar_pdf, exportar_csv, generar_grafico

class Interfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Gastos")
        self.cliente = None

        self.style = tb.Style("superhero")  # Puedes usar otros temas como "flatly", "cosmo", etc.
        self.root.geometry("800x600")

        self.crear_widgets()

    def crear_widgets(self):
        self.frame_superior = ttk.Frame(self.root, padding=10)
        self.frame_superior.pack(fill="x")

        ttk.Label(self.frame_superior, text="Nombre del cliente:").pack(side="left")
        self.nombre_entry = ttk.Entry(self.frame_superior)
        self.nombre_entry.pack(side="left", padx=5)
        ttk.Button(self.frame_superior, text="Cargar cliente", command=self.cargar_cliente).pack(side="left", padx=5)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        self.tab_registro = ttk.Frame(self.notebook)
        self.tab_grafico = ttk.Frame(self.notebook)
        self.tab_exportar = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_registro, text="Registrar")
        self.notebook.add(self.tab_grafico, text="Gráfico")
        self.notebook.add(self.tab_exportar, text="Exportar")

        self.construir_tab_registro()
        self.construir_tab_grafico()
        self.construir_tab_exportar()

    def construir_tab_registro(self):
        frame = self.tab_registro
        campos = ttk.Frame(frame, padding=10)
        campos.pack()

        self.tipo = tb.StringVar(value="Ingreso")
        self.descripcion = tk.StringVar()
        self.monto = tk.DoubleVar()
        self.categoria = tk.StringVar()

        ttk.Label(campos, text="Tipo:").grid(row=0, column=0, sticky="e")
        ttk.Combobox(campos, textvariable=self.tipo, values=["Ingreso", "Egreso"]).grid(row=0, column=1)

        ttk.Label(campos, text="Descripción:").grid(row=1, column=0, sticky="e")
        ttk.Entry(campos, textvariable=self.descripcion).grid(row=1, column=1)

        ttk.Label(campos, text="Monto:").grid(row=2, column=0, sticky="e")
        ttk.Entry(campos, textvariable=self.monto).grid(row=2, column=1)

        ttk.Label(campos, text="Categoría:").grid(row=3, column=0, sticky="e")
        self.categoria_cb = ttk.Combobox(
            campos,
            textvariable=self.categoria,
            values=["General", "Efectivo", "Pagos", "Servicios", "Alimentos", "Transporte"],
            state="normal"
        )    
        self.categoria_cb.grid(row=3, column=1)
        self.categoria_cb.set("General")


        ttk.Button(campos, text="Registrar", command=self.registrar).grid(row=4, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(frame, columns=("tipo", "descripcion", "monto", "categoria", "fecha"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=120)
        self.tree.pack(pady=10, expand=True, fill="both")
        ttk.Button(frame, text="Eliminar registro seleccionado", command=self.eliminar_registro).pack(pady=5)

        self.saldo_label = ttk.Label(frame, text="Saldo actual: $0.00", font=("Arial", 12, "bold"))
        self.saldo_label.pack(pady=5)

    def construir_tab_grafico(self):
        self.canvas_frame = ttk.Frame(self.tab_grafico)
        self.canvas_frame.pack(expand=True, fill="both", padx=20, pady=20)

        ttk.Button(self.tab_grafico, text="Actualizar gráfico", command=self.mostrar_grafico).pack(pady=10)

        # Reemplazar la sección de botones de exportación en la interfaz gráfica
    def construir_tab_exportar(self):
        frame = self.tab_exportar
        exportar_menu = ttk.Menubutton(frame, text="Exportar", bootstyle="primary")
        menu = tk.Menu(exportar_menu, tearoff=0)
        menu.add_command(label="CSV (ligero)", command=lambda: exportar_csv(self.cliente))
        menu.add_command(label="Excel (.xlsx)", command=lambda: self.exportar_excel())
        menu.add_command(label="PDF", command=lambda: exportar_pdf(self.cliente))
        exportar_menu["menu"] = menu
        exportar_menu.pack(pady=5)

    def cargar_cliente(self):
        nombre = self.nombre_entry.get().strip()
        if not nombre:
            messagebox.showwarning("Aviso", "Debe ingresar un nombre.")
            return
        self.cliente = Cliente(nombre)
        self.actualizar_tabla()

    def registrar(self):
        if not self.cliente:
            messagebox.showwarning("Aviso", "Primero debe cargar un cliente.")
            return

        try:
            r = Registro(
                self.tipo.get(),
                self.descripcion.get(),
                self.monto.get(),
                self.categoria.get()
            )
            self.cliente.agregar_registro(r)
            self.cliente.guardar_datos()
            self.actualizar_tabla()
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar_tabla(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for r in self.cliente.obtener_registros():
            self.tree.insert("", "end", values=(r.tipo, r.descripcion, f"${r.monto:.2f}", r.categoria, r.fecha))

        saldo = self.cliente.obtener_saldo()
        self.saldo_label.config(text=f"Saldo actual: ${saldo:.2f}")

    def limpiar_campos(self):
        self.descripcion.set("")
        self.monto.set(0.0)
        self.categoria.set("")

    def mostrar_grafico(self):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        generar_grafico(self.cliente, self.canvas_frame)

    def eliminar_registro(self):
        if not self.cliente:
            messagebox.showwarning("Aviso", "Primero debe cargar un cliente.")
            return

        item = self.tree.selection()
        if not item:
            messagebox.showinfo("Información", "Debe seleccionar un registro para eliminar.")
            return

        confirm = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este registro?")
        if confirm:
            index = self.tree.index(item)
            del self.cliente.registros[index]
            self.cliente.guardar_datos()
            self.actualizar_tabla()
    
    def exportar_excel(self):
        if not self.cliente:
            messagebox.showwarning("Advertencia", "Primero debes crear o cargar un cliente.")
            return

        archivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos Excel", "*.xlsx")])
        if archivo:
            self.cliente.exportar_excel(archivo)
            messagebox.showinfo("Éxito", f"Datos exportados a Excel en:\n{archivo}")
