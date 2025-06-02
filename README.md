# TFG



Este proyecto es un programa en Python que calcula el kerma en aire por radiación dispersa para una sala de radiografía general.  
Permite introducir distancias mínimas desde el paciente a las paredes, techo y suelo, y realiza los cálculos necesarios para evaluar la radiación dispersa según diferentes tensiones y tipos de exploración.

---

## Funcionalidades principales

- Lectura de datos de entrada desde un archivo `input.csv`.
- Cálculo del KAP anual por tipo de exploración.
- Cálculo de valores `Smax` específicos para paredes, techo y suelo según la tensión (kV).
- Cálculo del kerma máximo y kerma corregido por la distancia (1/d²).
- Uso de ventanas gráficas para pedir distancias con validación.
- Generación de resultados en archivos CSV para análisis posterior.

---

## Clonar el repositorio

Para obtener el script y los archivos asociados, clona este repositorio en tu máquina:

```bash
git clone https://github.com/saratorresglez/TFG.git
cd TFG
```

---

## Requisitos

Python 3.7 o superior  
Librerías necesarias (instalar con):

```bash
pip install -r requirements.txt
```
---

## ¿Cómo usarlo?

1. Comprueba que existe un archivo `input.csv` con este formato pues es aquí es donde el usuario introducirá los datos de partida para cada tipo de exploración.
2. Ejecuta el script principal (por ejemplo, `main.py`):

```bash
python main.py
```
3. Aparecerán ventanas gráficas para introducir las distancias mínimas a cada superficie (4 paredes, techo y suelo). Introduce valores positivos en metros.
4. Al completar todas las distancias, el programa generará en la misma carpeta:

- `resultados_kap.csv` – KAP anual por tipo de exploración  
- `analisis_por_tension.csv` – Kerma dispersa corregido por distancia para cada superficie y todos los páratemtros previos que conducen al cálculo de este.



