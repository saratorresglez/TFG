import pandas as pd
import tkinter as tk
from tkinter import simpledialog, messagebox

# Crear ventana raíz casi invisible 
root = tk.Tk()
root.title("Ventana Principal (invisible)")
root.geometry("1x1+990+480")  
root.update_idletasks()
root.deiconify()  # Mostrar ventana (pero es casi invisible)


# Función para pedir una distancia y validarla
def pedir_distancia(etiqueta):
    while True:
        try:
            valor = simpledialog.askstring("Entrada", f"Introduce la distancia {etiqueta} (en metros):", parent=root)
            if valor is None:
                raise TypeError
            distancia = float(valor)
            if distancia <= 0:
                raise ValueError
            return distancia
        except (TypeError, ValueError):
            messagebox.showerror("Error", f"Introduce un número válido y positivo para la distancia {etiqueta}.", parent=root)

# Pedir distancias BUCKY DE MESA
messagebox.showinfo("Distancias", "Introduce las distancias para el BUCKY DE MESA", parent=root)
d_pared1 = pedir_distancia("PARED 1 (bucky mesa)")
d_pared2 = pedir_distancia("PARED 2 (bucky mesa)")
d_pared3 = pedir_distancia("PARED 3 (bucky mesa)")
d_pared4 = pedir_distancia("PARED 4 (bucky mesa)")
d_techo = pedir_distancia("TECHO (bucky mesa)")
d_suelo = pedir_distancia("SUELO (bucky mesa)")

# Pedir distancias BUCKY DE PARED
messagebox.showinfo("Distancias", "Introduce las distancias para el BUCKY DE PARED", parent=root)
dp_pared_lateral1 = pedir_distancia("PARED LATERAL 1 (bucky pared)")
dp_pared_lateral2 = pedir_distancia("PARED LATERAL 2 (bucky pared)")
dp_techo = pedir_distancia("TECHO (bucky pared)")
dp_suelo = pedir_distancia("SUELO (bucky pared)")
dp_detras_tubo = pedir_distancia("PARED DETRÁS DEL TUBO")
dp_detras_bucky = pedir_distancia("PARED DETRÁS DEL BUCKY DE PARED")

# Función principal
def procesar_archivo(nombre_csv, es_bucky_pared=False):
    df = pd.read_csv(nombre_csv, sep=";", encoding="utf-8")
    df["KAP anual (Gy.cm^2)"] = df["KAP (Gy.cm^2)"] * df["numero de exploraciones anuales"]

    salida_kap = f"resultados_kap_{'pared' if es_bucky_pared else 'mesa'}.csv"
    df[["Tipo de exploración", "KAP anual (Gy.cm^2)"]] = df[["Tipo de exploración", "KAP anual (Gy.cm^2)"]].round(3)
    df[["Tipo de exploración", "KAP anual (Gy.cm^2)"]].to_csv(salida_kap, sep=";", index=False, encoding="utf-8")

    kap_por_tension = df.groupby("Tensión (kV)")["KAP anual (Gy.cm^2)"].sum().reset_index()

    if not es_bucky_pared:
        kap_por_tension["Smax_pared"] = 0.031 * kap_por_tension["Tensión (kV)"] + 2.5
        kap_por_tension["Smax_techo"] = 0.058 * kap_por_tension["Tensión (kV)"] + 4.8
        kap_por_tension["Smax_suelo"] = 0.011 * kap_por_tension["Tensión (kV)"] + 0.9

        kap_por_tension["Kerma_max_pared"] = kap_por_tension["Smax_pared"] * kap_por_tension["KAP anual (Gy.cm^2)"]
        kap_por_tension["Kerma_max_techo"] = kap_por_tension["Smax_techo"] * kap_por_tension["KAP anual (Gy.cm^2)"]
        kap_por_tension["Kerma_max_suelo"] = kap_por_tension["Smax_suelo"] * kap_por_tension["KAP anual (Gy.cm^2)"]

        kap_por_tension["Kerma_corregido_pared1"] = kap_por_tension["Kerma_max_pared"] / d_pared1**2
        kap_por_tension["Kerma_corregido_pared2"] = kap_por_tension["Kerma_max_pared"] / d_pared2**2
        kap_por_tension["Kerma_corregido_pared3"] = kap_por_tension["Kerma_max_pared"] / d_pared3**2
        kap_por_tension["Kerma_corregido_pared4"] = kap_por_tension["Kerma_max_pared"] / d_pared4**2
        kap_por_tension["Kerma_corregido_techo"] = kap_por_tension["Kerma_max_techo"] / d_techo**2
        kap_por_tension["Kerma_corregido_suelo"] = kap_por_tension["Kerma_max_suelo"] / d_suelo**2

        kap_por_tension = kap_por_tension.round(3)
        kap_por_tension.to_csv("analisis_por_tension_mesa.csv", sep=";", index=False, encoding="utf-8")

    else:
        # Smax adaptado
        kap_por_tension["Smax_lateral"] = 0.031 * kap_por_tension["Tensión (kV)"] + 2.5
        kap_por_tension["Smax_detras_tubo"] = 0.058 * kap_por_tension["Tensión (kV)"] + 4.8
        kap_por_tension["Smax_detras_bucky"] = 0.011 * kap_por_tension["Tensión (kV)"] + 0.9

        kap_por_tension["Kerma_max_lateral"] = kap_por_tension["Smax_lateral"] * kap_por_tension["KAP anual (Gy.cm^2)"]
        kap_por_tension["Kerma_max_detras_tubo"] = kap_por_tension["Smax_detras_tubo"] * kap_por_tension["KAP anual (Gy.cm^2)"]
        kap_por_tension["Kerma_max_detras_bucky"] = kap_por_tension["Smax_detras_bucky"] * kap_por_tension["KAP anual (Gy.cm^2)"]

        kap_por_tension["Kerma_corregido_lateral1"] = kap_por_tension["Kerma_max_lateral"] / dp_pared_lateral1**2
        kap_por_tension["Kerma_corregido_lateral2"] = kap_por_tension["Kerma_max_lateral"] / dp_pared_lateral2**2
        kap_por_tension["Kerma_corregido_techo"] = kap_por_tension["Kerma_max_lateral"] / dp_techo**2
        kap_por_tension["Kerma_corregido_suelo"] = kap_por_tension["Kerma_max_lateral"] / dp_suelo**2
        kap_por_tension["Kerma_corregido_detras_tubo"] = kap_por_tension["Kerma_max_detras_tubo"] / dp_detras_tubo**2
        kap_por_tension["Kerma_corregido_detras_bucky"] = kap_por_tension["Kerma_max_detras_bucky"] / dp_detras_bucky**2

        kap_por_tension = kap_por_tension.round(3)
        kap_por_tension.to_csv("analisis_por_tension_pared.csv", sep=";", index=False, encoding="utf-8")
        

# Ejecutar cálculos para ambos archivos
procesar_archivo("input.csv", es_bucky_pared=False)
procesar_archivo("input_pared.csv", es_bucky_pared=True)

# Confirmación final
messagebox.showinfo("Proceso completado", "Los cálculos para ambos buckys se han completado correctamente y los archivos han sido generados.", parent=root)


# Cerrar ventana raíz al finalizar
root.destroy()