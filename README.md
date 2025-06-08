# TFG



Este proyecto es un programa en Python que calcula el kerma en aire por radiación dispersa para una sala de radiografía general.  
Permite introducir distancias mínimas desde el paciente a las paredes, techo y suelo, y realiza los cálculos necesarios para evaluar la radiación dispersa según diferentes tensiones y tipos de exploración.

---

## Funcionalidades principales

- Lectura de datos desde archivos CSV: `input.csv` para bucky de mesa, `input_pared.csv` para bucky de pared.
- Cálculo del KAP anual por tipo de exploración.
- Cálculo de valores específicos `Smax` para paredes, techo y suelo según la tensión (kV), con fórmulas distintas para bucky de mesa y bucky de pared.
- Cálculo del kerma máximo y kerma corregido por la distancia (1/d²) para todas las superficies consideradas.
- Solicitud interactiva y validada de las distancias a las superficies mediante ventanas gráficas.
- Generación de resultados en archivos CSV para análisis posterior:
  - `resultados_kap_mesa.csv`
  - `analisis_por_tension_mesa.csv`
  - `resultados_kap_pared.csv`
  - `analisis_por_tension_pared.csv`

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

1. Comprueba que existen los archivos `input.csv` para el bucky de mesa e`input_pared.csv` para bucky de pared con  formato csv pues es aquí es donde el usuario introducirá los datos de partida para cada tipo de exploración y bucky.
2. Ejecuta el script principal (por ejemplo, `apartadoa.py`):

```bash
python apartadoa.py
```
3. Aparecerán ventanas gráficas para introducir las distancias mínimas a cada superficie (4 paredes, techo y suelo) para ambos buckys. Introduce valores positivos en metros.

4. Al completar todas las distancias, el programa generará en la misma carpeta los siguientes archivos:

- `resultados_kap_mesa.csv` – KAP anual por tipo de exploración para el bucky de mesa  
- `analisis_por_tension_mesa.csv` – Kerma dispersa corregido por distancia para cada superficie del bucky de mesa y todos los parámetros previos que conducen al cálculo.

- `resultados_kap_pared.csv` – KAP anual por tipo de exploración para el bucky de pared  
- `analisis_por_tension_pared.csv` – Kerma dispersa corregido por distancia para cada superficie del bucky de pared y todos los parámetros previos que conducen al cálculo.


