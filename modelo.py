 # Clases Cliente y Registro (lógica de negocio)
# modelo.py
import pandas as pd 
import json
import os
from datetime import datetime
from Estilo_excel import crear_excel_con_estilo 
from tkinter import filedialog

DATOS_DIR = "datos"
os.makedirs(DATOS_DIR, exist_ok=True)

class Registro:
    def __init__(self, tipo, descripcion, monto, categoria=None, fecha=None):
        self.tipo = tipo
        self.descripcion = descripcion
        self.monto = monto
        self.categoria = categoria
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "tipo": self.tipo,
            "descripcion": self.descripcion,
            "monto": self.monto,
            "categoria": self.categoria,
            "fecha": self.fecha
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["tipo"],
            data["descripcion"],
            data["monto"],
            data.get("categoria"),
            data["fecha"]
        )

class Cliente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.registros = []
        self.cargar_datos()

    def agregar_registro(self, registro):
        self.registros.append(registro)

    def obtener_saldo(self):
        ingresos = sum(r.monto for r in self.registros if r.tipo == "Ingreso")
        egresos = sum(r.monto for r in self.registros if r.tipo == "Egreso")
        return ingresos - egresos

    def obtener_registros(self):
        return self.registros

    def guardar_datos(self):
        ruta = os.path.join(DATOS_DIR, f"{self.nombre}.json")
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in self.registros], f, indent=4)

    def cargar_datos(self):
        ruta = os.path.join(DATOS_DIR, f"{self.nombre}.json")
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                self.registros = [Registro.from_dict(r) for r in json.load(f)]

    # Método exportar_excel en la clase Cliente
    def exportar_excel(self, ruta):
        ruta = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if ruta:
         crear_excel_con_estilo(self.registros, ruta)