import os
import pandas as pd
import tkinter as tk
from tkinter import simpledialog, messagebox

# Crear ventana oculta para los diálogos
root = tk.Tk()
root.withdraw()

# Función para pedir una distancia y validarla
def pedir_distancia(etiqueta):
    while True:
        try:
            valor = simpledialog.askstring("Entrada", f"Introduce la distancia {etiqueta} (en metros):")
            if valor is None:
                raise TypeError
            distancia = float(valor)
            if distancia <= 0:
                raise ValueError
            return distancia
        except (TypeError, ValueError):
            messagebox.showerror("Error", f"Introduce un número válido y positivo para la distancia {etiqueta}.")

# Pedir distancias para las 4 paredes
d_pared1 = pedir_distancia("a la PARED 1")
d_pared2 = pedir_distancia("a la PARED 2")
d_pared3 = pedir_distancia("a la PARED 3")
d_pared4 = pedir_distancia("a la PARED 4")

# Pedir distancias para techo y suelo
d_techo = pedir_distancia("al TECHO")
d_suelo = pedir_distancia("al SUELO")

# Borrar archivos antiguos si existen
archivos_a_borrar = ["resultados_kap.csv", "analisis_por_tension.csv"]
for archivo in archivos_a_borrar:
    if os.path.exists(archivo):
        os.remove(archivo)

# Cargar datos del archivo CSV
df = pd.read_csv("input.csv", sep=";", encoding="utf-8")

# Calcular KAP anual por tipo de exploración
df["KAP anual (Gy.cm^2)"] = df["KAP (Gy.cm^2)"] * df["numero de exploraciones anuales"]
df[["Tipo de exploración", "KAP anual (Gy.cm^2)"]].to_csv("resultados_kap.csv", sep=";", index=False, encoding="utf-8")

# Agrupar por tensión y sumar KAP anual
kap_por_tension = df.groupby("Tensión (kV)")["KAP anual (Gy.cm^2)"].sum().reset_index()

# Calcular Smax para pared, techo y suelo
kap_por_tension["Smax_pared (μGy/Gy.cm^2)"] = 0.031 * kap_por_tension["Tensión (kV)"] + 2.5
kap_por_tension["Smax_techo (μGy/Gy.cm^2)"] = 0.058 * kap_por_tension["Tensión (kV)"] + 4.8
kap_por_tension["Smax_suelo (μGy/Gy.cm^2)"] = 0.011 * kap_por_tension["Tensión (kV)"] + 0.9

# Calcular kerma dispersa máximo
kap_por_tension["Kerma_max_pared (μGy/año)"] = kap_por_tension["Smax_pared (μGy/Gy.cm^2)"] * kap_por_tension["KAP anual (Gy.cm^2)"]
kap_por_tension["Kerma_max_techo (μGy/año)"] = kap_por_tension["Smax_techo (μGy/Gy.cm^2)"] * kap_por_tension["KAP anual (Gy.cm^2)"]
kap_por_tension["Kerma_max_suelo (μGy/año)"] = kap_por_tension["Smax_suelo (μGy/Gy.cm^2)"] * kap_por_tension["KAP anual (Gy.cm^2)"]

# Corregir kerma por la distancia para cada pared (1/d²)
kap_por_tension["Kerma_corregido_pared1 (μGy/año)"] = kap_por_tension["Kerma_max_pared (μGy/año)"] / d_pared1**2
kap_por_tension["Kerma_corregido_pared2 (μGy/año)"] = kap_por_tension["Kerma_max_pared (μGy/año)"] / d_pared2**2
kap_por_tension["Kerma_corregido_pared3 (μGy/año)"] = kap_por_tension["Kerma_max_pared (μGy/año)"] / d_pared3**2
kap_por_tension["Kerma_corregido_pared4 (μGy/año)"] = kap_por_tension["Kerma_max_pared (μGy/año)"] / d_pared4**2

# Corregir kerma para techo y suelo
kap_por_tension["Kerma_corregido_techo (μGy/año)"] = kap_por_tension["Kerma_max_techo (μGy/año)"] / d_techo**2
kap_por_tension["Kerma_corregido_suelo (μGy/año)"] = kap_por_tension["Kerma_max_suelo (μGy/año)"] / d_suelo**2

# Guardar el resultado final
kap_por_tension.to_csv("analisis_por_tension.csv", sep=";", index=False, encoding="utf-8")

# Mostrar mensaje de éxito con todas las distancias
messagebox.showinfo("Proceso completado", (
    "Cálculos finalizados correctamente.\n\n"
    f"Distancia pared 1: {d_pared1} m\n"
    f"Distancia pared 2: {d_pared2} m\n"
    f"Distancia pared 3: {d_pared3} m\n"
    f"Distancia pared 4: {d_pared4} m\n"
    f"Distancia al techo: {d_techo} m\n"
    f"Distancia al suelo: {d_suelo} m"
))
