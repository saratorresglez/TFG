import pandas as pd
import tkinter as tk
from tkinter import simpledialog, messagebox
import numpy as np
from tkinter import ttk
from itertools import combinations_with_replacement

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

# Función principal apartado a
def procesar_archivo(nombre_csv, es_bucky_pared=False):
    df = pd.read_csv(nombre_csv, sep=";", encoding="utf-8")
    df["KAP anual (Gy.cm^2)"] = df["KAP (Gy.cm^2)"] * df["numero de exploraciones anuales"]

    salida_kap = f"resultados_kap_{'pared' if es_bucky_pared else 'mesa'}.csv"
    
    kap_por_tension = df.groupby("Tensión (kV)")["KAP anual (Gy.cm^2)"].sum().reset_index()

    if not es_bucky_pared:
        kap_por_tension["Smax_pared"] = 0.031 * kap_por_tension["Tensión (kV)"] + 2.5
        kap_por_tension["Smax_techo"] = 0.058 * kap_por_tension["Tensión (kV)"] + 4.8
        kap_por_tension["Smax_suelo"] = 0.011 * kap_por_tension["Tensión (kV)"] + 0.9

        kap_por_tension["Kerma_max_pared"] = kap_por_tension["Smax_pared"] * kap_por_tension["KAP anual (Gy.cm^2)"]
        kap_por_tension["Kerma_max_techo"] = kap_por_tension["Smax_techo"] * kap_por_tension["KAP anual (Gy.cm^2)"]
        kap_por_tension["Kerma_max_suelo"] = kap_por_tension["Smax_suelo"] * kap_por_tension["KAP anual (Gy.cm^2)"]

        kap_por_tension["Kerma_corregido_pared1"] = kap_por_tension["Kerma_max_pared"] / d_pared1**2 / 1000
        kap_por_tension["Kerma_corregido_pared2"] = kap_por_tension["Kerma_max_pared"] / d_pared2**2 / 1000
        kap_por_tension["Kerma_corregido_pared3"] = kap_por_tension["Kerma_max_pared"] / d_pared3**2 / 1000
        kap_por_tension["Kerma_corregido_pared4"] = kap_por_tension["Kerma_max_pared"] / d_pared4**2 / 1000
        kap_por_tension["Kerma_corregido_techo"] = kap_por_tension["Kerma_max_techo"] / d_techo**2 / 1000
        kap_por_tension["Kerma_corregido_suelo"] = kap_por_tension["Kerma_max_suelo"] / d_suelo**2 / 1000

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

        kap_por_tension["Kerma_corregido_lateral1"] = kap_por_tension["Kerma_max_lateral"] / dp_pared_lateral1**2 / 1000
        kap_por_tension["Kerma_corregido_lateral2"] = kap_por_tension["Kerma_max_lateral"] / dp_pared_lateral2**2 / 1000
        kap_por_tension["Kerma_corregido_techo"] = kap_por_tension["Kerma_max_lateral"] / dp_techo**2 / 1000
        kap_por_tension["Kerma_corregido_suelo"] = kap_por_tension["Kerma_max_lateral"] / dp_suelo**2 / 1000
        kap_por_tension["Kerma_corregido_detras_tubo"] = kap_por_tension["Kerma_max_detras_tubo"] / dp_detras_tubo**2 / 1000
        kap_por_tension["Kerma_corregido_detras_bucky"] = kap_por_tension["Kerma_max_detras_bucky"] / dp_detras_bucky**2 / 1000

        kap_por_tension = kap_por_tension.round(3)
        kap_por_tension.to_csv("analisis_por_tension_pared.csv", sep=";", index=False, encoding="utf-8")
        

# Ejecutar cálculos para ambos archivos
procesar_archivo("input.csv", es_bucky_pared=False)
procesar_archivo("input_pared.csv", es_bucky_pared=True)

#  Bloque para generar el csv combinado con materiales 

def pedir_material(barrera):
    seleccion = {"material": None}

    def elegir_plomo():
        seleccion["material"] = "plomo"
        ventana.destroy()

    def elegir_hormigon():
        seleccion["material"] = "hormigon"
        ventana.destroy()
    
    def elegir_ambos():
        seleccion["material"] = "ambos"
        ventana.destroy()

    ventana = tk.Toplevel(root)
    ventana.title(f"Selecciona material para '{barrera}'")
    ventana.geometry("350x160")
    ventana.update_idletasks()
    ventana.deiconify() 
    ventana.grab_set()

    etiqueta = tk.Label(ventana, text=f"Selecciona material para la barrera '{barrera}':")
    etiqueta.pack(pady=10)

    boton_plomo = tk.Button(ventana, text="Solo Plomo", width=20, command=elegir_plomo)
    boton_plomo.pack(pady=3)

    boton_hormigon = tk.Button(ventana, text="Solo Hormigón", width=20, command=elegir_hormigon)
    boton_hormigon.pack(pady=3)
    
    boton_ambos = tk.Button(ventana, text="Ambos Materiales", width=20, command=elegir_ambos)
    boton_ambos.pack(pady=3)

    ventana.wait_window()
    return seleccion["material"]

# Mapas de columnas a barreras y buckys para analisis_por_tension_mesa.csv
mapeo_mesa = {
    "Kerma_corregido_pared1": "Pared 1",
    "Kerma_corregido_pared2": "Pared 2",
    "Kerma_corregido_pared3": "Pared 3",
    "Kerma_corregido_pared4": "Pared 4",
    "Kerma_corregido_techo": "Techo",
    "Kerma_corregido_suelo": "Suelo",
}

# Mapas para analisis_por_tension_pared.csv
mapeo_pared = {
    "Kerma_corregido_lateral1": "Pared 1",
    "Kerma_corregido_detras_bucky": "Pared 2",
    "Kerma_corregido_lateral2": "Pared 3",
    "Kerma_corregido_detras_tubo": "Pared 4",
    "Kerma_corregido_techo": "Techo",
    "Kerma_corregido_suelo": "Suelo",
}

# Leer los CSV
df_mesa = pd.read_csv("analisis_por_tension_mesa.csv", sep=";", encoding="utf-8")
df_pared = pd.read_csv("analisis_por_tension_pared.csv", sep=";", encoding="utf-8")

# Extraer datos mesa en formato largo
filas_mesa = []
for col, barrera in mapeo_mesa.items():
    if col in df_mesa.columns:
        for _, fila in df_mesa.iterrows():
            filas_mesa.append({
                "tension": fila["Tensión (kV)"],
                "kerma_corregido": fila[col],
                "barrera": barrera,
                "bucky": "mesa",
            })

# Extraer datos pared en formato largo
filas_pared = []
for col, barrera in mapeo_pared.items():
    if col in df_pared.columns:
        for _, fila in df_pared.iterrows():
            filas_pared.append({
                "tension": fila["Tensión (kV)"],
                "kerma_corregido": fila[col],
                "barrera": barrera,
                "bucky": "pared",
            })

# Crear DataFrame combinado
df_combinado = pd.DataFrame(filas_mesa + filas_pared)

# Pedir material para cada barrera (solo una vez por barrera)
materiales = {}
barreras_unicas = df_combinado["barrera"].unique()
for barrera in barreras_unicas:
    materiales[barrera] = pedir_material(barrera)

# Asignar columna material
df_combinado["material"] = df_combinado["barrera"].map(materiales)

# Guardar nuevo CSV
df_combinado.to_csv("kerma_con_material.csv", sep=";", index=False, encoding="utf-8")

messagebox.showinfo(
    "Materiales asignados",
    "El archivo 'kerma_con_material.csv' ha sido creado con las columnas solicitadas y materiales asignados.",
    parent=root,
)

filas_expandidas = []

for _, fila in df_combinado.iterrows():
    barrera = fila["barrera"]
    material_seleccionado = materiales[barrera]
    
    if material_seleccionado == "ambos":
        # Crear dos filas: una para plomo y otra para hormigón
        fila_plomo = fila.copy()
        fila_plomo["material"] = "plomo"
        filas_expandidas.append(fila_plomo)
        
        fila_hormigon = fila.copy()
        fila_hormigon["material"] = "hormigon"
        filas_expandidas.append(fila_hormigon)
    else:
        # Mantener la fila original con el material seleccionado
        fila["material"] = material_seleccionado
        filas_expandidas.append(fila)

# Recrear el DataFrame con las filas expandidas
df_combinado_expandido = pd.DataFrame(filas_expandidas)

# Continuar con el resto del proceso usando df_combinado_expandido
df_combinado_expandido.to_csv("kerma_con_material.csv", sep=";", index=False, encoding="utf-8")


# Cargar los CSV sin renombrar columnas
df_kerma = pd.read_csv("kerma_con_material.csv", sep=";")
df_coef = pd.read_csv("coeficientes.csv")

# Crear columnas vacías en df_kerma para los coeficientes
df_kerma["alpha"] = np.nan
df_kerma["beta"] = np.nan
df_kerma["gamma"] = np.nan

# Asignar coeficientes por voltaje más cercano SUPERIOR
for idx, row in df_kerma.iterrows():
    material = row["material"]  
    tension = row["tension"]    

    # Filtrar filas que coinciden con el material
    sub_df = df_coef[df_coef["material"] == material]

    # Buscar voltajes superiores o iguales
    voltajes_superiores = sub_df[sub_df["tension"] >= tension]
    
    if not voltajes_superiores.empty:
        # Si hay voltajes superiores, tomar el menor de ellos (más cercano superior)
        idx_min = voltajes_superiores["tension"].idxmin()
        fila_coef = voltajes_superiores.loc[idx_min]
    else:
        # Si no hay voltajes superiores, tomar el voltaje más alto disponible
        # (esto sería una situación de seguridad conservadora)
        idx_max = sub_df["tension"].idxmax()
        fila_coef = sub_df.loc[idx_max]

    # Asignar coeficientes a df_kerma
    df_kerma.at[idx, "alpha"] = fila_coef["alpha (mm^-1)"]
    df_kerma.at[idx, "beta"] = fila_coef["beta (mm^-1)"]
    df_kerma.at[idx, "gamma"] = fila_coef["gamma"]

# Guardar CSV con coeficientes añadidos
df_kerma.to_csv("kerma_con_material.csv", sep=";", index=False) 

# Diccionarios de opciones de P según el criterio
criterio_normal = {
    "Zona controlada (20 mSv/año)": 20,
    "Zona vigilada (6 mSv/año)": 6,
    "Zona de público (1 mSv/año)": 1
}

criterio_sutton = {
    "Zonas público/vigiladas (0.3 mSv/año)": 0.3,
    "Almacén chasis CR (0.025 mSv/año)": 0.025
}

# Leer el CSV con el separador adecuado
df_kerma = pd.read_csv("kerma_con_material.csv", sep=";")

# Obtener lista de barreras únicas
barreras = df_kerma["barrera"].unique()

# Diccionario para guardar la selección de P para cada barrera
seleccion_P = {}

# Ventana principal para elegir el criterio
def elegir_criterio():
    ventana_criterio=tk.Toplevel(root) 
    ventana_criterio.title("Seleccionar criterio")

    tk.Label(ventana_criterio, text="Selecciona el criterio para P:").pack(pady=10)

    def continuar():
        seleccion = criterio_var.get()
        if seleccion not in ["normal", "sutton"]:
            messagebox.showerror("Error", "Selecciona un criterio")
            return
        ventana_criterio.destroy()
        pedir_P_por_barrera(seleccion)

    criterio_var = tk.StringVar()
    tk.Radiobutton(ventana_criterio, text="Criterio normal", variable=criterio_var, value="normal").pack(anchor="w")
    tk.Radiobutton(ventana_criterio, text="Criterio Sutton", variable=criterio_var, value="sutton").pack(anchor="w")

    tk.Button(ventana_criterio, text="Continuar", command=continuar).pack(pady=10)

    ventana_criterio.wait_window()

# Ventana secundaria para elegir P por barrera
def pedir_P_por_barrera(criterio):
    ventana_P = tk.Toplevel(root)
    ventana_P.title("Seleccionar P por barrera")

    frame = tk.Frame(ventana_P)
    frame.pack(padx=10, pady=10)

    opciones = criterio_normal if criterio == "normal" else criterio_sutton
    menus_desplegables = {}

    for barrera in barreras:
        tk.Label(frame, text=f"{barrera}:").pack(anchor="w")
        var = tk.StringVar()
        var.set(next(iter(opciones)))  # primera opción como predeterminada
        menu = ttk.OptionMenu(frame, var, var.get(), *opciones.keys())
        menu.pack(anchor="w", fill="x")
        menus_desplegables[barrera] = var

    def guardar():
        for barrera in barreras:
            tipo_zona = menus_desplegables[barrera].get()
            seleccion_P[barrera] = opciones[tipo_zona]

        df_kerma["P"] = df_kerma["barrera"].map(seleccion_P)
        df_kerma.to_csv("kerma_con_material.csv", sep=";", index=False)
        messagebox.showinfo("Guardado", "Columna P añadida al archivo kerma_con_material.csv", parent=ventana_P)
        ventana_P.destroy()

    boton_guardar = tk.Button(ventana_P, text="Guardar", command=guardar)
    boton_guardar.pack(pady=10)

    ventana_P.grab_set()
    ventana_P.wait_window()

#Ejecutar la selección
elegir_criterio()


 # Lista de barreras (debes tenerla definida en tu código principal)
barreras = ['Pared 1', 'Pared 2', 'Pared 3', 'Pared 4', 'Techo', 'Suelo']

# Función para mostrar la sugerencia previa
def mostrar_sugerencias():
    mensaje = (
        "Valores típicos para el factor de ocupación (T):\n\n"
        "- Ocupación total: T = 1\n"
        "- Ocupación parcial: T = 0.2 - 0.5\n"
        "- Ocupación ocasional: T = 0.05 - 0.125\n\n"
        "Introduce un valor entre 0 y 1 para cada barrera."
    )
    messagebox.showinfo("Sugerencias para el factor de ocupación (T)", mensaje)

# Función principal para pedir T y guardar el archivo
def pedir_T_por_barrera():
    mostrar_sugerencias()

    seleccion_T = {}

    for barrera in barreras:
        while True:
            valor_str = simpledialog.askstring(
                "Factor de ocupación", f"Introduce T para {barrera} (entre 0 y 1):"
            )
            if valor_str is None:
                messagebox.showerror("Error", "Debes introducir un valor.")
                continue
            try:
                valor = float(valor_str)
                if 0 <= valor <= 1:
                    seleccion_T[barrera] = valor
                    break
                else:
                    messagebox.showerror("Error", "El valor debe estar entre 0 y 1.")
            except ValueError:
                messagebox.showerror("Error", "Introduce un número válido.")

    # Leer el CSV y añadir la columna T
    df_final = pd.read_csv("kerma_con_material.csv", sep=";")
    df_final["T"] = df_final["barrera"].map(seleccion_T)
    df_final.to_csv("kerma_con_material.csv", sep=";", index=False)
    messagebox.showinfo("Guardado", "Columna T añadida al archivo kerma_con_material.csv")


# Ejecutar la selección de T
pedir_T_por_barrera()
       

def calcular_factor_transmision(x, alpha, beta, gamma):
    """
    Calcula el factor de transmisión B_kV usando la fórmula de Archer inversa
    """
    try:
        exp_term = np.exp(alpha * gamma * x)
        base = (1 + beta/alpha) * exp_term - beta/alpha
        B_kV = base ** (-1/gamma)
        return B_kV
    except (OverflowError, ZeroDivisionError, ValueError):
        return 0  # Si hay overflow, la transmisión es prácticamente 0

def funcion_objetivo(x, datos_barrera):
    """
    Función objetivo: suma de kerma corregido * factor de transmisión - P/T
    Buscamos el x donde esta función se hace cero (o negativa)
    """
    suma_total = 0
    
    for _, fila in datos_barrera.iterrows():
        kerma = fila['kerma_corregido']
        alpha = fila['alpha']
        beta = fila['beta'] 
        gamma = fila['gamma']
        
        # Calcular factor de transmisión para este kV
        B_kV = calcular_factor_transmision(x, alpha, beta, gamma)
        
        # Sumar contribución de esta tensión
        suma_total += kerma * B_kV
    
    # P/T es constante para toda la barrera (mismo para todas las filas)
    P_sobre_T = datos_barrera.iloc[0]['P'] / datos_barrera.iloc[0]['T']
    
    return suma_total - P_sobre_T

def dicotomia(datos_barrera, x_min=0, x_max=100, tolerancia=1e-6, max_iter=100):
    """
    Método de dicotomía para encontrar el espesor mínimo de blindaje
    
    Args:
        datos_barrera: DataFrame con datos de una barrera específica
        x_min: espesor mínimo a considerar (mm)
        x_max: espesor máximo a considerar (mm)
        tolerancia: precisión deseada
        max_iter: máximo número de iteraciones
    
    Returns:
        x_solucion: espesor mínimo necesario en mm
    """
    
    # Verificar que existe solución en el intervalo
    f_min = funcion_objetivo(x_min, datos_barrera)
    f_max = funcion_objetivo(x_max, datos_barrera)
    
    if f_min <= 0:
        return x_min  # No necesita blindaje
    
    if f_max > 0:
        # Aumentar x_max hasta encontrar cambio de signo
        while f_max > 0 and x_max < 1000:
            x_max *= 2
            f_max = funcion_objetivo(x_max, datos_barrera)
        
        if f_max > 0:
            raise ValueError("No se puede encontrar espesor suficiente")
    
    # Aplicar dicotomía
    for iteracion in range(max_iter):
        x_medio = (x_min + x_max) / 2
        f_medio = funcion_objetivo(x_medio, datos_barrera)
        
        if abs(f_medio) < tolerancia or abs(x_max - x_min) < tolerancia:
            return x_medio
        
        if f_medio > 0:
            x_min = x_medio
        else:
            x_max = x_medio
    
    return (x_min + x_max) / 2

def calcular_blindajes():
    """
    Función principal que calcula los espesores para todas las barreras y materiales
    """
    # Leer datos
    df = pd.read_csv("kerma_con_material.csv", sep=";")
    
    # Agrupar por barrera Y material (puede haber múltiples materiales por barrera)
    grupos = df.groupby(['barrera', 'material'])
    resultados = []
    
    for (barrera, material), datos_grupo in grupos:
        
        # Verificar que tenemos datos válidos
        if datos_grupo.empty:
            continue
        
        # Verificar que tenemos todos los coeficientes necesarios
        if datos_grupo[['alpha', 'beta', 'gamma']].isnull().any().any():
            continue
        
        try:
            # Aplicar método de dicotomía
            espesor_mm = dicotomia(datos_grupo)
            
            # Obtener datos adicionales
            P = datos_grupo.iloc[0]['P']
            T = datos_grupo.iloc[0]['T']
            
            # Convertir a cm
            espesor_cm = espesor_mm / 10
            
            resultados.append({
                'Barrera': barrera,
                'Material': material,
                'Espesor_mm': round(espesor_mm, 3),
                'Espesor_cm': round(espesor_cm, 3),
                'P_mSv': P,
                'T': T,
                'Verificacion': round(funcion_objetivo(espesor_mm, datos_grupo), 6)
            })
            
        except Exception as e:
            resultados.append({
                'Barrera': barrera,
                'Material': material,
                'Espesor_mm': 'ERROR',
                'Espesor_cm': 'ERROR',
                'P_mSv': datos_grupo.iloc[0]['P'] if not datos_grupo.empty else 'N/A',
                'T': datos_grupo.iloc[0]['T'] if not datos_grupo.empty else 'N/A',
                'Verificacion': str(e)
            })
    
    # Crear DataFrame con resultados
    df_resultados = pd.DataFrame(resultados)
    
    # Ordenar por barrera y material para mejor visualización
    df_resultados = df_resultados.sort_values(['Barrera', 'Material'])
    
    # Guardar resultados
    df_resultados.to_csv("resultados_blindaje.csv", sep=";", index=False)
    
    return df_resultados
# Ejemplo de uso
if __name__ == "__main__":
    # Calcular todos los blindajes
    resultados = calcular_blindajes()

seleccion_densidad={}

def preguntar_densidad():
    for barrera in barreras:
        while True:
             if barrera == "Techo" or barrera == "Suelo":
                 
                 try:
                     valor_densidad = simpledialog.askstring("Densidad del hormigón", f"Introduce la densidad para {barrera}")    
                     if valor_densidad is None:
                         raise TypeError
                     densidad = float(valor_densidad)
                     if densidad <= 0:
                         raise ValueError
                     seleccion_densidad[barrera] = densidad
                     break
                 except (TypeError, ValueError):
                     messagebox.showerror("Error", f"Introduce un número válido y positivo para la densidad de {barrera}.")
             else:
                 seleccion_densidad[barrera] = 0
                 break

preguntar_densidad()

#Leer el DataFrame
df_densidad = pd.read_csv("resultados_blindaje.csv", sep=";")

# Función para asignar la densidad solo si el material es hormigón
def densidad_filtrada(row):
    if row["Material"] == "hormigon":
        return seleccion_densidad[row["Barrera"]]
    else:
        return 0

# Aplicar la función al DataFrame
df_densidad["Densidad real"] = df_densidad.apply(densidad_filtrada, axis=1)

# Guardar el archivo actualizado
df_densidad.to_csv("resultados_blindaje.csv", sep=";", index=False)
        
               
seleccion_espesor_real={}

def preguntar_espesor_real():
    for barrera in barreras:
        while True:
             if barrera == "Techo" or barrera == "Suelo":
                 
                 try:
                     valor_espesor_real = simpledialog.askstring("Espesor real", f"Introduce el espesor real para {barrera}")    
                     if valor_espesor_real is None:
                         raise TypeError
                     espesor_real = float(valor_espesor_real)
                     if espesor_real <= 0:
                         raise ValueError
                     seleccion_espesor_real[barrera] = espesor_real
                     break
                 except (TypeError, ValueError):
                     messagebox.showerror("Error", f"Introduce un número válido y positivo para el espesor real de {barrera}.")
             else:
                 seleccion_espesor_real[barrera] = 0
                 break

preguntar_espesor_real()



#Leer el DataFrame
df_espesor_real = pd.read_csv("resultados_blindaje.csv", sep=";")

# Función para asignar la espesor real solo si el material es hormigón
def espesor_real_filtrado(row):
    if row["Material"] == "hormigon":
        return seleccion_espesor_real[row["Barrera"]]
    else:
        return 0

# Aplicar la función al DataFrame
df_espesor_real["Espesor real"] = df_espesor_real.apply(espesor_real_filtrado, axis=1)

# Guardar el archivo actualizado
df_espesor_real.to_csv("resultados_blindaje.csv", sep=";", index=False)


def agregar_espesor_corregido(df):
    
    def calcular_corregido(densidad, espesor):
        if densidad == 0:
            return 0.0
        elif densidad == 2.35:
            return espesor
        else:
            return (densidad * espesor) / 2.35
    
    df['Espesor real corregido'] = df.apply(
        lambda row: calcular_corregido(row['Densidad real'], row['Espesor real']), 
        axis=1
    )
    return df

# Leer CSV, procesar y guardar
df_espesor_corregido = pd.read_csv('resultados_blindaje.csv', sep=';')
df_espesor_corregido = agregar_espesor_corregido(df_espesor_corregido)
df_espesor_corregido.to_csv('resultados_blindaje.csv', sep=';', index=False)



def calcular_espesor_plomo_optimo(espesor_requerido_mm):
    # Planchas comerciales disponibles
    planchas = [1.0, 1.5, 2.0]
    
    # Si el espesor requerido es 0 o negativo, devolver 0
    if espesor_requerido_mm <= 0:
        return 0.0
    
    # Generar todas las combinaciones posibles hasta un máximo razonable
    # Limitamos a 10 planchas para evitar combinaciones excesivas
    combinaciones_validas = []
    
    for num_planchas in range(1, 11):  # De 1 a 10 planchas
        for combo in combinations_with_replacement(planchas, num_planchas):
            espesor_total = sum(combo)
            if espesor_total >= espesor_requerido_mm:
                combinaciones_validas.append(espesor_total)
    
    # Si no hay combinaciones válidas, usar la plancha más grande
    if not combinaciones_validas:
        return max(planchas)
    
    # Devolver el espesor mínimo que cumple el requisito
    return min(combinaciones_validas)

def agregar_espesor_plomo_real(df):
    def calcular_para_fila(row):
        if row['Material'].lower() == 'plomo':
            return calcular_espesor_plomo_optimo(row['Espesor_mm'])
        else:
            return 0.0
    
    df['Espesor plomo real'] = df.apply(calcular_para_fila, axis=1)
    return df

# Leer CSV, procesar y guardar
df = pd.read_csv('resultados_blindaje.csv', sep=';')
df = agregar_espesor_plomo_real(df)
df.to_csv('resultados_blindaje.csv', sep=';', index=False)



def crear_csv_final():
    """
    Crea un CSV final con las columnas: Barrera, Material, Espesor necesario
    siguiendo la lógica específica para cada tipo de barrera
    """
    # Leer el CSV de resultados
    df = pd.read_csv('resultados_blindaje.csv', sep=';')
    
    # Lista para almacenar las filas del nuevo CSV
    filas_finales = []
    
    # Obtener barreras únicas
    barreras = df['Barrera'].unique()
    
    for barrera in barreras:
        datos_barrera = df[df['Barrera'] == barrera]
        
        if barrera in ['Pared 1', 'Pared 2', 'Pared 3', 'Pared 4']:
            # Para paredes: usar Espesor plomo real de la fila con material plomo
            fila_plomo = datos_barrera[datos_barrera['Material'] == 'plomo']
            if not fila_plomo.empty:
                espesor_necesario = fila_plomo.iloc[0]['Espesor plomo real']
                filas_finales.append({
                    'Barrera': barrera,
                    'Material': 'plomo',
                    'Espesor necesario': espesor_necesario
                })
        
        elif barrera in ['Techo', 'Suelo']:
            # Para techo y suelo: lógica más compleja
            fila_hormigon = datos_barrera[datos_barrera['Material'] == 'hormigon']
            fila_plomo = datos_barrera[datos_barrera['Material'] == 'plomo']
            
            if not fila_hormigon.empty:
                espesor_real_corregido = fila_hormigon.iloc[0]['Espesor real corregido']
                espesor_mm_hormigon = fila_hormigon.iloc[0]['Espesor_mm']
                
                if espesor_real_corregido > espesor_mm_hormigon:
                    # Usar hormigón con espesor real corregido
                    filas_finales.append({
                        'Barrera': barrera,
                        'Material': 'hormigon',
                        'Espesor necesario': espesor_real_corregido
                    })
                    
                else:
                    # Usar plomo
                    if not fila_plomo.empty:
                        espesor_plomo_real = fila_plomo.iloc[0]['Espesor plomo real']
                        filas_finales.append({
                            'Barrera': barrera,
                            'Material': 'plomo',
                            'Espesor necesario': espesor_plomo_real
                        })
                        
    
    # Crear DataFrame final
    df_final = pd.DataFrame(filas_finales)
    
    # Redondear espesor necesario a 3 decimales
    df_final['Espesor necesario'] = df_final['Espesor necesario'].round(3)
    
    # Guardar CSV
    df_final.to_csv('blindaje_final.csv', sep=';', index=False)
    
    
    
    return df_final

crear_csv_final()

# Cerrar ventana raíz al finalizar
root.destroy()


