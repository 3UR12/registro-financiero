# Funciones auxiliares (PDF, CSV, gráficos)
# utils.py
import tkinter as tk
import csv
import os
from fpdf import FPDF
from tkinter import filedialog
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")
EXPORT_DIR = "exportaciones"
os.makedirs(EXPORT_DIR, exist_ok=True)

def exportar_csv(cliente):
    try:
        archivo = filedialog.asksaveasfilename(defaultextension=".csv", initialdir=EXPORT_DIR)
        if archivo:
            with open(archivo, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(["Tipo", "Descripción", "Monto", "Categoría", "Fecha"])
                for r in cliente.obtener_registros():
                    writer.writerow([r.tipo, r.descripcion, r.monto, r.categoria, r.fecha])
    except Exception as e:
        print(f"Error al exportar a CSV: {e}")

def exportar_pdf(cliente):
    try:
        archivo = filedialog.asksaveasfilename(defaultextension=".pdf", initialdir=EXPORT_DIR)
        if archivo:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, f"Registros de {cliente.nombre}", ln=True, align="C")
            for r in cliente.obtener_registros():
                pdf.cell(200, 10, f"{r.tipo} | {r.descripcion} | ${r.monto:.2f} | {r.categoria} | {r.fecha}", ln=True, border=1)
            pdf.output(archivo)
    except Exception as e:
        print(f"Error al exportar a PDF: {e}")

# utils.py
import tkinter as tk
import csv
import os
from fpdf import FPDF
from tkinter import filedialog
import matplotlib
matplotlib.use("Agg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

EXPORT_DIR = "exportaciones"
os.makedirs(EXPORT_DIR, exist_ok=True)

def exportar_csv(cliente):
    try:
        archivo = filedialog.asksaveasfilename(defaultextension=".csv", initialdir=EXPORT_DIR)
        if archivo:
            with open(archivo, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(["Tipo", "Descripción", "Monto", "Categoría", "Fecha"])
                for r in cliente.obtener_registros():
                    writer.writerow([r.tipo, r.descripcion, r.monto, r.categoria, r.fecha])
    except Exception as e:
        print(f"Error al exportar a CSV: {e}")

def exportar_pdf(cliente):
    try:
        archivo = filedialog.asksaveasfilename(defaultextension=".pdf", initialdir=EXPORT_DIR)
        if archivo:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, f"Registros de {cliente.nombre}", ln=True, align="C")
            for r in cliente.obtener_registros():
                pdf.cell(200, 10, f"{r.tipo} | {r.descripcion} | ${r.monto:.2f} | {r.categoria} | {r.fecha}", ln=True, border=1)
            pdf.output(archivo)
    except Exception as e:
        print(f"Error al exportar a PDF: {e}")

def generar_grafico(cliente, canvas_frame):
    try:
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure

        # Limpiar gráficos anteriores
        for widget in canvas_frame.winfo_children():
            widget.destroy()

        # Preparar datos
        ingresos = sum(r.monto for r in cliente.registros if r.tipo == "Ingreso")
        egresos = sum(r.monto for r in cliente.registros if r.tipo == "Egreso")

        categorias_ingreso = {}
        categorias_egreso = {}
        for r in cliente.registros:
            if r.tipo == "Ingreso":
                categorias_ingreso[r.categoria] = categorias_ingreso.get(r.categoria, 0) + r.monto
            elif r.tipo == "Egreso":
                categorias_egreso[r.categoria] = categorias_egreso.get(r.categoria, 0) + r.monto

        # Crear figura con 2 subgráficos
        fig = Figure(figsize=(10, 5), dpi=100)
        fig.subplots_adjust(bottom=0.25)  # Espacio para etiquetas inferiores

        # Gráfico 1: Pie chart general
        ax1 = fig.add_subplot(121)
        ax1.pie([ingresos, egresos], labels=["Ingresos", "Egresos"], autopct="%1.1f%%", colors=["#3CB371", "#FF6347"])
        ax1.set_title("Ingresos vs Egresos")

        # Gráfico 2: Barras por categoría
        ax2 = fig.add_subplot(122)
        labels = list(set(categorias_ingreso.keys()) | set(categorias_egreso.keys()))
        ingresos_cat = [categorias_ingreso.get(cat, 0) for cat in labels]
        egresos_cat = [categorias_egreso.get(cat, 0) for cat in labels]

        x = range(len(labels))
        ax2.bar(x, ingresos_cat, width=0.4, label="Ingresos", align='center', color="#3CB371")
        ax2.bar([i + 0.4 for i in x], egresos_cat, width=0.4, label="Egresos", align='center', color="#FF6347")
        ax2.set_xticks([i + 0.2 for i in x])
        ax2.set_xticklabels(labels, rotation=45, ha="right")
        ax2.tick_params(axis='x', labelsize=8)
        ax2.set_title("Categorías por tipo")
        ax2.legend()

        # Ajuste general de espacio entre subgráficos
        fig.tight_layout(pad=4)

        # Mostrar en interfaz
        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Botón para guardar gráfico
        def guardar_grafico():
            try:
                file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                         filetypes=[("Imagen PNG", "*.png"), ("PDF", "*.pdf")],
                                                         title="Guardar gráfico")
                if file_path:
                    fig.savefig(file_path)
            except Exception as e:
                print(f"Error al guardar gráfico: {e}")

        btn_guardar = tk.Button(canvas_frame, text="Guardar gráfico", command=guardar_grafico, bg="#4CAF50", fg="white")
        btn_guardar.pack(pady=5)

    except Exception as e:
        print(f"Error al generar gráfico: {e}")
