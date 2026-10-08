# Laboratorio 3: Sistema de Búsqueda (Lista, ABB y B+)

**Estudiante:** Xiomara Echavarría Gallego

## 1. El problema

Comparar tres estructuras de datos — **Lista**, **Árbol Binario de Búsqueda (ABB)** y **Árbol B+** — para medir cuánto tardan en buscar un estudiante por su `id`, y ver cómo escala ese tiempo cuando crece el número de estudiantes `N`, en dos situaciones:

- con los `id` **desordenados** (caso normal)
- con los `id` **ordenados** (peor caso)

Cada estudiante es un diccionario con `id`, `nombre`, `edad` y `promedio`. La búsqueda siempre es por `id`.

## 2. Las estructuras y las decisiones de diseño

### Estructura

- **Lista**: recorre de uno en uno. Complejidad: `O(N)`.
- **ABB**: baja por el árbol (menor a la izquierda, mayor a la derecha). Complejidad: `O(log N)` en caso aleatorio, pero **`O(N)` cuando los ids están ordenados** y el árbol se degrada.
- **B+**: baja por el árbol y almacena los datos en las hojas. Complejidad: `O(log N)` siempre.

### Decisiones de diseño

- **La Lista** se implementó con la **lista de Python**. La búsqueda sigue siendo `O(N)` porque se recorre de principio a fin.
- **El ABB** se hizo de manera **iterativa**, no recursiva. Esto es más eficiente y evita el riesgo de desbordamiento de la pila si los ids están ordenados y el árbol crece en una sola rama.
- **El B+** usa nodos con capacidad limitada y se reorganiza al llenarse, por lo que queda balanceado y no se degrada.

## 3. Cómo se midió (metodología)

- **Reloj:** `time.perf_counter()` (alta precisión).
- **Muchas búsquedas por medición:** una búsqueda sola tarda microsegundos, por lo que se realizan miles o millones de búsquedas, se mide el total y luego se divide entre la cantidad de búsquedas. Así cada medición dura más de 1 segundo.
- **10 repeticiones** por caso. Se reportan **promedio ± desviación estándar**.
- **Recolector de basura apagado** (`gc.disable()`) durante la medición.
- **Rango de `N`**:
  - más valores con `id` aleatorios (de 1.000 a 100.000)
  - menos con `id` ordenados (de 1.000 a 20.000), porque construir un ABB ordenado es `O(N²)` y se vuelve muy lento.


## 4. Cómo correr el proyecto

Las instrucciones detalladas están en **`COMO_CORRER.md`**. En resumen, para Windows se usa:

```bash
pip install matplotlib
python pruebas.py && python experimento.py && python graficas.py
```

- `experimento.py` mide y guarda `datos/resultados.csv`
- `graficas.py` genera `figuras/graficas.png` y `datos/tablas.md`

## 5. Resultados

Las tablas completas están en **`datos/tablas.md`** y la figura en **`figuras/graficas.png`** (4 gráficas: aleatorios y ordenados, cada uno en escala normal y logarítmica).

### Tiempo de una búsqueda (µs), ids aleatorios — resumen

- `N = 1.000`: Lista = `22,2`, ABB = `1,31`, B+ = `1,25`, Lista es `18×` más lenta que B+
- `N = 20.000`: Lista = `566`, ABB = `3,13`, B+ = `2,55`, Lista es `222×` más lenta que B+
- `N = 100.000`: Lista = `7.042`, ABB = `5,50`, B+ = `4,53`, Lista es **`1.555×`** más lenta que B+

### Tiempo de una búsqueda (µs), ids ordenados — resumen

- `N = 1.000`: Lista = `19,0`, ABB = `50,0`, B+ = `1,26`, ABB es `40×` más lento que B+
- `N = 20.000`: Lista = `432`, ABB = `1.102`, B+ = `2,79`, ABB es **`395×`** más lento que B+

### Altura de los árboles (prueba de degradación)

- `N = 1.000`: ABB aleatorio ≈ 23, ABB ordenado = **1.000**, B+ ≈ 6
- `N = 20.000`: ABB aleatorio ≈ 34, ABB ordenado = **20.000**, B+ ≈ 9

## 6. Análisis y hallazgos

- **La Lista es `O(N)`:** cuando `N` se duplica, su tiempo se duplica. Con 100.000 estudiantes, llega a ser **1.555 veces más lenta que el B+**.
- **Los árboles son `O(log N)`:** con `id` aleatorios casi no crecen y se mantienen en 1–6 µs.
- **El ABB se degrada con `id` ordenados:** su altura se vuelve igual a `N` (una fila), así que buscar en él cuesta `O(N)`, como en la Lista. La tabla de alturas lo demuestra.
- **El B+ nunca se degrada:** se mantiene `O(log N)` en los dos casos. Es la estructura más robusta.
- **El entorno afecta la medición:** en una primera corrida, con el navegador y OneDrive abiertos, el ABB ordenado en `N = 20.000` tuvo un valor mucho más alto. Al cerrar las apps y volver a correr, el dato bajó significativamente. Por eso es importante controlar el entorno al medir tiempos.

## 7. Conclusión

El **B+ es la estructura más robusta**: es `O(log N)` siempre, pase lo que pase con el orden de los datos; por eso lo usan muchas bases de datos reales. El **ABB** es excelente con datos desordenados, pero se degrada con datos ordenados y pasa a ser `O(N)`. La **Lista** solo sirve para pocos datos.

## 8. Entorno (mi computador)

- **Procesador:** AMD Ryzen 3 7320U with Radeon Graphics (2,40 GHz)
- **RAM:** 16 GB (13,7 GB utilizables)
- **Sistema operativo:** Windows 11, 64 bits (x64)
- **Python:** 3.13.2
- **matplotlib:** 3.11.2
- **Fecha de la corrida:** 8 de octubre de 2026, aproximadamente 10:50 a. m.
- **FACTOR usado:** 1 (corrida normal, 10 repeticiones)

> Los datos del procesador, RAM y sistema operativo fueron revisados en **Configuración → Sistema → Información**. No se copió el identificador de dispositivo ni el ID del producto.

## 9. Archivos del proyecto

- `lista.py`, `abb.py`, `bmas.py`: las tres estructuras
- `pruebas.py`: verifica que las estructuras funcionan
- `experimento.py`: mide tiempos y guarda `datos/resultados.csv`
- `graficas.py`: genera `figuras/graficas.png` y `datos/tablas.md`
- `COMO_CORRER.md`: instrucciones paso a paso
- `GUIA_SUSTENTACION.md`: explicación detallada para la sustentación
- `README.md`: este documento

## 10. Código de honor

Declaro que:

- Desarrollé este laboratorio **con ayuda de una inteligencia artificial (Claude)**, con la que fui construyendo y entendiendo el código (las estructuras, el experimento y las gráficas).
- **Discutí el diseño del experimento con mi compañera Arelis Giraldo Mazo** (trabajo en equipo permitido y declarado). Cada una entregó su propio código y sus propios datos.
- **Las mediciones las realicé yo**, en mi propio computador, con las condiciones descritas en la sección “Entorno”.
- **Entiendo el funcionamiento del código y puedo sustentarlo.**


