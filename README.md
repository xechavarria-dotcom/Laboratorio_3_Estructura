# Laboratorio 3 — Sistema de Búsqueda (Lista, ABB y B+)

**Estudiante:** Xiomara Echavarría Gallego — 〔COMPLETAR: tu código estudiantil / cédula〕
**Curso:** Estructura de Datos — Universidad de Antioquia

---

## 1. De qué se trata

En este laboratorio comparo tres estructuras de datos —una **Lista**, un **Árbol Binario de
Búsqueda (ABB)** y un **Árbol B+**— para una tarea muy concreta: **buscar a un estudiante por
su `id`**. Cada estudiante es un diccionario con `id`, `nombre`, `edad` y `promedio`, y la
búsqueda siempre es por `id`.

Lo que quiero medir es **cuánto tarda cada estructura en encontrar a un estudiante** y, sobre
todo, **cómo cambia ese tiempo cuando crece el número de estudiantes N**. Y lo miro en dos
situaciones, porque no es lo mismo:

- Con los `id` **desordenados** (como llegan normalmente en la vida real).
- Con los `id` **ordenados** (el peor caso para uno de los árboles, como se verá).

La idea es ver con datos de verdad cuál estructura aguanta mejor cuando hay muchos
estudiantes.

---

## 2. La idea en simple

Buscar a un estudiante por su `id` es parecido a buscar un contacto. Cada estructura lo hace
de una forma distinta:

- **La Lista** es como leer la lista de asistencia de arriba a abajo hasta encontrar el
nombre. Si hay 100.000 estudiantes y el que busco quedó de último, me toca revisarlos casi
todos. Por eso se dice que es **O(N)**: entre más estudiantes, más tardo, en proporción
directa.
- **El ABB** es como el juego de *"adivina el número"*, donde en cada intento me dicen "más
arriba" o "más abajo" y así **descarto la mitad** cada vez. Por eso normalmente es
rapidísimo: **O(log N)**. Pero tiene una trampa: eso solo funciona si el árbol quedó
**parejo** (ramificado). Si los `id` entraron ya ordenados (1, 2, 3, 4…), el árbol no se
ramifica: queda como una **escalera de un solo lado**, un pasillo largo de N escalones. Y
recorrer esa escalera es tan lento como la Lista (**O(N)**). A eso le decimos que el ABB
**se degrada**.
- **El B+** es como un **diccionario con pestañas** o el índice de un libro: no importa cómo
llegaron las palabras, siempre me lleva derechito a la página. Se mantiene rápido
(**O(log N)**) pase lo que pase, porque se reacomoda solo para no quedar nunca
desbalanceado.

Ese es justo el corazón del laboratorio: ver cómo el ABB brilla con datos desordenados pero
se cae con datos ordenados, mientras que el B+ nunca se cae.

---

## 3. Las tres estructuras y mis decisiones de diseño

Estructura
Cómo busca
Complejidad

**Lista**
recorre de uno en uno
O(N)

**ABB**
baja por el árbol (menor a la izq., mayor a la der.)
O(log N) desordenado · **O(N) ordenado (se degrada)**

**B+**
baja por el árbol y los datos quedan en las hojas
O(log N) **siempre**

Las decisiones que tomé y por qué:

- **La Lista la hice con la lista de Python** (el profe lo permitió). Insertar es meter al
final (rápido), y buscar es recorrerla de principio a fin, así que la búsqueda sigue siendo
O(N), que es justo lo que quiero mostrar.
- **El ABB lo hice iterativo, no recursivo**, por dos razones. La primera y más importante:
**no se desborda**. Con los `id` ordenados el árbol queda de N niveles de profundidad (la
escalera), y un ABB recursivo tendría que llamarse a sí mismo N veces anidadas; con N
grande eso **supera el límite de recursión de Python y el programa se cae**. El iterativo
usa un `while` y baja por el árbol sin ese problema. La segunda razón: es un poquito **más
efeciente**, porque cada llamada recursiva tiene un costo extra (guardar y preparar la
llamada), y el `while` se ahorra eso.
- **El B+** usa nodos de hasta 4 claves; cuando un nodo se llena, se parte solo y reparte las
claves. Por eso **queda siempre balanceado y nunca se degrada**, ni siquiera con los `id`
ordenados.

---

## 4. Cómo lo medí (la metodología)

Medir tiempos pequeños bien es más complicado de lo que parece, así que fui con cuidado:

- **Reloj de alta precisión:** uso `time.perf_counter()`.
- **Muchas búsquedas por medición.** Una sola búsqueda dura millonésimas de segundo:
demasiado poquito para medirla de forma confiable. Entonces hago **miles o millones de
búsquedas**, mido el total y lo divido entre cuántas hice. Así **cada medición dura más de
1 segundo**, que fue lo que pidió el profe. Un detalle clave: para que pasara de 1 segundo
**subí el número de búsquedas (M), no el número de estudiantes (N)** — así no cambio el
tamaño del problema que estoy midiendo.
- **10 repeticiones** de cada medición. Reporto el **promedio ± la desviación estándar**. El
`±` es el promedio *más o menos* cuánto variaron las 10 repeticiones entre sí: si ese
número es chiquito, las medidas salieron muy parejas (confiables); si es grande, algo las
estaba moviendo.
- **Apago el recolector de basura** (`gc.disable()`) mientras corre el cronómetro, para que
Python no me meta una pausa en la mitad de una medición y la dañe.
- **Rango de N:** uso **más valores con `id` aleatorios** (de 1.000 a 100.000) y **menos con
`id` ordenados** (de 1.000 a 20.000). ¿Por qué menos en ordenados? Porque **construir** el
ABB con `id` ordenados es lentísimo (queda armando la escalera entera, O(N²)) y arriba de
20.000 se demora demasiado solo en construirse.

---

## 5. Cómo correr el proyecto

Las instrucciones paso a paso están en **`COMO_CORRER.md`**. En resumen (Windows):

```
pip install matplotlib
python pruebas.py && python experimento.py && python graficas.py
```

- `pruebas.py` revisa que las tres estructuras funcionen bien.
- `experimento.py` mide los tiempos y guarda el resumen en `datos/resultados.csv`.
- `graficas.py` lee ese CSV y genera `figuras/graficas.png` y las tablas en `datos/tablas.md`.

---

## 6. Qué encontré (resultados)

Las tablas completas están en **`datos/tablas.md`** y las gráficas en
**`figuras/graficas.png`**. Acá dejo el resumen.

**Tiempo de una búsqueda (µs), `id` aleatorios.** La última columna es cuántas veces más
lenta es la Lista que el B+:

N
Lista
ABB
B+
Lista es … más lenta que B+

1.000
22,2
1,31
1,25
18×

20.000
566
3,13
2,55
222×

100.000
7.042
5,50
4,53
**1.555×**

**Tiempo de una búsqueda (µs), `id` ordenados.** Acá el ABB se degrada; la última columna es
cuántas veces más lento es el ABB que el B+:

N
Lista
ABB
B+
ABB es … más lento que B+

1.000
19,0
50,0
1,26
40×

20.000
432
1.102
2,79
**395×**

**La prueba de la degradación: la altura de los árboles.** La altura es cuántos niveles hay
que bajar; con `id` ordenados el ABB tiene altura igual a N (la escalera), y por eso se vuelve
tan lento:

N
ABB aleatorio
ABB ordenado
B+

1.000
~23
**1.000**
~6

20.000
~34
**20.000**
~9

---

## 7. Las gráficas (y por qué son 4)

En `figuras/graficas.png` hay **4 gráficas**: los `id` aleatorios arriba y los ordenados
abajo, y cada caso en **dos escalas**, normal y logarítmica. Las puse así a propósito:

- En la **escala normal** se ve lo brutal que crece la curva lenta (la Lista, o el ABB
ordenado): crece tanto que **aplasta** a las otras dos contra el piso y uno no alcanza a
distinguir el ABB del B+.
- En la **escala logarítmica** (la que pidió el profe) ese problema se arregla: comprime los
valores grandes y estira los chiquitos, así que **se ven las tres curvas** al tiempo y se
puede comparar bien el ABB contra el B+.

Las **rayitas verticales** en cada punto son la **desviación estándar** (± 1): qué tanto
variaron las 10 repeticiones de esa medición. Casi no se notan porque salieron muy parejas
(buena señal).

---

## 8. Análisis y hallazgos

- **La Lista es O(N):** cuando N se duplica, su tiempo se duplica. Con 100.000 estudiantes
llega a ser **1.555 veces más lenta que el B+**. Sirve para pocos datos, nada más.
- **Los árboles son O(log N) con `id` aleatorios:** casi no crecen. Pasar de 1.000 a 100.000
estudiantes apenas les sube el tiempo (se quedan en unos pocos µs).
- **El ABB se degrada con `id` ordenados:** su altura se vuelve **igual a N** (la escalera de
un solo lado), así que buscar en él cuesta O(N), como en la Lista. La tabla de alturas lo
demuestra: con N=20.000 la altura del ABB ordenado es **20.000**, mientras que la del B+ es
**~9**.
- **El B+ nunca se degrada:** se mantiene rápido (O(log N)) en los dos casos. Es el más
robusto, y por eso es el que usan las bases de datos de verdad.
- **El entorno afecta la medición.** Esto lo vi en carne propia: en una primera corrida, con
el navegador y OneDrive abiertos, el ABB ordenado en N=20.000 se me **disparó** a 21.101 µs
con una desviación de 62.248 (¡más grande que el propio promedio!). Eso pasó porque otros
programas le estaban robando el procesador al experimento en plena medición. Cerré todo y
volví a correr, y ese mismo dato bajó a **1.102 ± 23,7**, ya limpio y parejo. Por eso es
tan importante controlar el entorno cuando uno mide tiempos.

---

## 9. Conclusión

El **B+ es la estructura más robusta**: es O(log N) siempre, sin importar si los datos vienen
ordenados o desordenados —por eso lo usan las bases de datos reales—. El **ABB** es excelente
con datos desordenados, pero **peligroso** con datos ordenados, porque se degrada a O(N) y se
vuelve tan lento como la Lista. Y la **Lista** solo sirve cuando hay pocos datos.

---

## 10. Entorno (mi computador)

Procesador
AMD Ryzen 3 7320U with Radeon Graphics (2,40 GHz)

RAM
16 GB (13,7 GB utilizables)

Sistema operativo
Windows 11, 64 bits (x64)

Python
3.13.2

matplotlib
3.11.2

Fecha de la corrida
8 de octubre de 2026, ~10:50 a. m.

FACTOR usado
1 (corrida normal, 10 repeticiones)

---

## 11. Archivos del proyecto

Archivo
Qué es

`lista.py`, `abb.py`, `bmas.py`
Las tres estructuras

`pruebas.py`
Verifica que las estructuras funcionan

`experimento.py`
Mide los tiempos y guarda `datos/resultados.csv`

`graficas.py`
Genera `figuras/graficas.png` y `datos/tablas.md`

`COMO_CORRER.md`
Instrucciones paso a paso

`GUIA_SUSTENTACION.md`
Explicación detallada para la sustentación

`README.md`
Este documento

---

## 12. Código de honor

Declaro que:

- Desarrollé este laboratorio **con ayuda de una inteligencia artificial (Claude)**, con la
que fui construyendo y entendiendo el código (las estructuras, el experimento y las
gráficas).
- **Discutí ideas generales del diseño del experimento con una compañera** (trabajo en equipo
permitido y declarado). Cada una entregó su propio código y sus propios datos.
- **Las mediciones las hice yo**, en mi propio computador, con las condiciones descritas en la
sección "Entorno".
- **Entiendo cómo funciona el código y puedo sustentarlo.**
