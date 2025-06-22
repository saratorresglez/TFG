# TFG

Este proyecto es un programa en Python que calcula el kerma en aire por radiación dispersa para una sala de radiografía general y determina los espesores de blindaje necesarios para diferentes tipos de barreras.

Permite introducir distancias mínimas desde el paciente a las paredes, techo y suelo, y realiza los cálculos necesarios para evaluar la radiación dispersa según diferentes tensiones y tipos de exploración, culminando con el cálculo de blindajes optimizados.

---

## Funcionalidades principales

- **Lectura de datos desde archivos CSV**: `input.csv` para bucky de mesa, `input_pared.csv` para bucky de pared, `coeficientes.csv` para coeficientes de atenuación.
- **Cálculo del KAP anual** por tipo de exploración.
- **Cálculo de valores específicos `Smax`** para paredes, techo y suelo según la tensión (kV), con fórmulas distintas para bucky de mesa y bucky de pared.
- **Cálculo del kerma máximo y kerma corregido** por la distancia (1/d²) para todas las superficies consideradas.
- **Solicitud interactiva y validada** de las distancias a las superficies mediante ventanas gráficas.
- **Selección de materiales** por barrera (plomo, hormigón o ambos).
- **Asignación de límites de dosis** según criterios de protección radiológica (normal o Sutton).
- **Cálculo del factor de ocupación (T)** para cada barrera.
- **Cálculo de espesores de blindaje** utilizando el método de Archer inverso y algoritmo de dicotomía.
- **Optimización de espesores comerciales** para plomo (1.0, 1.5, 2.0 mm).
- **Corrección por densidad** para hormigón respecto a la densidad de referencia (2.35 g/cm³).
- **Generación de resultados** en múltiples archivos CSV para análisis posterior.

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

**Librerías incluidas:**
- `pandas` - Manipulación de datos
- `numpy` - Cálculos numéricos
- `tkinter` - Interfaz gráfica (incluida en Python estándar)

---

## Estructura de archivos

### Archivos de entrada requeridos:
- `input.csv` - Datos del bucky de mesa (tensión, KAP, número de exploraciones)
- `input_pared.csv` - Datos del bucky de pared (tensión, KAP, número de exploraciones)
- `coeficientes.csv` - Coeficientes de atenuación por material y tensión (alpha, beta, gamma)

### Formato de los archivos CSV de entrada:

**input.csv / input_pared.csv:**
```csv
Tensión (kV);KAP (Gy.cm^2);numero de exploraciones anuales
80;0.5;100
100;0.8;150
120;1.2;200
```

**coeficientes.csv:**
```csv
material;tension;alpha (mm^-1);beta (mm^-1);gamma
plomo;80;0.123;0.456;0.789
hormigon;80;0.234;0.567;0.890
```

---

## ¿Cómo usarlo?

1. **Comprueba que existen los archivos** `input.csv` para el bucky de mesa, `input_pared.csv` para bucky de pared y `coeficientes.csv` con formato CSV, pues es aquí donde el usuario introducirá los datos de partida para cada tipo de exploración y los coeficientes de atenuación.

2. **Ejecuta el script principal**:
   ```bash
   python calculadora_blindaje.py
   ```

3. **Aparecerán ventanas gráficas** para introducir las distancias mínimas a cada superficie (4 paredes, techo y suelo) para ambos buckys. Introduce valores positivos en metros.

4. **Selecciona materiales** para cada barrera mediante las ventanas desplegables (plomo, hormigón o ambos).

5. **Elige el criterio de protección** radiológica (normal o Sutton) y asigna límites de dosis para cada barrera.

6. **Introduce factores de ocupación (T)** para cada barrera (valores entre 0 y 1).

7. **Para hormigón**: introduce la densidad real y espesor existente para techo y suelo.

8. **Al completar todos los pasos**, el programa generará en la misma carpeta los siguientes archivos:

### Archivos de salida generados:

- `resultados_kap_mesa.csv` – KAP anual por tipo de exploración para el bucky de mesa
- `analisis_por_tension_mesa.csv` – Kerma dispersa corregido por distancia para cada superficie del bucky de mesa
- `resultados_kap_pared.csv` – KAP anual por tipo de exploración para el bucky de pared
- `analisis_por_tension_pared.csv` – Kerma dispersa corregido por distancia para cada superficie del bucky de pared
- `kerma_con_material.csv` – Datos consolidados con materiales, coeficientes y parámetros asignados
- `resultados_blindaje.csv` – Cálculos detallados de espesores para cada barrera y material
- **`blindaje_final.csv`** – **Resultado final con espesores de blindaje necesarios**

---

## Criterios de protección radiológica

### Criterio Normal:
- Zona controlada: 20 mSv/año
- Zona vigilada: 6 mSv/año  
- Zona de público: 1 mSv/año

### Criterio Sutton:
- Zonas público/vigiladas: 0.3 mSv/año
- Almacén chasis CR: 0.025 mSv/año

---

## Factor de ocupación (T)

Valores típicos sugeridos:
- **Ocupación total**: T = 1
- **Ocupación parcial**: T = 0.2 - 0.5
- **Ocupación ocasional**: T = 0.05 - 0.125

---

## Metodología de cálculo

El programa utiliza:
- **Fórmulas específicas de Smax** según tensión y tipo de bucky
- **Corrección por ley inversa del cuadrado** para la distancia
- **Método de Archer** para el cálculo de transmisión: B = [(1+β/α)e^(αγx) - β/α]^(-1/γ)
- **Algoritmo de dicotomía** para encontrar el espesor mínimo de blindaje
- **Optimización de espesores comerciales** para plomo
- **Corrección por densidad** para hormigón


